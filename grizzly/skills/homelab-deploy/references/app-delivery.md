# App Delivery Patterns

Conventions for the chart/manifests, container, ingress, storage, and data
dependencies of a homelab app. The delivery *mechanics* (Flux, GHCR, register
workflow) are in `ci-cd-runners.md`; this file is the app-shape detail.

## Where the manifests live

- **First-party app:** a `deploy/` Helm chart in the app's own repo, scaffolded
  from `app-deploy-template`. CI bumps `deploy/values.yaml` `image.tag`; Flux
  renders the chart. Edit `deploy/templates/*` to add resources (PVC, CronJob,
  ExternalSecret, etc.).
- **Personal/third-party app:** raw manifests (or a `HelmRelease` against an
  upstream `HelmRepository`) under `lab-apps/apps/<name>/`, listed in
  `apps/kustomization.yaml`. No chart of your own needed for a single-container
  upstream image — plain `Deployment`/`StatefulSet` + `Service` + `Ingress`
  (+ `PersistentVolumeClaim`) is cleaner. See `lab-apps/apps/actual-budget`.

## Dockerfile conventions (first-party)

Multi-stage, non-root, no secrets in the build context.

```dockerfile
FROM node:22-bookworm-slim AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:22-bookworm-slim AS runner
RUN addgroup --system --gid 1001 nodejs && adduser --system --uid 1001 app
USER app
COPY --from=builder --chown=app:nodejs /app/.next/standalone ./
EXPOSE 3000
CMD ["node", "server.js"]
```

Base images by stack: Node `node:22-bookworm-slim`, Python `python:3.12-slim`,
static `nginx:alpine`. Pin a real tag; CI tags the image with the commit SHA.

## Ingress

See the SKILL.md ingress block — `ingressClassName: nginx`, no `tls:` block,
host on `bearflinn.com`. Common annotation: `proxy-body-size` for uploads;
`proxy-read-timeout` / `proxy-request-buffering: "off"` for streaming/long polls.

## Resource sizing (starting points)

| Workload | CPU req/limit | Mem req/limit |
|----------|---------------|---------------|
| Static site | 50m / 100m | 64Mi / 128Mi |
| Node/Python service | 100m / 500m | 256Mi / 512Mi |
| Heavier service | 500m / 1 | 512Mi / 1Gi |

Set probes against a real health path; allow generous `initialDelaySeconds`
for apps that run DB migrations on boot.

## Persistent data

Pick the storage class per the SKILL.md table. Single-writer/SQLite → `iscsi-zfs`
(RWO, `strategy: Recreate`, replicas 1); shared/multi-reader → `nfs-mergerfs`
(RWX); must-survive-prune → `iscsi-zfs-retain`. No `VolumeSnapshotClass` is
installed, so back PVCs up explicitly (e.g. a `sqlite3 .backup` CronJob to an
`nfs-mergerfs` PVC — see `lab-apps/apps/actual-budget/backup-cronjob.yaml`).

## Connecting to Postgres / Redis / object storage

These foundation stores run on the **R730xd** (Docker Compose, ZFS tier), **not
in-cluster** — there is no `database` namespace or in-cluster Postgres service
anymore. From a pod, connect over the LAN to the R730xd (host/port in
`grizzly-platform/docs/network.md`; deploy details in `docker/` and
`ansible/playbooks/deploy-foundation-stores.yml`).

- Credentials come from **OpenBao via an `ExternalSecret`** (see SKILL.md
  Secrets), not `--set` flags or hand-written Secrets.
- MinIO (S3) has two instances: Obs (ZFS tier) and Bulk (MergerFS); pick per use.

## Checklist before opening the PR

- [ ] Storage class matches the access pattern (SQLite ⇒ iSCSI, not NFS).
- [ ] RWO volume ⇒ single replica + `strategy: Recreate`.
- [ ] Secrets via OpenBao/ESO, never plaintext in git.
- [ ] Ingress host is a `bearflinn.com` subdomain, plain HTTP, no `tls:`.
- [ ] Data that must survive ⇒ `iscsi-zfs-retain` (or PV patched to Retain) + a backup.
- [ ] Operational story addressed (health probe, where logs go, how to restore).
