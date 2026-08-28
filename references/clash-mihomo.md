# Clash and Mihomo Subscription Delivery

Read this file for YAML, subscription URLs, QR codes, node/rule changes, DNS, persistence, or client `EOF` errors.

## Preserve the delivery contract

- A `vless://` or `hysteria2://` URI is a single-node share link. A Clash subscription URL is HTTP(S) and returns a complete Clash YAML document.
- If the user asks for all nodes, reconcile every intended node from the running servers to the YAML. Verify actual protocol, label, server, port, and group membership independently; do not carry obsolete names forward.
- A QR code must encode the intended URL or URI. Decode it after generation and compare exact bytes before delivery.
- A tokenized URL is bearer access, not per-user authorization. Tailscale membership plus a random token provides stronger private access; rotating only the URL cannot revoke node credentials already downloaded.

## Build the configuration deliberately

Keep node definitions, proxy groups, DNS, and routing as separate concerns. For a mainland-China policy, a maintainable order is usually:

1. private/local exceptions;
2. narrowly scoped reject rules;
3. explicit services that must proxy, including AI/media groups when requested;
4. explicit domestic exceptions;
5. maintained China domain data;
6. China IP data with `no-resolve` where appropriate;
7. non-China routing;
8. final fallback.

Rule order is behavior. Do not paste a large third-party ruleset wholesale or combine overlapping sources merely because they are popular. Compare source maintenance, Mihomo compatibility, coverage, overlap, first-load cost, and false-direct risk. Test frequent domestic services and record uncovered exceptions without claiming exhaustive business coverage.

When using Mihomo GEO data, prefer a source compatible with the selected Mihomo release. For China/private names under fake-IP mode, `fake-ip-filter-mode: rule` with `GEOSITE,cn,real-ip` and `GEOSITE,private,real-ip` can avoid proxying or synthesizing common domestic/private names while other traffic remains fake-IP. Treat this as a policy choice, not a universal default.

## Validate local and served states

Run `scripts/verify_clash_subscription.py` with the local file and served URL. Require at least:

- YAML structure loads and expected node/group names exist;
- group references resolve and no duplicate node/group names exist;
- Mihomo's native config test passes;
- when GEO/rule providers are used, a fresh empty data directory completes its first load instead of succeeding from cache;
- the endpoint returns HTTP 200 and the served bytes hash-match the intended local file;
- current node/group/rule counts match the design;
- a real client or Mihomo connection proves at least one node in each required protocol family.

Do not expose full token paths or node credentials in validation logs.

## Prove persistence

For a local or private subscription service, verify all of these together:

1. persistent service or scheduled task exists with the intended startup/restart behavior;
2. its runtime state is healthy;
3. the expected listener exists on the intended interface;
4. the exact tokenized URL fetch succeeds from the client-relevant network;
5. fetched bytes match the source YAML;
6. battery/login/reboot conditions relevant to the host do not silently suppress startup.

A temporary `python -m http.server`, a task definition without a listener, or one successful historical fetch is not continuous availability.

## Diagnose `EOF` by layers

Do not assume `EOF` is a network break or client-version issue. Check in this order:

1. Fetch the exact URL repeatedly and compare status, length, and hash.
2. Bypass unintended local proxy settings when testing LAN/Tailscale URLs.
3. Parse the fetched bytes and run Mihomo's native test; inspect the exact schema error.
4. Test in a fresh data directory. GEO/rule downloads can time out after YAML parsing and surface as `EOF` on mobile clients.
5. Check client support for every protocol and optional field; use a reduced compatibility profile only when evidence points to a client limitation.
6. Clear the failed client profile/cache only after the served artifact is corrected.

Common fixes must be evidence-specific: malformed YAML or truncated keys require restoring values and re-validating; first-download timeouts require a reachable maintained source or removal of the external dependency; a stale listener requires fixing persistence. Do not hide these different causes behind a generic "reimport the subscription" answer.
