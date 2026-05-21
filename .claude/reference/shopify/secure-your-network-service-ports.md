---
title: Secure your network service ports
source: https://shopify.dev/docs/apps/build/security/secure-network-service-ports
author: []
published: []
created: 2026-05-11
description: You must ensure your app does not expose network services unnecessarily before you submit it to be reviewed by Shopify.
tags: [clippings]
---

To help ensure the security of your app, you must not expose any services publicly that aren't necessary for the functionality of your app. Common services that shouldn't be exposed include MySQL, Redis, Memcached, and Elasticsearch. During the app review process, we identify publicly accessible services by using the security tool Nmap to identify [open ports](https://en.wikipedia.org/wiki/Port_\(computer_networking\)).

If our scan detects unexpected open ports when we review your app, then you'll be notified and asked to re-evaluate whether the services need to be publicly accessible. If the services do need to be publicly accessible, then you'll be given a Google form, where you must explain the following:

- what services are running on the detected open ports
- why each service is necessary to the proper functioning of your application
- why the service must be publicly accessible
- what steps you have taken to ensure that having the service publicly accessible is safe for Shopify merchants and buyers
	If you're unsure how modify a service or your host configuration to make services inaccessible publicly, the following links explain the solution for common hosting providers:
- [Amazon Web Services](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_SecurityGroups.html)
- [Google Cloud Platform](https://cloud.google.com/vpc/docs/firewalls)
- [Microsoft Azure](https://docs.microsoft.com/en-us/azure/virtual-network/network-security-groups-overview)
- [Digital Ocean](https://docs.digitalocean.com/products/networking/firewalls/)

---

---
