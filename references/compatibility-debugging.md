# Compatibility and Deep Debugging

Read this file when behavior differs by operating system, architecture, cloud provider, core version, client, or network—or when an ordinary fix fails repeatedly.

## Build the compatibility fingerprint

Capture only facts that can change the chosen procedure:

| Dimension | Fingerprint | Typical adapter |
|---|---|---|
| Control host | Windows/Linux/macOS, shell, CLI path/version, auth freshness, proxy environment | avoid nested quoting; use a small script; renew CLI auth; bypass local proxy for private URLs |
| Cloud plane | provider, account/project, region, instance type, provider firewall/API authority | provider-specific discovery and firewall operation; distinguish shell access from control-plane authority |
| Server | distro/version, CPU architecture, init system, package manager, privilege, memory/disk | select matching release asset/repository/service unit; add resource safeguards only when measured |
| Proxy core | Xray/Hysteria/Mihomo version, native config schema, CLI output fields, service layout | inspect `--help`, version output, native config test, and installed unit instead of assuming an older interface |
| Client | product/platform/version, supported protocols/fields, import mode, cache/data state | complete YAML versus node URI; capability-minimized profile; fresh profile/data directory |
| Network | client ISP, TCP/UDP reachability, DNS, MTU, proxy variables, IPv4/IPv6, provider and host firewall | choose transport, bypass unintended proxy, inspect both firewall layers, run paired path tests |

Do not collect every possible fact up front. Start with the dimension implicated by the symptom and expand only to adjacent dependencies.

## Adapter rules

- Detect capabilities before choosing commands. A package name, release filename, config field, or CLI subcommand can differ by distro, architecture, and version.
- Treat actual command output and native schema errors as the contract. If a generated field is empty, inspect the producing command's current output names before rewriting the configuration.
- If the server cannot reliably fetch an official release, fetch it on a trusted control host, verify provenance/checksum there, transfer it, and verify the remote hash. Do not silently switch to an unofficial mirror.
- On Windows, move JSON/JMESPath/remote-shell complexity into a temporary script and keep secrets out of its literal text. Inspect each bounded phase instead of waiting on one opaque long command.
- When package installation fails, distinguish missing repository, unsupported architecture, expired metadata, privilege, and network failure. Do not treat `package not found` as product absence.
- On small VPS instances, measure memory pressure, CPU throttling, and disk before adding swap, priority, or buffer tuning. Resource workarounds are environment adapters, not protocol defaults.

## Vertical isolation ladder

1. Preserve the exact symptom, timestamp, client/core versions, and last known-good state without exposing credentials.
2. Reproduce once on the original path; record failure, timeout, and cache behavior.
3. Locate the boundary: control plane, host/service, public reachability, protocol handshake, subscription delivery, client import, or target application.
4. Build the smallest safe probe for that boundary. Prefer native config tests and protocol-aware clients over generic port checks.
5. Compare a known-good sibling or minimal profile while changing one dimension only.
6. If the failure moves, follow it; if it stays, deepen instrumentation at that boundary. Do not keep rotating unrelated settings.
7. Recompose the full configuration and rerun layered acceptance. A minimal profile proving compatibility is not the final deliverable unless the user requested it.

## Common deep-dive branches

### Provisioning or service start

- Confirm asset architecture, checksum, executable permission, config path, service user, and effective unit.
- Compare the generated config against the installed core's native schema.
- Separate a hanging installer from a slow/no-output remote shell by running bounded stages and inspecting process/service state.

### Client import or `EOF`

- Separate node URI import from HTTP(S) subscription import.
- Compare served bytes with the local file, then run the same core/version family used by the client when possible.
- Test protocol and optional-field support. Create a reduced compatibility profile only to isolate the unsupported field, then restore all required nodes and policies in the compatible shape.
- Test with a clean profile/data directory to distinguish parsing from first-download or stale-cache failure.

### Connected but slow

- Compare server-local, raw client-server transport, proxy protocol, and destination-specific paths.
- Test TCP and UDP separately before choosing Reality versus Hysteria2.
- Escalate to retransmit, congestion-window, MTU, QUIC debug, and route/ASN evidence only after simpler layer separation.

### Works once but not after restart

- Re-read the effective service/task definition, runtime state, listener, environment, working directory, permissions, and exact endpoint.
- Reboot or reproduce the relevant login/battery condition when persistence is a requirement. A definition without a running listener is not persistence.

## Generalization boundary

Record a proven adapter as a conditional rule, for example: "When the installed core changes an output field, parse the observed output" or "When private URL tests inherit a loopback proxy, rerun direct." Do not encode a historical host, provider ID, version, IP, or credential as the rule itself.
