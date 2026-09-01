# Retire a Node and Its Resource Graph

Read this file when stopping, deleting, replacing, cleaning up, or proving that a node no longer creates cost. Retirement reconciles the complete scoped resource graph, not only the compute instance.

## Resolve the boundary

Bind the exact provider account/project, regions, node IDs, dependent resources, tailnet objects, authoritative subscriptions, derived client artifacts, and unrelated workloads that must survive.

When the user says “delete everything,” determine whether that means idle remnants, one named node and its dependencies, or every node resource in named accounts and regions. State which live paths will stop working. Do not interpret “all” across unrelated accounts, providers, regions, tailnets, or workloads.

## Pre-delete ledger

Inventory and bind exact IDs before mutation:

- non-terminated instances and attached volumes or disks, including deletion policy;
- allocated public/static addresses and association state;
- detached storage, snapshots, custom images, NAT gateways, load balancers, and provider-specific billable dependencies;
- node-specific security groups/firewalls, key pairs, DNS, certificates, and access objects;
- tailnet device state;
- authoritative subscriptions plus raw links, encoded derivatives, QR artifacts, serving tasks/listeners, and active client databases.

Back up the active client and subscription data needed for rollback. Keep backups outside active serving paths and exclude them from live-reference searches.

## Safe retirement order

1. Drain or mark the old path unavailable when a reversible cutover is possible, and prove the replacement or surviving path first.
2. Release already-disassociated addresses that are proven in scope.
3. Terminate or delete the exact compute resources and wait for the provider's terminal state.
4. Re-inventory; verify the expected attached storage deletion, then remove only authorized detached storage and newly disassociated addresses.
5. Remove authorized dependent firewalls, keys, images, snapshots, DNS, certificates, or hosted endpoints after their dependencies are gone.
6. Remove the retired node from every active subscription variant, proxy group, raw link set, encoded derivative, QR artifact, and client database. Regenerate derivatives from the authoritative source instead of patching them independently.
7. Reload persistent delivery when required and validate the bytes clients actually receive.

Use the provider reference for product-specific rules. For AWS, [providers/aws.md](providers/aws.md) distinguishes Lightsail deletion from EC2 termination, EBS deletion policy, and attached versus detached public-address behavior.

## Zero-residual acceptance

Use the scoped ledger rather than a single success message. Require:

- no in-scope non-terminal compute resource;
- no in-scope billable address, storage, snapshot, image, gateway, or load balancer left unintentionally;
- exact node-specific access objects absent when their removal was authorized;
- no retired node or dangling group reference in active client/subscription data;
- surviving subscription bytes hash-match the authoritative source and pass the target core's validation;
- the surviving real client path still works.

An offline tailnet record is normally a stale control-plane object, not proof that cloud resources still bill. Remove it only when tailnet cleanup is authorized.

## Unexpected cost after deletion

Billing data can lag. Use live inventory to prove current cleanup and label delayed billing observations rather than retrying destructive actions.

Group cost by service and usage type, then compare it with the ledger. Check public-address hours, outbound transfer, detached storage, snapshots/images, NAT/load-balancer hours, taxes, and credits separately. A historical charge can remain after cleanup; the acceptance condition is no current in-scope billable resource, not an instantly zero historical bill.
