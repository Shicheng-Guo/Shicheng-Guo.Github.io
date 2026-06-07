---
layout: post
title: "How to Get a Free Oracle Cloud Always Free Virtual Machine (2026 Guide)"
author: Shicheng Guo
date: 2026-06-06
categories: tutorials
tags: oracle-cloud cloud free-tier vm devops linux
---

Want a real virtual server that runs 24/7 and costs nothing — not for a 12-month trial, but indefinitely? Oracle Cloud's **Always Free** tier is one of the few offers that genuinely delivers this. In this guide, you'll set one up from scratch: account, network, VM, and the guardrails that keep it free forever.

## Why Oracle Cloud Free Tier?

Among the major cloud providers, Oracle Cloud offers one of the most generous free tiers available today:

- Up to **2 AMD micro VMs** (`VM.Standard.E2.1.Micro`)
- **Ampere A1 (ARM)** instances — up to 4 OCPUs and 24 GB RAM, capacity permitting
- **200 GB** of block storage
- A **public IPv4 address**
- A choice of **Linux** operating systems
- **No automatic expiration** for Always Free resources

That combination makes Oracle Cloud an excellent home for personal websites, APIs, AI agents, Docker containers, cron jobs, and full development environments — without a recurring bill.

> **Always Free vs. Free Trial:** New accounts also get a 30-day, US$300 trial credit. Anything labeled **"Always Free"** stays free after the trial ends. The rest of this guide sticks to Always Free–eligible resources.

## Step 1 — Create an Oracle Cloud Account

1. Visit [oracle.com/cloud/free](https://www.oracle.com/cloud/free/).
2. Sign up with a valid email address.
3. Complete phone verification.
4. Add a credit card for identity verification — Always Free resources won't be charged.
5. **Choose your Home Region carefully.**

> ⚠️ **Home Region is permanent.** Always Free compute is tied to your tenancy's Home Region and can't be changed later. Pick the region closest to you or your users.

## Step 2 — Create a VCN (Virtual Cloud Network)

Before creating a VM, you need a network for it to live in.

1. Open the **Oracle Cloud Console**.
2. Go to **Networking → Virtual Cloud Networks**.
3. Click **Start VCN Wizard → Create VCN with Internet Connectivity**.

Suggested values:

| Setting | Value |
|---|---|
| VCN CIDR | `10.0.0.0/16` |
| Public Subnet | `10.0.0.0/24` |
| Private Subnet | `10.0.1.0/24` |
| IPv6 | Disabled |
| DNS Hostnames | Enabled |

The wizard automatically provisions a public subnet, a private subnet, an Internet Gateway, a NAT Gateway, and a Service Gateway.

## Step 3 — Create an Always Free VM

Navigate to **Compute → Instances → Create Instance**.

**Basic information** — give it a memorable name, e.g. `free-a1-server`.

**Shape** — open *Change Shape* and pick one:

- **Preferred:** `VM.Standard.A1.Flex` (ARM Ampere — far more powerful)
- **Fallback:** `VM.Standard.E2.1.Micro` (AMD — always available)

For an A1.Flex instance, **1 OCPU / 6 GB RAM** is a safe Always Free starting point (the cap is 4 OCPUs / 24 GB total across all A1 instances).

**Image** — choose a Linux image such as Oracle Linux 9 or Ubuntu LTS (22.04 / 24.04).

## Step 4 — Configure Networking

In the networking section of the create form:

- Select **Existing VCN** (the one from Step 2)
- Select the **existing public subnet**
- **Automatically assign a public IPv4 address** ✅
- Leave IPv6 disabled

**SSH keys** — upload your own public key (`.pub`) *or* let Oracle generate a key pair.

> 🔑 If Oracle generates the key, **download the private key immediately** — you can't retrieve it later. Store it somewhere safe.

## Step 5 — Configure Storage

- **Boot volume:** 47–50 GB
- **Performance:** Balanced (10 VPU)
- **No** additional block volumes
- **No** backup policy

This keeps you comfortably inside the 200 GB Always Free storage allowance.

## Step 6 — Launch the Instance

Click **Create** and wait for the state to turn green (**Running**).

If you see *"Out of capacity for shape VM.Standard.A1.Flex"*, don't worry — this is a **capacity** message, not a billing problem. Try:

- A **different Availability Domain** in your region
- A **smaller** A1 configuration (e.g. 1 OCPU instead of 4)
- **Retrying later** — capacity frees up frequently

If A1 stays unavailable, fall back to `VM.Standard.E2.1.Micro`, which is essentially always free and available.

## Step 7 — Connect via SSH

Grab the **Public IP** from the instance details page, then connect with your private key.

**Oracle Linux** (default user `opc`):

```bash
ssh -i id_rsa opc@<PUBLIC_IP>
```

**Ubuntu** (default user `ubuntu`):

```bash
ssh -i id_rsa ubuntu@<PUBLIC_IP>
```

Example:

```bash
ssh -i id_rsa opc@129.146.255.135
```

> If you get a *"permissions too open"* error, tighten the key file: `chmod 600 id_rsa`.

## Step 8 — Create a Budget Alert

This is your safety net against accidental charges.

Go to **Billing & Cost Management → Budgets → Create Budget**:

- **Budget amount:** US$1 / month
- **Alert thresholds:** 50%, 80%, 100%

You'll get an email the moment any paid resource sneaks in.

## Step 9 — Verify Free Tier Usage

Go to **Storage → Boot Volumes** and:

- **Delete** boot volumes left behind by terminated instances (they still count against your quota)
- **Keep** your active VM's boot volume
- Confirm total storage stays **under 200 GB**

## Recommended Always-Free Setup

For a rock-solid, never-expires configuration:

- **Shape:** `VM.Standard.E2.1.Micro` (or `A1.Flex` if available)
- **OS:** Oracle Linux 9
- **Boot volume:** ~47 GB
- **Public IPv4** address
- **Monthly budget alert** at $1

This setup can run indefinitely at no cost while comfortably hosting static and dynamic websites, REST APIs, Docker containers, Python services, AI agents, and personal dev environments.

## Final Thoughts

Oracle Cloud's Always Free tier remains one of the best long-term free cloud offers around. The A1 ARM instances in particular punch well above their weight — when you can get capacity. Set up the budget alert, keep an eye on your storage, and you've got a capable always-on server for the price of a credit-card verification.

Happy hosting. 🚀
