title: A Practical Guide to Multicast using PIM Sparse Mode and Bootstrap Router
category:
- Route/Switch
author: Brandon James
summary: 

Multicast is often a scary word for Network Engineers and I think this is due to the way courses, books and whitepapers teach multicast. It's an older protocol[^1] with lots of weird rules and deployment options. Educators and vendors want to explain multicast in it's entirety, but most people really just need PIM Sparse Mode and BSR. In this article I cover Multicast Addressing, PIM Sparse Mode, Bootstrap Router, Layer 2 Multicast and IGMP Snooping. 


# Multicast Addressing

Multicast Addresses are also referred to as Multicast Groups. [RFC 5771](https://tools.ietf.org/html/rfc5771) defines the best practices for Multicast Group assignments: 


Address Range|Size|Designation|
---|---|---|
224.0.0.0 - 224.0.0.255|/24|Local Network Control Block|
224.0.1.0 - 224.0.1.255|/24|Internetwork Control Block|
224.0.2.0 - 224.0.255.255|65024|AD-HOC Block I
224.1.0.0 - 224.1.255.255|/16|RESERVED
224.2.0.0 - 224.2.255.255|/16|SDP/SAP Block
224.3.0.0 - 224.4.255.255|2 /16s|AD-HOC Block II
224.5.0.0 - 224.255.255.255|251 /16s|RESERVED
225.0.0.0 - 231.255.255.255|7 /8s|RESERVED
232.0.0.0 - 232.255.255.255|/8|Source-Specific Multicast Block
233.0.0.0 - 233.251.255.255|16515072|GLOP Block
233.252.0.0 - 233.255.255.255|/14|AD-HOC Block III
234.0.0.0 - 238.255.255.255|5 /8s|RESERVED
239.0.0.0 - 239.255.255.255|/8|Administratively Scoped Block

I only cover IPv4 in this article, but IPv6 has similar reservations. (RFC 7346)[https://tools.ietf.org/html/rfc7346] is a good starting point for anyone wanting to learn about IPv6 multicast.

(IPv4 Multicast reservations are handled by IANA)[https://www.iana.org/assignments/multicast-addresses/multicast-addresses.xhtml]

## Local Network Control Block (224.0.0.0/24)

Used for things like HSRP, VRRP and OSPF, multicast groups within this space are specifically not routable. This is done for a good reason, the protocols with assignments in this space are typically meant for use within a single broadcast domain and a single device might have multiple instances of one of these protocols. As an example, a L3 switch running HSRP will most likely be running HSRP on all of it's SVIs. If the HSRP multicast group was routable, this could cause a single SVI to become the only active router on the entire switch. 

## Local Internetwork Control Block (224.0.1.0/24)



# PIM Sparse-Mode

# Bootstrap Router

# Layer 2 Multicast

# IGMP Snooping



[^1]: IP Multicast was first standardized in 1986, see [RFC 988](https://tools.ietf.org/html/rfc988)