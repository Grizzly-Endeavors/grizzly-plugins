# CI/CD & Self-Hosted Runners

The cluster is **GitOps**: CI builds and publishes artifacts and bumps a tag in
git — **Flux** does the actual deploy. **CI never runs `kubectl`/`helm` to
deploy.** Runtime secrets are injected at runtime via OpenBao + External Secrets,
**not** fetched in CI.

## First-party deploy pipeline (app-deploy-template `deploy.yaml`)

On push to `main` (paths-ignore `deploy/values.yaml`, `**.md`, `.github/**`):

1. Build image from root `Dockerfile`.
2. Push to **GHCR**: `ghcr.io/<owner>/<repo>:<sha>` and `:latest` (login with the
   built-in `GITHUB_TOKEN`, `packages: write`).
3. `yq` bump `image.repository`/`image.tag` in `deploy/values.yaml`, commit with
   `[skip ci]` (`contents: write`).
4. **Flux** sees the commit and reconciles the `HelmRelease` within ~1 min.

The build job runs on **`ubuntu-latest`** (GitHub-hosted) — fine for typical
Docker builds. Customize the workflow per app for tests, build args, caching.
The template skips build+bump while the `Dockerfile` is still the placeholder
stub, so a freshly-created repo doesn't bump to a non-existent image.

## Onboarding (app-deploy-template `register.yaml`)

One-time `workflow_dispatch` calling the reusable
`grizzly-endeavors/lab-iac/.github/workflows/register-app.yaml@master` (lab-iac =
the platform/grizzly-platform repo) with `app_name`, `namespace`, optional
`ingress_host`, `auto_merge`. It opens an auto-merging PR adding
`kubernetes/apps/<app>/` to the platform repo. Needs the `FLUX_OPS_APP_ID` /
`FLUX_OPS_APP_PRIVATE_KEY` org secrets (GitHub App for the PR).

Personal/third-party apps skip all of this — just add a folder in `lab-apps`
(see SKILL.md).

## Self-hosted runners (ARC v2)

- Scale set **`lab-runners`** → `runs-on: lab-runners`. Org `grizzly-endeavors`,
  controller in namespace `arc-systems`.
- Capabilities: **Docker-in-Docker**, **Rust toolchain** with **sccache** backed
  by MinIO/S3 (`SCCACHE_BUCKET`/`SCCACHE_ENDPOINT`), `gh`, Node.
- Use `lab-runners` for heavy/native builds (Rust, cross-compile, big images);
  `ubuntu-latest` is fine for ordinary Docker builds like the template's.
- Manifests: `grizzly-platform/kubernetes/infrastructure/github-runners/`.

## Rust binary release (CalVer, tag-triggered)

Still current; used by Rust projects shipping binaries. Build on `lab-runners`;
publish a GitHub Release.

```yaml
on:
  push:
    tags: ["v*"]
permissions:
  contents: write

jobs:
  checks:
    runs-on: lab-runners
    outputs: { tag: ${{ steps.v.outputs.tag }} }
    steps:
      - uses: actions/checkout@v4
      - id: v
        run: |
          TAG="${GITHUB_REF_NAME}"
          echo "$TAG" | grep -qE '^v[0-9]{4}\.[0-9]{2}\.[0-9]{2}(-[0-9]+)?$' \
            || { echo "::error::tag not CalVer vYYYY.0M.0D(-N)"; exit 1; }
          echo "tag=$TAG" >> "$GITHUB_OUTPUT"
      - run: cargo fmt --check
      - run: cargo clippy --all-targets -- -D warnings
      - run: cargo test --quiet
      - run: cargo deny check

  build:
    needs: checks
    strategy:
      fail-fast: false
      matrix:
        include:
          - { target: x86_64-unknown-linux-gnu,  runner: lab-runners, artifact: <app>-linux-x86_64 }
          - { target: aarch64-unknown-linux-gnu, runner: lab-runners, artifact: <app>-linux-aarch64, cross: true }
          - { target: aarch64-apple-darwin,      runner: macos-15,    artifact: <app>-macos-aarch64 }
    runs-on: ${{ matrix.runner }}
    env:
      CARGO_TARGET_AARCH64_UNKNOWN_LINUX_GNU_LINKER: aarch64-linux-gnu-gcc
    steps:
      - uses: actions/checkout@v4
      - if: runner.os == 'macOS'
        uses: dtolnay/rust-toolchain@stable
      - if: matrix.cross
        run: rustup target add ${{ matrix.target }}
      - run: cargo build --release --target ${{ matrix.target }}
      - run: cp target/${{ matrix.target }}/release/<bin> ${{ matrix.artifact }}
      - uses: actions/upload-artifact@v4
        with: { name: "${{ matrix.artifact }}", path: "${{ matrix.artifact }}" }

  release:
    needs: [checks, build]
    runs-on: lab-runners
    env: { GH_TOKEN: "${{ secrets.GITHUB_TOKEN }}" }
    steps:
      - uses: actions/checkout@v4
      - uses: actions/download-artifact@v4
        with: { path: release-artifacts }
      - run: gh release create "${{ needs.checks.outputs.tag }}" --generate-notes release-artifacts/*/<app>-*
```

aarch64-linux cross-compiles on `lab-runners` (linker env required); aarch64-mac
uses GitHub-hosted `macos-15`.

## Conventions

- **Deploy is Flux's job.** Don't add `kubectl`/`helm` deploy steps to CI.
- **App images → GHCR** (`ghcr.io/grizzly-endeavors/<repo>`). The in-cluster OCI
  registry is for internal images, not app delivery.
- **Runtime secrets → OpenBao + ExternalSecret**, never CI env or `--set`.
- `workflow_dispatch` on deploy workflows for manual re-runs; `paths` filters for
  monorepos; write a build summary to `$GITHUB_STEP_SUMMARY`.
