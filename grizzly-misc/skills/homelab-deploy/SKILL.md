---
name: homelab-deploy
description: Deploy applications to the Grizzly Endeavors homelab Kubernetes cluster. Use when deploying apps to the cluster, onboarding a new app to Flux GitOps, writing or editing Helm charts / raw K8s manifests for the homelab, configuring ingress for a bearflinn.com subdomain, wiring app secrets through OpenBao + External Secrets, choosing a storage class, setting up CI/CD with the self-hosted ARC runners, building Rust binary releases, or debugging a homelab deployment. Covers both first-party apps (source + deploy/ chart) and personal/third-party apps (manifests in lab-apps).
---

# Homelab Deploy

Authoritative infra repo: **`~/Projects/grizzly-platform`** (the platform/IaC
repo, formerly `lab-iac` on GitHub). It is the source of truth — read it rather
than trusting this skill for volatile specifics.

| Need | Read in grizzly-platform |
|------|--------------------------|
| Machines, specs, **live IPs/roles** | `docs/hardware.md`, `docs/network.md` |
| How the cluster was built + smoke tests | `docs/k8s-cluster-standup.md` |
| NodePort allocations | `docs/nodeport-allocation.md` |
| Why anything is the way it is | `docs/decisions/` (ADRs) |
| OpenBao secrets (paths, auth, how-tos) | `docs/runbooks/openbao-quickref.md` |

**Never hardcode IPs or node names** into manifests or this skill — they live in
`ansible/group_vars/all/network.yml` and drift. This skill stays accurate by
describing the *model* and pointing at those docs.

## Architecture (the durable shape)

- **Cluster:** K8s v1.33.10, **Cilium** CNI, **Flux** GitOps. One control plane
  (`dell-inspiron-15`) + workers (`quanta` is the main workhorse; `intel-nuc`,
  `optiplex`). Check `kubectl get nodes` for current Ready state.
- **Storage:** **democratic-csi** on the Dell **R730xd** (not a cluster node).
  See [Storage](#storage).
- **Ingress / TLS:** Internet → **Hetzner VPS (Caddy, wildcard `*.bearflinn.com`
  TLS via Cloudflare DNS-01)** → dedicated **WireGuard tunnel** → R730xd iptables
  DNAT → K8s NodePort → **ingress-nginx** → app. In-cluster traffic is **plain
  HTTP**. Any `*.bearflinn.com` subdomain not explicitly claimed in the proxy-vps
  Caddy config auto-routes to the cluster ingress — **new subdomains need no
  proxy-VPS change** (ADR-019).
- **Secrets:** **OpenBao** is the source of truth, consumed via **External
  Secrets Operator** (`ClusterSecretStore/openbao`). See [Secrets](#secrets).
- **Registry:** app images go to **GHCR** (`ghcr.io/grizzly-endeavors/<repo>`).
  An in-cluster OCI registry also exists (S3→MinIO) for internal images.
- **Runners:** ARC v2 self-hosted, scale set **`lab-runners`** → `runs-on: lab-runners`.

## Two delivery models — pick the right one

### First-party app (you own the source code)
Repo created from **`grizzly-endeavors/app-deploy-template`** (`~/Projects/app-deploy-template`):
contains a `deploy/` Helm chart + `Dockerfile` + two workflows.

1. Create repo from the template.
2. Run the **Register with Flux** workflow (`workflow_dispatch`) once — it calls
   the reusable `register-app.yaml` in grizzly-platform, opening an auto-merging
   PR that adds `kubernetes/apps/<app>/` (a Flux `GitRepository` + `HelmRelease`
   pointing at your repo's `deploy/`).
3. From then on, **push to `main`** → `deploy.yaml` builds the image, pushes to
   GHCR (`:<sha>`), bumps `image.tag` in `deploy/values.yaml`, commits `[skip
   ci]`; **Flux reconciles within ~1 min**. No manual `helm`/`kubectl`.

Mirror an existing one: `grizzly-platform/kubernetes/apps/{landing-page,resume-site,caz-portfolio}`.

### Personal / third-party app (upstream image or chart, no source)
Manifests live in the **`lab-apps`** repo (`~/Projects/lab-apps`), `apps/<name>/`,
reconciled by the `personal-apps` Flux Kustomization (ADR-025). Add a folder of
raw manifests (or a `HelmRelease` against an upstream `HelmRepository`) and list
it in `apps/kustomization.yaml`. One PR; Flux does the rest.

Mirror an existing one: `lab-apps/apps/{actual-budget,obsidian-livesync}`.

## Ingress (both models)

Plain HTTP, `ingressClassName: nginx`, **no TLS block** (Caddy terminates TLS
upstream). Host is a `bearflinn.com` subdomain.

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: <app>
  annotations:
    nginx.ingress.kubernetes.io/proxy-body-size: "10m"  # if uploads
spec:
  ingressClassName: nginx
  rules:
    - host: <app>.bearflinn.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: <app>
                port:
                  number: <port>
```

cert-manager is installed but only has a self-signed ClusterIssuer — **do not**
add a `tls:` block or Let's Encrypt annotations for web ingress.

## Storage

democratic-csi, R730xd. Check `kubectl get sc`.

| Class | Backing | Access | Reclaim | Use for |
|-------|---------|--------|---------|---------|
| `iscsi-zfs` (default) | ZFS zvol, ext4 | RWO | Delete | databases, **SQLite**, single-writer |
| `iscsi-zfs-retain` | ZFS zvol, ext4 | RWO | **Retain** | stateful data that must survive PVC deletion (ADR-026) |
| `nfs-mergerfs` | MergerFS bulk | RWX | Delete | shared / multi-attach / many-reader |

- **SQLite or any embedded DB → iSCSI, never NFS** (NFS locking corrupts SQLite).
- RWO ⇒ single replica + `strategy: Recreate` (rolling update Multi-Attach-fails).
- `prune: true` on the Flux Kustomizations means deleting an app folder deletes
  its PVC unless the class/PV is Retain. Use `iscsi-zfs-retain` for data you care
  about, and document a backup (no `VolumeSnapshotClass` is installed).

## Secrets

**OpenBao** is the source of truth (ADR-023/024); **Infisical holds only the
OpenBao unseal keys** — it is not a general secret store. Quickref:
`grizzly-platform/docs/runbooks/openbao-quickref.md`.

Workloads consume secrets via **External Secrets Operator**: write an
`ExternalSecret` next to the consuming release referencing
`ClusterSecretStore/openbao`; ESO materializes a K8s `Secret`.

- Paths (KV v2, mount `secret/`): platform → `grizzly-platform/<domain>/<name>`;
  personal apps → `lab-apps/<app>/<name>`.
- Example to copy: `lab-apps/apps/obsidian-livesync/externalsecret.yaml`.
- If an app **can't consume an env/file secret** (some store credentials in their
  own DB after UI entry), keep the value in OpenBao as a record and skip the
  ExternalSecret — don't create a Secret the app never reads (see ADR-026 / Actual Budget).

## Debugging (least-verbose first — save context)

```bash
kubectl get pods -n <ns>
kubectl logs deploy/<app> -n <ns> --tail=20
kubectl rollout status deploy/<app> -n <ns>

# Flux: is the app reconciling?
flux get kustomizations -n flux-system          # personal-apps / apps / infrastructure
flux get helmreleases -A
flux reconcile kustomization <name> -n flux-system --with-source   # force a sync

# CI
gh run list -L 3 ; gh run view <id>
```

Avoid `kubectl describe`, `-A` dumps, full logs, `get events` unless actively debugging.

## References

- `references/app-delivery.md` — chart/manifest conventions, Dockerfile patterns, ingress, resource sizing, connecting to R730xd Postgres.
- `references/ci-cd-runners.md` — the GitOps CI model, GHCR build/tag-bump, ARC `lab-runners`, Rust binary releases.
