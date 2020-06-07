---
title: How I Automate - Concurrency
publication_date: 2019-08-01
tags:
- Automation
- Programming
author: Brandon James
static_url: "about"
---
## About
Welcome to NTN!

My name is Brandon James. I am a Network Engineer working in the Data Center space. NTN is my technical blog. It naturally has a bit of a slant towards networking topics, but nothing is really off-limits. In general I try to avoid vendor specific topics. I like to dive deep into RFCs, software engineering and computer science topics. 

## Notes-Core
NTN runs on a custom back-end. In the past I've used ghost and wordpress. Ghost was fairly close to what I was after, but I prefer working with markdown files over using an in-browser editor. Since I know python I decided to go ahead and try building my own back-end. This site is the second iteration of that back-end. Eventually *Notes-Core* (working title) will be open sourced, but it isn't there yet. 

Notes-Core is built on Flask and uses Pandoc (through pypandoc) to render markdown files into HTML. NTNv1 was built using a similar system, but was never designed as a platform. Notes-Core is being built alongside NTNv2, but I'm taking care to build something completely reusable. NTNv1 had other issues, such as an overly complicated front-end and a cluttered UI. I'm taking care to remediate those issues as well. 