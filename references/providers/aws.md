# AWS Node Product and Cost Choice

Read this file with [provision-node.md](../provision-node.md) before creating or replacing an AWS node when product, plan, promotional credits, or cost limits matter. Read the retirement section with [retire-node.md](../retire-node.md) for AWS cleanup. This file contains AWS-specific decisions only; use the shared references for service installation, ports, client delivery, and end-to-end validation.

## Verify live commercial terms

Prices, Free Tier rules, bundle specifications, address charges, transfer allowances, and promotional-credit eligibility can change. Verify them immediately before recommending or creating a resource:

- [Lightsail pricing and current bundles](https://aws.amazon.com/lightsail/pricing/)
- [Lightsail FAQs for billing, transfer, and static IP behavior](https://aws.amazon.com/lightsail/faq/)
- [AWS Free Tier credits](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/free-tier.html)
- [EC2 On-Demand pricing](https://aws.amazon.com/ec2/pricing/on-demand/)

Use the selected Region's terms. Record the source and verification date in the task; do not preserve a price snapshot as an evergreen Skill rule.

## Present the product choice

Resolve only facts that can change the recommendation: target Region, public IPv4 requirement, one lightweight service versus several resident services, expected outbound transfer, and available credit expiry/eligibility when readable through an authorized billing view.

If the user has not selected the AWS product and plan, present two or three mutually exclusive choices and wait for selection before creating a billable resource. Put the recommendation first and explain for each option:

- verified monthly fixed price or capped bundle price;
- memory, storage, and included transfer;
- public IPv4 and stable-address treatment;
- suitable workload and the main limitation;
- what must be deleted or released to stop charges.

Do not repeat this gate after the user explicitly selects a product or plan. Flag a concrete incompatibility before mutation if the selected plan cannot satisfy the stated workload.

For the cheapest simple AWS VPS with public IPv4 and one proxy service, normally recommend the smallest Lightsail Linux IPv4 bundle. Offer the next Lightsail memory tier for multiple resident services or easier maintenance. Offer EC2 only when granular instance families, VPC/IAM integration, architecture selection, or other EC2-specific control matters.

Use this response shape with live-verified values:

> Recommended — Lightsail smallest IPv4 Linux plan: `<price>/month`, `<memory>`, `<disk>`, `<included transfer>`. Lowest predictable total cost for one lightweight node.
>
> More headroom — Lightsail next memory tier: `<price>/month`, `<memory>`, `<disk>`, `<included transfer>`. Better for multiple resident services.
>
> More control — EC2: `<compute + root EBS + public IPv4 fixed cost>/month` before chargeable transfer and tax. Choose for EC2-specific flexibility.
>
> Which one should I create?

Keep the explanation at the user's requested level. Do not expand a small-VPS choice into IAM, agent, API, organization, or enterprise cost architecture.

## Calculate cost and credit coverage

For Lightsail, distinguish the capped bundle from extras. State the selected Region's included outbound allowance. Under current terms, an attached Lightsail static IP has no separate charge, an unattached static IP can bill, and a stopped instance continues accruing plan charges until deletion; verify these terms live before quoting them.

For EC2, calculate at least:

`monthly fixed = hourly instance price * expected hours + root EBS + public IPv4`

List chargeable outbound transfer, snapshots, extra volumes, Elastic IP remnants, NAT gateways, and load balancers separately. For T-family instances, verify CPU-credit mode and explain surplus-credit risk before choosing Unlimited mode.

Estimate usable credit coverage as the lesser of eligible credit divided by verified monthly cost and the time until credit or account-plan expiry. Promotional credit is a payment offset, not automatically a hard cap. Do not promise that AWS cannot charge a payment method unless the current plan and credit terms enforce that outcome. Budget alerts can lag and are notifications, not automatic shutdown.

## AWS-specific provisioning deltas

For Lightsail, select the requested Region, Linux/Unix with an OS-only current distribution, the chosen IPv4-capable bundle, and a static IP when the endpoint must survive stop/start. Keep the static IP attached or delete it. Avoid snapshots, load balancers, extra disks, managed databases, or other resources unless required.

For EC2, verify architecture compatibility, root EBS size/type and `DeleteOnTermination`, CPU-credit mode for T-family instances, public-address requirements, and the exact security group. Avoid NAT gateways, load balancers, additional volumes, snapshots, or Elastic IPs unless required.

After product creation, return to [provision-node.md](../provision-node.md) for protocol, firewall, service, Tailscale, and real-client acceptance. Include the selected product/plan, Region, verified price source/date, address attachment state, and exact cost-ending deletion boundary in the final evidence.

## AWS-specific retirement

- Lightsail: deleting the instance ends its plan charge; stopping it does not. Reconcile static IPs, snapshots, attached disks, load balancers, databases, DNS, and other separately managed resources.
- EC2: verify terminal instance state, root and data-volume deletion policy, detached EBS, Elastic IP allocation, snapshots/images, NAT gateways, and load balancers. Termination does not prove these dependencies are gone.
- Cost Explorer can lag. Use live regional inventory for cleanup acceptance and billing data for attribution, not as a reason to repeat deletion.
