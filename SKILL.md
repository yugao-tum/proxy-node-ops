---
name: proxy-node-ops
description: "Plan, deploy, replace, troubleshoot, benchmark, deliver, and retire self-hosted VPS proxy nodes across cloud providers. Use for Xray VLESS Reality, Hysteria2, Tailscale administration paths, Clash/Mihomo subscriptions, cost-aware AWS node selection, migrations, compatibility failures, performance tests, or billable-resource cleanup; do not use for generic consumer VPN recommendations or unrelated cloud administration."
---

# Proxy Node Operations

Finish the requested node outcome and prove the real client path. Treat remembered IPs, saved links, prior commands, and old configurations as discovery hints, never as current state.

## Route the task

Choose one primary mode, then load only the references needed for that mode. If a task spans phases, load the next reference when that phase begins instead of loading the entire skill at once.

- **Create or replace a node:** read [references/provision-node.md](references/provision-node.md). For AWS product selection, promotional credits, Lightsail/EC2, or cost limits, also read [references/providers/aws.md](references/providers/aws.md) before provisioning. Read [references/retire-node.md](references/retire-node.md) only when an old node or residual resources will be removed.
- **Retire a node or remove continuing cost:** read [references/retire-node.md](references/retire-node.md). Also read the relevant provider reference when product-specific stop, delete, storage, or address behavior matters.
- **Troubleshoot a compatibility or repeated failure:** read [references/compatibility-debugging.md](references/compatibility-debugging.md), then follow its handoff to provisioning, performance, or subscription delivery only after locating the failing boundary.
- **Diagnose speed or compare routes/protocols:** read [references/performance-testing.md](references/performance-testing.md).
- **Create or repair Clash/Mihomo delivery:** read [references/clash-mihomo.md](references/clash-mihomo.md).
- **Handle credentials or create a reusable/public artifact:** read [references/secret-handling.md](references/secret-handling.md).

## Shared operating contract

1. Resolve the outcome, scope, explicit choices, and acceptance evidence before mutation. Do not reopen a choice the user already made unless live evidence shows it cannot meet the requirement.
2. Inspect the live cloud control plane, Tailscale state, node OS, and delivered client configuration as separate planes. A fact in one plane does not prove another.
3. Respect authority boundaries. Host access cannot change provider firewalls or delete cloud resources; a provider session does not authorize unrelated accounts, regions, tailnets, or client artifacts.
4. Prefer stage -> validate -> cut over -> retire. Before destructive work, bind exact resource IDs, preserve a recoverable configuration, and state the service impact.
5. Keep credentials and topology-linked identifiers out of routine logs, shell history, reusable resources, benchmarks, and repository history. Use protected inputs and redacted diagnostics.
6. Validate by layers appropriate to the mode. Provisioning success, a running process, an open port, or a local YAML file alone is never end-to-end proof.
7. Treat a timeout, `403`, empty result, missing CLI, or stale record as a blocked observation, not proof that a resource or service is absent.

## Depth and evidence

Start with the smallest pass that can answer the request. Escalate to a compatibility deep dive only when environment differences or repeated failure justify it, and to a causal performance deep dive only when speed or reliability is the target. Vertical depth follows one real failure through dependent layers; it does not broaden the project.

For a material blocker, preserve a compact issue record in the current task: symptom -> discriminating test -> observation -> cause or remaining hypotheses -> fix -> rollback -> verification -> generalization boundary. Add only proven, portable failure shields to reusable artifacts.

Lead the final report with the outcome. Include live acceptance evidence, what changed, rollback or deletion boundary, required user action, and unresolved limitations.

## Deterministic helpers

- Run `scripts/verify_clash_subscription.py` after creating or changing a subscription. It validates local and served state while redacting credentials.
- Run `scripts/audit_artifact_secrets.py` before finalizing a reusable skill, template, example, or diagnostic bundle. A clean scan reduces accidental disclosure risk but does not prove unknown secret formats are absent.

## Stop gates

Stop and request direction when the target or deletion boundary is ambiguous, required authorization is unavailable, an explicit product choice is still required, or the requested delivery would expose a private bearer credential beyond the stated access model.
