---
title: Locator/ID Separation Protocol - LISP
category:
- Route/Switch
published: 2019-09-04
author: Brandon James
post_image: /static/images/lisp_overview.png
summary: The Locator/ID Separation Protocol or LISP was originally designed to decrease the size of routing tables on the Internet. As the protocol matured it made it's way into the enterprise[^1] though solutions like Cisco Software Defined Access. In this article I provide a summary of the problem LISP solves and how LISP functions. The purpose of this article isn't to cover the protocol in it's entirety, but to build an awareness of how the protocol works.
---
<iframe src="https://pinecast.com/player/3ba520d4-69f1-4e69-ba83-7750b4dbba54?theme=minimal" seamless height="60" style="border:0" class="pinecast-embed" frameborder="0" width="100%"></iframe>

The Locator/ID Separation Protocol or LISP was originally designed to decrease the size of routing tables on the Internet. As the protocol matured it made it's way into the enterprise[^1] though solutions like Cisco Software Defined Access. In this article I provide a summary of the problem LISP solves and how LISP functions. The purpose of this article isn't to cover the protocol in it's entirety, but to build an awareness of how the protocol works.

# Why LISP Exists

LISP was formally ratified under [RFC 6830](https://tools.ietf.org/html/rfc6830). The following quote from the RFC is the best summary for the problem LISP solves:

>for routing to be efficient, the address must be assigned topologically; for collections of devices to be easily and effectively managed, without the need for renumbering in response to topological change (such as that caused by adding or removing attachment points to the network or by mobility events), the address must explicitly not be tied to the topology.

In a perfect world (at least from the perspective of an Internet router), all IP speaking devices would be distributed uniformly throughout the globe, ISPs would never suffer outages so enterprises wouldn't need to multi-home their internet connections and [RFC 790](https://tools.ietf.org/html/rfc790) would've never existed (37.0.0.0/8 might belong to Texas or Ontario instead of DEC). This would make it trivial for carriers to aggregate routes based on region. 

Unfortunately, this simply isn't how things work. Overtime, ISPs have been forced to disaggregate due to both multi-homing and the increased demand for IP space. This is why we've ended up with over [700,000 routes (and counting)](https://www.cidr-report.org/as2.0/) in Internet routing tables. LISP provides a way to decrease the number of routes on the internet. 

# How it works

LISP separates Location and Identification by replacing IP addresses with RLOCs (Routing Locators) and EIDs (Endpoint Identifiers). RLOCs are assigned to routers based on region so they can be topologically aggregated. EIDs are assigned to endpoints and don't need to be topologically assigned. EIDs are only reachable through the RLOC on the edge of the LISP site where they reside. In contrast with typical IP routing, EID prefixes are not installed in the routing table. Instead LISP uses an EID-to-RLOC database to locate EIDs and deliver packets.

LISP can be thought of as a dynamic tunneling protocol. LISP data plane packets use IP-in-IP encapsulation where the outer IP header contains the source and destination RLOCs and the inner header contains the source and destination EIDs. As the packet enters the tunnel, the Ingress Tunnel Router (ITR) performs the encapsulation and as the packet leaves the tunnel, the Egress Tunnel Router (ETR) performs the decapsulation. XTRs are LISP routers that can perform both functions.

LISP endpoints continue to speak IP exactly like they do today. From the perspective of a LISP router, each endpoint has an EID, but from the perspective of the endpoint itself, it has an IP address. In addition, endpoints only send traffic to EIDs. The general flow for a LISP packet is (1) the endpoint sends a packet destined to an EID, (2) the LISP router receives the packet and looks up the destination EID in the EID-to-RLOC database, (3) the router encapsulates the packet and forwards it to the destination RLOC and (4) the destination router decapsulates the packet and forwards it to the destination endpoint.

[![LISP Overview](/static/images/lisp_overview.png "LISP Overview")](/static/images/lisp_overview.png)

## EID-to-RLOC Resolution

The EID-to-RLOC Mapping service operates similarly to DNS, but instead of domain-to-IP mappings, it provides EID-to-RLOC mappings. The method used to provide mappings in the LISP beta network is called LISP Alternative Logical Topology or LISP+ALT. [RFC 6836](https://tools.ietf.org/html/rfc6836) describes LISP+ALT in detail. There are other standards for LISP databases and all provide a common interface for LISP routers. I'm not going to spend much time discussing the database implementation. Instead, we will focus on the standard interface they provide.

In addition to the definitions found in [RFC 6830](https://tools.ietf.org/html/rfc6830), [RFC 6833](https://tools.ietf.org/html/rfc6833) defines the Map-Server interface and expands on the message types the interface uses. Map-Requests and Map-Replies are the two message types directly used to perform EID-to-RLOC resolution.

### LISP Map-Requests and Map-Replies

Map-Requests are used to request EID-to-RLOC mappings and Map-Replies are used to provide mappings. [RFC 6833](https://tools.ietf.org/html/rfc6833) provides definitions for Map-Resolvers and Map-Servers. Map-Resolvers proxy Map-Requests sent from ITRs and maintain a local EID-to-RLOC database. Map-Servers learn EID-to-RLOC mappings from authoritative ETRs and publish them to their EID-to-RLOC database.

When a Map-Resolver receives a map request and the mapping is in its local database, the resolver will respond with a Map-Reply. If it's not in the database, the resolver may take a couple different actions. If the resolver can determine the EID is non-existent it will respond with a "negative" Map-Reply. Otherwise, it will forward the Map-Request to either an authoritative Map-Server or ETR, which will then respond to the request directly[^2]. 

__Map-Request message format from [RFC 6830](https://tools.ietf.org/html/rfc6830) section 6.1.2__

```
        0                   1                   2                   3
        0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
       |Type=1 |A|M|P|S|p|s|    Reserved     |   IRC   | Record Count  |
       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
       |                         Nonce . . .                           |
       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
       |                         . . . Nonce                           |
       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
       |         Source-EID-AFI        |   Source EID Address  ...     |
       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
       |         ITR-RLOC-AFI 1        |    ITR-RLOC Address 1  ...    |
       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
       |                              ...                              |
       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
       |         ITR-RLOC-AFI n        |    ITR-RLOC Address n  ...    |
       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
     / |   Reserved    | EID mask-len  |        EID-Prefix-AFI         |
   Rec +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
     \ |                       EID-Prefix  ...                         |
       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
       |                   Map-Reply Record  ...                       |
       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

A couple things to note. (1) The Map-Reply Record field. This contains the EID-to-RLOC mapping of the source, so the ETR that receives the Map-Request can update its cache upon receipt. (2) The Record Count field, multiple records may be requested in a single datagram. Additional request fields are simply added one after the other in a single Map-Request packet.

__Map-Reply message format from [RFC 6830](https://tools.ietf.org/html/rfc6830) section 6.1.3__

```
        0                   1                   2                   3
        0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
       |Type=2 |P|E|S|          Reserved               | Record Count  |
       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
       |                         Nonce . . .                           |
       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
       |                         . . . Nonce                           |
   +-> +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |   |                          Record TTL                           |
   |   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   R   | Locator Count | EID mask-len  | ACT |A|      Reserved         |
   e   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   c   | Rsvd  |  Map-Version Number   |       EID-Prefix-AFI          |
   o   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   r   |                          EID-Prefix                           |
   d   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |  /|    Priority   |    Weight     |  M Priority   |   M Weight    |
   | L +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   | o |        Unused Flags     |L|p|R|           Loc-AFI             |
   | c +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |  \|                             Locator                           |
   +-> +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

A couple things to note. (1) Multiple records may be returned for a single Map-Request, the Priority and Weight fields are used by the ITR to determine which RLOC to use. Lower priority is preferred. In the case of a tie, the weight is used to determine how load should be shared between RLOCs. The M Priority and M Weight fields are used for multicast traffic. (2) The Record TTL field determines how long the record may be cached by an ITR or Map-Resolver.

## LISP Packet Formats

__Data Plane__

LISP data plane packets use IP-in-IP encapsulation where the outer-header contains the source and destination RLOCs and the inner-header contains the source and destination EIDs. I. I've copied the IPv4 Data Plane packet format from [RFC 6830](https://tools.ietf.org/html/rfc6830) section 5.1 below.

```
        0                   1                   2                   3
        0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
     / |Version|  IHL  |Type of Service|          Total Length         |
    /  +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |   |         Identification        |Flags|      Fragment Offset    |
   |   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   OH  |  Time to Live | Protocol = 17 |         Header Checksum       |
   |   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |   |                    Source Routing Locator                     |
    \  +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
     \ |                 Destination Routing Locator                   |
       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
     / |       Source Port = xxxx      |       Dest Port = 4341        |
   UDP +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
     \ |           UDP Length          |        UDP Checksum           |
       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   L   |N|L|E|V|I|flags|            Nonce/Map-Version                  |
   I \ +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   S / |                 Instance ID/Locator-Status-Bits               |
   P   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
     / |Version|  IHL  |Type of Service|          Total Length         |
    /  +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |   |         Identification        |Flags|      Fragment Offset    |
   |   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   IH  |  Time to Live |    Protocol   |         Header Checksum       |
   |   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |   |                           Source EID                          |
    \  +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
     \ |                         Destination EID                       |
       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

       IHL = IP-Header-Length
       
```

I'm not going to go into detail on the packet format here, just note that the LISP header is sandwiched between the inner and outer IP headers.

__Control Plane__

The IPv4 control plane packet format from [RFC 6830](https://tools.ietf.org/html/rfc6830) section 6.1 is copied below. Unlike LISP data plane packets, LISP control plane packets are only sent to routable addresses so they do not utilize IP-in-IP tunneling.

```
       0                   1                   2                   3
       0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
       |Version|  IHL  |Type of Service|          Total Length         |
       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
       |         Identification        |Flags|      Fragment Offset    |
       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
       |  Time to Live | Protocol = 17 |         Header Checksum       |
       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
       |                    Source Routing Locator                     |
       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
       |                 Destination Routing Locator                   |
       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
     / |           Source Port         |         Dest Port             |
   UDP +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
     \ |           UDP Length          |        UDP Checksum           |
       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
       |                                                               |
       |                         LISP Message                          |
       |                                                               |
       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

```

Note that the Map-Request and Map-Reply messages from above would be contained in the 'LISP Message' field of this packet.


## Use Cases

### LISP on the Internet

The Internet is the obvious and intended use case for LISP. LISP provides a potential solution to the exponential increase in routes on the internet. As IPv6 adoption increases, so will the size of Internet routing tables. In addition, LISP could potentially extend the life of IPv4 by allowing the use of prefixes longer than /24 without carrier lock-in. 

When writing the LISP standard, the authors distinguished between Provider Independent (PI) and Provider Assigned (PA) addresses. Since PA addresses are assigned to service providers, they can be topologically aggregated. PI addresses on the other hand, might be assigned to a company, university or government and therefore aren't necessarily aggregatable. In the case of the Internet, it would make sense to use PA space for RLOCs and PI space as EIDs.

Interoperability between LISP and non-LISP sites becomes more of an issue when we look at the public internet. [RFC 6832](https://tools.ietf.org/html/rfc6832) discusses three solutions to this problem. I'm not going to discuss any of them in full, but the solutions include proxy-ITRs,  Proxy-ETRs and a form of NAT that substitutes EIDs for routable addresses.

### LISP in the Enterprise

All IP networks are similar, so something useful for the Internet may also be useful for the enterprise. On the surface, this seems less true for LISP than it is for BGP. LISP provides a solution for the exponential growth of routes, but Cisco ASR RP3 route processors can handle up to 8.5 million IPv4 routes[^3]. It's unlikely that many enterprises are close to that and those that are will have the budget to run the latest and greatest hardware. Using LISP to avoid advertising routes into an enterprise core is generally going to add needless complexity.

That being said, LISP provides a way route traffic to specific hosts without the need to advertise host routes. Since LISP has a concept of longest prefix matching, host routes take precedence over less-specific routes to a subnet. This means LISP could be used for endpoint mobility across multiple sites. Note that while an endpoint would keep it's IP address when moving to a new site, LISP does nothing to stretch Layer 2 so it would need to be combined with something like OTV. This solution is rather complicated, so it lends itself well to Software Defined Networking.

LISP is already being used by enterprises that have implemented Cisco SDA[^4]. SDA uses an _enhanced_ version of LISP for Control-Plane traffic, in roughly the way I described above. SDA routers only maintain local routes and use LISP to locate endpoints on the SDA fabric. Cisco uses VXLAN instead of LISP to encapsulate data-plane traffic from endpoints so that Layer 2 headers stay intact. It's possible that other Software Defined Networking solutions use LISP in some way, but I'm not aware of any.

## Glossary of LISP Terms

* __Routing Locators (RLOCs)__ - RLOCs are 32 or 128-bit integers used to describe a location

* __Endpoint Identifiers (EIDs)__ - EIDs are 32 or 128-bit integers used to identify an endpoint

_Note: both RLOCs and EIDs are written using the traditional dotted decimal format we use for IPs_

* __Tunnel Routers (xTR)__ - Encapsulates IP packets leaving LISP sites and decapsulates IP packets entering LISP sites.
	- __Ingress Tunnel Router (ITR)__ - Tunnel Router that performs encapsulation and looks up EID-to-RLOC mappings
	- __Egress Tunnel Router (ETR)__ - Tunnel Router that performs decapsulation and acts as an authoritative source for EID-to-RLOC mappings
* __Map Server__ - Learns authoritative EID-to-RLOC mappings from ETRs and publishes them in a mapping database
* __Map Resolver__ - Resolves Map-Requests from ITRs using a mapping database


[^1]: The creators of LISP noted it's potential use in the enterprise. See Dino Farinacci's talk [here](http://www.youtube.com/watch?v=fxdm-Xouu-k)

[^2]: Details may vary between database implementations, the details here are true for both LISP+ALT and LISP-CONS

[^3]: When configured with 32-GB of memory. Real world capabilities may very based on the router's configuration. See the product sheet [here](https://www.cisco.com/c/en/us/products/collateral/routers/asr-1000-series-aggregation-services-routers/data_sheet_c78-441072.html).

[^4]: This [whitepaper](https://www.cisco.com/c/dam/en/us/solutions/collateral/enterprise-networks/software-defined-access/white-paper-c11-740585.pdf) provides a brief summary on how LISP is used in SDA.