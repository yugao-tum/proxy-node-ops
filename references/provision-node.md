# Provision or Replace a Node

Read this file for live discovery, new-node creation, replacement, firewall work, service installation, Tailscale enrollment, cutover, and layered acceptance. Read [retire-node.md](retire-node.md) only when old resources will actually be removed.

## Lock the intended outcome

Resolve the target geography, provider or allowed provider set, client, protocol constraints, expected traffic, services that must coexist, and acceptance evidence. Ask only for missing choices that change cost, compatibility, or architecture.

If the user has not chosen a provider product or plan and the alternatives materially differ, present a concise recommendation plus meaningful alternatives and obtain the selection before creating a billable resource. Do not repeat the choice when the user already selected it. For AWS, use [providers/aws.md](providers/aws.md) for the choice and live cost explanation.

## Build the four-plane baseline

Do not infer infrastructure from SSH history, `known_hosts`, filenames, or an old subscription.

| Plane | Confirm live | Common false proof |
|---|---|---|
| Cloud control plane | provider, account/project, region/zone, exact instance ID, state, public IP, provider firewall | a reachable IP or remembered name |
| Tailscale | hostname, tailnet IP, online state, tags, key/approval state | `tailscaled` installed or an old machine entry |
| Node OS | OS/architecture, access path, resources, services, configs, users, listeners, host firewall | package installed or service enabled |
| Client delivery | protocol parameters, node labels, groups, endpoint bytes, persistence | local YAML exists or one fetch once succeeded |

Classify each discovered asset as intended-current, candidate, legacy-confirmed, stale record, or unresolved. Never mutate an unresolved asset.

Before replacement, record the current service/configuration state, both firewall layers, client behavior, and a recoverable backup path. Identify unrelated workloads that must remain available.

## Choose the smallest viable design

- Prefer Reality over TCP when UDP is unavailable or unreliable.
- Consider Hysteria2 when the measured TCP path is lossy or congested and UDP works.
- TCP and UDP may share the same numeric port when both provider and host firewalls allow their respective protocols.
- Install one proxy service on a constrained node unless the user requires multiple protocols, a panel, or redundancy.
- Measure memory, CPU throttling, and disk before applying swap, priority, buffer, or kernel workarounds.

## Stage and implement

1. Stage a replacement without deleting the current path.
2. Install from an official repository or release and verify version plus checksum/signature when published.
3. Generate credentials on the target or through a protected temporary process. Follow [secret-handling.md](secret-handling.md); never echo private keys or full client URIs into routine output.
4. Validate configuration before restart and keep the prior configuration recoverable until acceptance passes.
5. Use the platform service manager with a restart policy, restrictive configuration/key permissions, and a low-privilege service account when supported.
6. Open only the required protocol and port in the provider and host firewalls, then re-read the effective rules.
7. For Tailscale, use a one-off/tagged key when authorized or surface the browser authorization URL. Verify the intended peer after authorization rather than assuming enrollment completed.

For repeatable Tailscale automation, prefer OAuth-generated tagged keys; for one server, prefer a one-off key. Keep reusable keys out of commands and generated scripts. Track the complete intended `tailscale up` argument set because omitted flags can change later state.

## Layered acceptance

Use observable checks appropriate to the design:

1. The proxy core's native configuration test passes.
2. The service is active and restart-managed.
3. The expected TCP or UDP listener belongs to the expected process.
4. The port is reachable from outside the host through the intended network path.
5. A protocol-aware client completes authentication and connection.
6. Observed proxy egress matches the intended node or routed exit.
7. Tailscale shows the intended peer online when mesh administration is part of the design.
8. Logs after the real test show no restart loop or new fatal error.

A service can be active behind a blocked provider firewall; a port can listen while authentication or client parameters are wrong. Do not collapse these checks into “works.”

## Cut over

Update the authoritative client configuration and selectors only after the staged node passes. For Clash/Mihomo delivery, continue with [clash-mihomo.md](clash-mihomo.md) and validate the served bytes. Confirm the client can use the replacement before draining the old path.

If retirement is authorized, hand off the exact legacy resources and dependency boundary to [retire-node.md](retire-node.md). A replacement request alone does not authorize deleting unrelated workloads, tailnet devices, subscriptions, addresses, disks, or snapshots.
