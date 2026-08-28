# Secret and Sensitive-Identifier Handling

Read this file whenever the task handles cloud credentials, SSH material, proxy credentials, Tailscale authorization, private subscription URLs, or reusable artifacts.

## Classify before handling

- **Secrets:** private keys, cloud access keys/secrets, OAuth/Tailscale auth keys, passwords, VLESS UUIDs used as credentials, Hysteria2 authentication, subscription path tokens, cookies, and bearer tokens.
- **Sensitive identifiers:** public node IPs, instance IDs, account/project/tenancy IDs, tailnet hostnames/IPs, email identities, key fingerprints, and private file paths.
- **Public but topology-linked values:** public keys, certificate fingerprints, SNI choices, ports, and node labels. They may be deliverable but should not be copied into a reusable skill.

The distinction changes redaction and delivery, not the requirement to avoid unnecessary persistence.

## Safe execution

- Discover whether a credential exists without printing its value. Prefer status/identity commands that prove authorization.
- Pass secrets through environment variables, stdin, protected secret stores, or restrictive temporary files. Avoid literal command arguments, generated scripts, URLs in logs, and shell history.
- Restrict local private-key ACLs before SSH use and remote config permissions before service start.
- Keep temporary credential lifetime bounded. Remove temporary copies after verification; do not delete the authoritative source unless explicitly requested.
- Do not place secrets in memory notes, comments, benchmark data, issue records, test fixtures, ordinary screenshots, unrequested QR previews, or repository history. A user-authorized QR delivery is a sensitive credential artifact and must be handled as such.

## Safe reusable artifacts

- Convert every project-specific value to a semantic placeholder such as `<instance-id>`, `<tailnet-host>`, `<uuid>`, or `<subscription-token>`.
- Use `example.com` and RFC 5737 documentation IP ranges when an example needs shape. Avoid realistic credential strings even when they are fake.
- Do not copy a prior command verbatim until it has been checked for embedded keys, callback URLs, signed query strings, user paths, IPs, or account identifiers.
- Run `scripts/audit_artifact_secrets.py <artifact-path>` before finalizing a skill, template, diagnostic bundle, or example set. Review findings in the source; the scanner reports type/file/line only and never the matched value.
- A clean scan reduces accidental inclusion risk but does not prove that a secret encoded in an unknown format is absent. Inspect provenance and intended content as well.

## User-facing delivery and rotation

- Show a requested connection URI or private subscription URL only in the final user-facing delivery, with a bearer-credential warning. Do not repeat it in progress messages or diagnostic output.
- Prefer a protected file or QR artifact when repeated plaintext would increase exposure, but remember that the artifact still contains the credential.
- If exposure is suspected, rotate the underlying node credentials as well as the subscription token. Changing only the URL does not revoke credentials already downloaded.
- Report what class of credential was rotated and which clients must refresh; do not echo the old or new value in the rotation log.
