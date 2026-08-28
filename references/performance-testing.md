# Performance Testing and Tuning

Read this file for slow nodes, route comparisons, protocol decisions, kernel tuning, or residential/alternate egress tests.

## Diagnose the layer before tuning

Measure these paths separately:

- server-local internet throughput and CPU/memory/NIC headroom;
- client-to-server latency, loss, retransmits, and raw transport throughput;
- proxy protocol throughput through the same server;
- destination-specific behavior and egress identity;
- TCP and UDP viability when choosing between Reality and Hysteria2.

If raw SSH/file transfer and VLESS are both slow while the server's own download is fast, the cross-border client-to-server path is the leading cause. Changing UUID, SNI, or reinstalling Xray is then a weak hypothesis. Conversely, a healthy raw path with a slow proxy justifies protocol/config inspection.

HTTP `403` proves that a server responded; it does not prove a browser session, login, checkout, or business action works. IP geolocation alone does not prove residential quality—check ASN/organization, repeated reachability, and the target application's behavior.

## Run paired evidence, not showcase tests

1. Freeze a baseline configuration and define the same endpoints, payload sizes, and client path for candidate tests.
2. Use repeated paired samples. Count every timeout/reset as a failure; for a quick low-risk test, three pairs are the minimum useful signal, and noisy paths warrant more.
3. Rank candidates by success rate first, then median latency/throughput. Keep tail latency and variance visible.
4. Separate generic web, bulk download/upload, and the actual business site. A residential route can improve a target marketplace while making general traffic dramatically worse.
5. Do not benchmark two agents against the same mutable node concurrently unless their changes are isolated.

## Reversible A/B discipline

- Back up the exact files and sysctls that may change.
- Change one variable at a time: congestion control, MTU probing, port, fingerprint/SNI, protocol, or egress route.
- Predefine a rollback trigger such as service failure, lower success rate, or material regression.
- After each test, verify service, listener, config permissions, and original egress. Remove temporary routes, listeners, credentials, and scripts.
- Preserve the winning change only when the repeated evidence supports it.

## Protocol-specific guidance

### VLESS Reality / TCP

- Verify Xray config and the effective Reality fields before blaming the network.
- BBR with an appropriate queue discipline and TCP MTU probing can help some lossy paths, but treat them as measured host-level experiments, not universal fixes.
- Alternate ports, fingerprints, or SNI values should be tested only when there is a concrete blocking/routing hypothesis.

### Hysteria2 / QUIC

- Use Hysteria2 as a candidate when TCP collapses under loss but UDP is usable, or as a parallel fallback rather than an automatic replacement.
- Confirm UDP at the provider firewall, host firewall, listener, and client network.
- Tune OS UDP buffers when the official guidance and measured workload justify it.
- Brutal bandwidth values are not an aspirational speed setting. Set them at or below demonstrated available bandwidth; values above the path capacity can reduce stability and waste traffic.
- Use the built-in protocol speed test when enabled, but also test real proxy egress because the internal speed test bypasses ACLs and outbounds.

## Residential or alternate egress

Treat an alternate egress as a separate product decision:

- compare direct VPS exit versus routed exit on identical samples;
- verify location and ASN rather than trusting the requested city label;
- measure the target site separately from generic throughput;
- prefer site-specific routing or a distinct client option when the alternate exit helps only one workload;
- never replace the main exit permanently when the test shows a large general regression.

Report the baseline, candidate, change, failure count, medians, business-site result, final state, and proof that rollback/cleanup succeeded.
