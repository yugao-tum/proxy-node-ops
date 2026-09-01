# Compatibility and Deep Debugging

Read this file when behavior differs by operating system, architecture, provider, core version, client, or network, or when an ordinary fix fails repeatedly. Its job is to isolate the failing boundary and hand the task to the relevant operational reference without duplicating that reference's procedure.

## Build the compatibility fingerprint

Capture only facts that can change the next test:

| Dimension | Fingerprint | Typical adapter |
|---|---|---|
| Control host | OS, shell, CLI path/version, auth freshness, proxy environment | small scripts instead of nested quoting; renew auth; bypass unintended proxy |
| Cloud plane | provider, account/project, Region, instance product, provider firewall/API authority | provider-specific inventory and firewall operation; separate host from control-plane authority |
| Server | distro/version, CPU architecture, init system, package manager, privilege, memory/disk | matching release/repository/service unit; measured resource safeguard |
| Proxy core | product/version, native schema, CLI fields, service layout | inspect current help/output and run the native config test |
| Client | product/platform/version, protocol/field support, import mode, cache/data state | complete subscription versus URI; reduced diagnostic profile; fresh data directory |
| Network | ISP, TCP/UDP reachability, DNS, MTU, proxy variables, IPv4/IPv6, both firewalls | transport choice, direct probe, paired path test |

Start with the dimension implicated by the symptom and expand only to adjacent dependencies.

## Adapter rules

- Detect capabilities before selecting package names, release assets, config fields, or CLI subcommands.
- Treat native command output and schema errors as the current contract. Inspect the producing command when a generated value is empty.
- If the server cannot fetch an official release reliably, download on a trusted control host, verify provenance/checksum, transfer it, and verify the remote hash. Do not silently use an unofficial mirror.
- On Windows, move JSON/JMESPath/remote-shell complexity into a short temporary script with bounded phases and no literal secrets.
- Distinguish missing repository, unsupported architecture, stale metadata, privilege, and network failure; `package not found` is not product absence.
- Measure memory pressure, CPU throttling, and disk before applying swap, priority, or buffer workarounds.

## Vertical isolation ladder

1. Preserve the exact symptom, timestamp, client/core versions, and last known-good state without credentials.
2. Reproduce once on the original path and record failure, timeout, and cache behavior.
3. Locate the boundary: control plane, host/service, public reachability, protocol handshake, subscription delivery, client import, or target application.
4. Build the smallest safe probe for that boundary. Prefer native configuration tests and protocol-aware clients over generic port checks.
5. Compare a known-good sibling or minimal profile while changing one dimension only.
6. Follow the failure when it moves; deepen instrumentation where it stays. Do not rotate unrelated settings.
7. Recompose the full configuration and rerun the relevant layered acceptance. A minimal diagnostic profile is not the final deliverable unless requested.

## Handoff after isolation

- Provisioning, service start, firewall, listener, or restart persistence: continue with [provision-node.md](provision-node.md).
- Client import, served bytes, subscription `EOF`, GEO first-load, or routing schema: continue with [clash-mihomo.md](clash-mihomo.md).
- Connected-but-slow, TCP/UDP comparison, congestion, MTU, QUIC, or alternate egress: continue with [performance-testing.md](performance-testing.md).
- Credential exposure or reusable diagnostic output: continue with [secret-handling.md](secret-handling.md).
- Deletion state or continuing cloud cost: continue with [retire-node.md](retire-node.md) and the relevant provider reference.

## Generalization boundary

Record a proven adapter as a conditional rule, such as “parse the installed core's observed output field” or “bypass an inherited loopback proxy for a private URL.” Do not encode a historical host, provider ID, version, IP, or credential as the reusable rule.
