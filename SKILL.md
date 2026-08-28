---
name: proxy-node-ops
description: "Operate self-hosted VPS proxy nodes end to end: discover live cloud and tailnet state, adapt across provider/OS/core/client variants, deploy or replace Xray VLESS Reality and Hysteria2 services, run reversible network tests, publish Clash/Mihomo subscriptions and routing, and verify persistence and client egress. Use for multi-cloud proxy-node setup, migration, compatibility debugging, tuning, troubleshooting, or subscription delivery; do not use for generic VPN recommendations or unrelated cloud administration."
---

# Proxy Node Operations

Finish the requested operational outcome and prove it at every layer. Treat prior commands, remembered IPs, saved links, and old configuration as discovery hints, never as current state.

## Load only the relevant detail

- For discovery, provisioning, replacement, firewall changes, Tailscale enrollment, or retirement, read [references/node-lifecycle.md](references/node-lifecycle.md).
- For slow nodes, route comparisons, protocol selection, kernel tuning, or residential egress tests, read [references/performance-testing.md](references/performance-testing.md).
- For Clash/Mihomo YAML, subscriptions, QR codes, routing, DNS, persistence, or `EOF`, read [references/clash-mihomo.md](references/clash-mihomo.md).
- For OS/architecture/provider/core-version/client/network mismatches or repeated failures, read [references/compatibility-debugging.md](references/compatibility-debugging.md).
- Whenever credentials are handled or a reusable artifact is created, read [references/secret-handling.md](references/secret-handling.md).
- Use `scripts/verify_clash_subscription.py` after creating or changing a subscription. Its output is deliberately credential-redacted.
- Use `scripts/audit_artifact_secrets.py` before finalizing reusable skills, templates, examples, or diagnostic bundles. Do not use it as a reason to print or delete live credentials.

## Choose depth deliberately

- **General pass:** fingerprint the environment, inspect current state, identify the failing plane, and apply the smallest safe check. Use for inventory, simple health checks, and well-understood operations.
- **Standard operation:** perform the full baseline -> change -> layered verification -> persistence/cutover loop. Use for deployment, migration, subscription edits, and ordinary troubleshooting.
- **Compatibility deep dive:** build the six-dimension compatibility matrix and isolate the smallest failing boundary. Use when platform, version, schema, import, or network behavior differs from the known-good path.
- **Causal performance deep dive:** instrument one end-to-end path, compare transports/protocols with paired A/B evidence, and trace the regression to a layer before tuning.

Start at the shallowest level that can answer the request. Escalate only when evidence shows a mismatch or the user asks for a deep investigation. Vertical depth means tracing one real failure through its dependent layers, not broadening into unrelated infrastructure.

## Operating invariants

1. Reconcile the real objective before acting: new node, replacement, optimization, private access, client delivery, or a combination. Preserve explicit protocol, geography, client, and deletion requirements.
2. Inventory four planes separately: cloud control plane, Tailscale control plane, node operating system, and delivered client configuration. A fact in one plane does not prove another.
3. Separate authority. Shell or Tailscale access can change the node but cannot change an AWS/GCP/OCI firewall or delete a cloud instance. Browser authorization may require the user; continue and verify immediately after they say it is complete.
4. Before destructive work, resolve exact instance IDs and take recoverable configuration backups. Prefer stage -> validate -> cut over -> retire. If the user explicitly requests deletion first, verify the exact targets and state the recovery consequence before deletion.
5. Keep secrets out of shell history, logs, memory, benchmark output, and repository files. Never transplant concrete keys, UUIDs, tokens, IPs, instance IDs, or subscription URLs from a prior conversation into reusable resources. Use placeholders and documentation-only addresses, one-off or narrowly scoped auth material, environment/stdin delivery, restrictive file ACLs, and redacted diagnostics. Deliver a requested client URI or subscription URL only in the user-facing result and warn that it is a bearer credential.
6. Do not call a node complete from provisioning success, a running process, or an existing scheduled task alone. Require configuration validation, active service, expected listener, external reachability, actual proxy egress, and persistence evidence.

## Core workflow

1. **Discover and classify.** Query live provider inventory and tailnet membership, inspect the host and current subscription, fingerprint compatibility dimensions, then report confirmed, blocked, stale, and unknown facts. Ignore legacy hosts the user has retired.
2. **Capture a baseline.** Record service/config state, firewall layers, public and tailnet addresses, current client behavior, and paired performance samples when speed is in scope. Back up only the files that may change.
3. **Choose the smallest architecture change.** Prefer Reality over TCP when UDP is unavailable or unreliable. Consider Hysteria2 when the measured TCP path is lossy or congested and UDP works. Dual TCP/UDP on the same numeric port is valid when both firewall layers allow the respective protocols.
4. **Implement with official artifacts.** Verify release provenance and checksums when available. Use a persistent service manager, least-privileged service account, narrow firewall rules, protected private keys, and deterministic configuration tests.
5. **Validate by layers.** Check config -> service -> listener -> outside reachability -> proxy egress -> real client path. For Tailscale, also verify the intended hostname/IP and online state after authorization.
6. **Benchmark changes as reversible A/B tests.** Change one variable at a time, count failures, compare repeated paired samples, and restore the prior state automatically or immediately when the candidate loses.
7. **Publish and persist the client configuration.** Preserve every intended node, actual protocol labels, group membership, route precedence, client compatibility, and protected access. Validate the served bytes, not only the local file.
8. **Cut over and retire.** Update subscriptions and selectors, verify clients can use the replacement, then stop/delete only the resolved legacy targets. Re-query provider and tailnet state afterward.
9. **Report evidence, not ceremony.** Lead with the outcome. Include what changed, live acceptance results, rollback location or reversal method, user action still required, and unresolved limitations.

## Convert failures into reusable knowledge

For every material blocker, keep a compact issue record in the current task: symptom -> discriminating test -> observation -> cause or remaining hypotheses -> fix -> rollback -> verification -> generalization boundary. Preserve the failure shield, not project-specific values. Do not add a one-off incident to this skill as a universal rule unless repeated evidence shows it changes future decisions.

## Stop gates

Stop and request direction when the target instance is ambiguous, required credentials or browser authorization are unavailable, a deletion target cannot be proven, or the requested change would expose a private subscription beyond the stated access model. A timeout, `403`, empty result, or missing CLI is a blocked observation—not proof that a node, rule, or service is absent.
