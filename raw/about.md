---
title: About
publication_date: 2019-08-01
author: Brandon James
static_url: "about"
---

[<img src="/static/images/me.jpg" style="border-radius:50%; width:300px">](https://www.brandonsjames.com)

Hi! My name is Brandon James. I am a Network Engineer living in Fort Worth, TX. Before I was all in on Networking, I worked for a Managed Services company where I worked with virtualization, storage, networking, Windows servers, Linux servers and did a bit of desktop support. I’m also a graduate of Texas Tech University where I studied Economics and minored in Computer Science. I am also slowly[^1] working towards an MS in CS though Arizona State online. To this day, I maintain a strong interest in Computer Science which has a direct impact in the way I approach networking topics.

Outside of my professional life, I’m a father, husband, dog owner, trail runner and wannabe landscape/wildlife/family photographer. On top of all that, I also consider NTN one of my hobbies. I only write about topics that I feel like writing about and only when I feel like writing. Admittedly this is something I work on pretty regularly, but many of my articles never see the light of day.

# NTN

NTN runs on a custom backend written in Python using the Flask framework. I've released the code under GPLv3, so if you're curious check it out on my [github](https://github.com/ntn). It's recently undergone a partial rewrite to improve reusability, to render markdown files using pandoc[^2] and because I wanted to simplify the UI. 

I decided to write my own backend for a few reasons. 1) I wanted to build public facing server side network tools 2) I prefer using my text editor to write markdown files over using an in-browser editor like the one offered with ghost 3) I wanted to learn Flask and get better at web development. 

On the blog side of NTN you can expect to find technical topics related to computers. I say this because despite the hostname and what I do for a living I'm interest in a wide variety of computing topics. As a consequence of what I do for a living, it is likely that most of my posts will be networking related.

# NTN Tools

NTN Tools was created based on an idea I had during my days working in managed services. If I'm at a customer site, working on their web-facing infrastructure, but my laptop is using their internal DNS and sending requests from inside their network. It would be convenient to perform basic checks via a public facing web service. NTN Tools was written more than 3 years after I left the MSP, but I use it quite a bit and have a backlog of new tools that I'd like to write. 

[^1]: I took my first course in Spring 2020 and plan to take 2 classes per year. Assuming I stick to this plan it will take me 5 years to finish the degree. Which is perfectly fine with me as I'm taking the classes for fun and don't want to overburden myself.
[^2]: NTNv1 rendered markdown using Flask-FlatPages, which wasn't terrible, but I prefer the output I get from pandoc. 