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

## Retire the resource graph, not only the instance

Terminating compute is not proof that a node has stopped costing money or disappeared from clients. Static/reserved public IPs, detached disks, snapshots, custom images, NAT gateways, load balancers, security groups, key pairs, DNS, hosted subscriptions, scheduled servers, QR artifacts, tailnet records, and client databases can have independent lifecycles. On AWS in particular, an Elastic IP can remain allocated and billable after its instance is gone; a root EBS volume is removed only when its attachment has `DeleteOnTermination=true`.

When a user says “delete everything,” resolve the boundary before mutation: only idle remnants, one named node and its dependencies, or every resource in the named account/regions. State which live nodes and subscription paths will stop working. Do not interpret “all” across unrelated accounts, providers, regions, or workloads.

### Pre-delete ledger

For every in-scope region, inventory and bind exact IDs before deleting:

- non-terminated instances and each attached volume's deletion policy;
- allocated public IPs and whether each is associated;
- unattached volumes, snapshots, custom images, NAT gateways, and load balancers;
- non-default security groups, key pairs, DNS/certificate objects, and other node-specific access objects;
- tailnet device state;
- every authoritative and derived subscription, encoded link bundle, QR artifact, persistent serving task/listener, and active client database.

Back up the active client and subscription configuration needed for rollback. Keep backups outside active serving paths and exclude them from “live reference” searches.

### Safe deletion order

1. Release already-disassociated public IPs that are proven in scope.
2. Terminate the exact instances and wait for the provider's terminal state.
3. Re-inventory; confirm expected volumes were deleted, then remove authorized detached volumes and any newly disassociated public IPs.
4. Delete dependent security groups, key pairs, images, snapshots, DNS, or hosted endpoints only after their dependencies are gone.
5. Remove retired nodes from every active subscription variant, proxy group, raw link list, encoded derivative, QR artifact, and client database. Regenerate derivatives from the authoritative source instead of patching each representation independently.
6. Restart or reload persistent subscription delivery when required, then validate the bytes clients actually receive.

### Zero-residual acceptance

Use a scoped ledger rather than a single success message. For a full regional retirement, require zero in-scope non-terminated instances, volumes, and allocated public IPs; exact node-specific security groups and key pairs absent; no retired node in active client/subscription data; no dangling proxy-group references; and the surviving subscription fetched successfully, hash-matched to its source, and accepted by the target core with a fresh data directory. Re-check persistent task state and listener after any restart.

An offline Tailscale device record is normally a non-billable stale control-plane object, not proof that cloud resources remain. Remove it only when the user also authorizes tailnet cleanup. Cost Explorer can lag behind deletion, so use live inventory to prove current resource removal and label billing data as delayed rather than retrying destructive actions.

### Unexpected cost after deletion

Do not assume the remaining cost is CPU. Group billing by service and usage type, then compare it with the live resource ledger. Check public IPv4 allocation hours, data transfer, detached storage, snapshots/images, NAT/load-balancer hours, and taxes or credits separately. A prior month's charge remains payable after cleanup; the acceptance condition is that no current in-scope billable resource remains, not that the historical bill instantly becomes zero.
