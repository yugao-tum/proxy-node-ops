# Node Lifecycle

Read this file for live discovery, deployment, replacement, firewall work, Tailscale enrollment, or retirement.

## Build a four-plane inventory

Do not infer infrastructure from SSH history, `known_hosts`, filenames, or an old subscription.

| Plane | Confirm live | Common false proof |
|---|---|---|
| Cloud control plane | provider, account/project, region/zone, exact instance ID, state, public IP, security group/firewall | a reachable IP or remembered instance name |
| Tailscale | hostname, tailnet IP, online state, tags, key/approval state | `tailscaled` installed or an old machine entry |
| Node OS | OS/arch, access path, services, configs, users, listeners, host firewall, resources | package installed or service enabled |
| Client delivery | actual protocol parameters, node labels, groups, endpoint bytes, persistence | local YAML exists or one fetch once succeeded |

Classify each discovered asset as intended-current, candidate, legacy-confirmed, stale record, or unresolved. Never mutate unresolved assets.

## Preflight

- Resolve the user's target architecture and which existing service must remain available.
- Confirm TCP versus UDP requirements at both provider and host firewalls. Tailscale access does not bypass a public security group for public client traffic.
- Inspect current config permissions and service unit before replacing either.
- Record a recoverable backup path and the exact command or file move that restores it.
- When working from Windows, avoid deeply nested PowerShell/JMESPath/remote-shell quoting. Put complex remote work in a short temporary script, transfer it, run it in bounded phases, inspect each phase, then remove it.

## Provision or replace

1. Stage the replacement without deleting the current path.
2. Install from an official repository or release. Verify the downloaded version and checksum/signature where the project publishes one.
3. Generate credentials on the target or in a protected temporary process. Never echo private keys or full client URIs into routine logs.
4. Validate configuration before restart. Keep the previous config available until the new process is healthy.
5. Use `systemd` or the platform service manager with restart policy, a low-privilege account when supported, and restrictive config/key permissions.
6. Open only the required protocol/port in both firewall layers. Re-read the effective rules.
7. Enroll Tailscale with a one-off/tagged key when authorized, or surface the browser URL. After authorization, verify the intended peer rather than assuming the pending command completed.

For Tailscale automation, prefer one-off keys for single servers and OAuth-generated tagged keys for repeatable infrastructure. Never place a reusable key directly in command history. Track the full intended `tailscale up` argument set because omitted flags can change subsequent state.

## Layered acceptance

Use observable checks appropriate to the environment:

1. The program's native configuration test passes.
2. The service is active and enabled/restart-managed.
3. The expected TCP or UDP socket is owned by the expected process.
4. The port is reachable from outside the host and through the intended network path.
5. A protocol-aware client completes a connection.
6. The observed proxy egress matches the target node or routed exit.
7. Tailscale shows the intended peer online when mesh access is part of the design.
8. Logs after the test contain no restart loop or fresh fatal errors.

Do not collapse these into a single "works" check. A service can be active behind a blocked security group; a port can listen while authentication or client parameters are wrong.

## Cutover and retirement

- Add the replacement to the complete subscription and relevant groups.
- Test the served subscription with a clean client state when practical.
- Mark the old node unavailable before deleting it if a reversible drain is possible.
- Delete only exact cloud IDs the user authorized. Verify termination independently from a preceding stop request.
- Re-query cloud inventory, tailnet membership, subscription contents, and client egress after retirement.

If the old node hosts unrelated workloads, separate or migrate them first. A proxy replacement request does not authorize removing other services.
