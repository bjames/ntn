title: Never The Network
published: 2019-11-23
category: 
- unfiled
author: Brandon James
post_image: /static/images/ITBlogAwards_2019_Badge-Finalist-BestNewcomer.png
summary: A month ago I decided to submit NTN to Cisco's IT Blog Awards in the Best Newcomer Category. To my surprise it got selected as a finalist. Since I don't have an about page, I wanted to briefly write about who I am, what NTN is and my plans for the future of NTN. 

[![Finalist](/static/images/ITBlogAwards_2019_Badge-Finalist-BestNewcomer.png "Finalist")](https://www.ciscofeedback.vovici.com/se/705E3ECD18791A68)

About a month ago I decided to submit NTN to Cisco's IT Blog Awards in the Best Newcomer Category. To my surprise it got selected as a finalist. If you'd like to vote for me (or any of the other great candidates), you can do so [here](https://www.ciscofeedback.vovici.com/se/705E3ECD18791A68). Since I don't have an about page, I wanted to briefly write about who I am and what NTN is. 

## Who I am
My name is Brandon James and I am a Network Engineer in Fort Worth, TX. I currently work in the enterprise space and have experience with datacenter and campus routing/switching, wireless and automation. Before I was all in on Networking, I worked for a Managed Services company where, in addition to networking, I worked with virtualization, storage, Windows and Linux servers, along with a bit of desktop support. I'm also a graduate from Texas Tech University where I studied Economics and minored in Computer Science. To this day, I maintain a strong interest in Computer Science which has a direct impact in the way I approach networking topics.

Outside of work, I'm a father of a 3-month old boy, husband, dog owner, trail runner and wannabe landscape/wildlife/family photographer. On top of all that, I also consider NTN one of my hobbies. I only write about topics that I feel like writing about and only when I feel like writing. Admittedly this is something I work on pretty regularly, but many of my articles never see the light of day. 

## NTN

I actually purchased neverthenetwork.com back in 2017, but I didn't really do anything with it other than put together a simple javascript subnet calculator. You can see what the pre-2019 iteration of NTN looked like on [wayback machine](https://web.archive.org/web/20180815153506/https://neverthenetwork.com/). Initially NTN was not going to be a blog, it was only going to feature networking tools, like those found in the [tools section](https://neverthenetwork.com/tools) of the website. This June I started teaching myself [flask](https://palletsprojects.com/p/flask/) and began piecing together some of the tools that I had planned. During this process, I decided to also create [NTN Notes](https://neverthenetwork.com/notes), which is functionally a technical blog. 

I've also recently made the [github project public](https://github.com/bjames/neverthenetwork). If you are interested in how NTN works on the back-end, github is probably the best place to do so. I haven't quite gotten around to writing a detailed readme, but rest assured it is coming. Note NTN is my first flask project, so go easy on me :). 

### NTN Tools
NTN Tools is something I dreamed up during my early networking career, I wanted a way to test access to customers from the internet while connected to their network. The obvious solution is a hotspot on your cell phone or a jumpbox sitting on the internet. While NTN Tools might not be useful to everyone, I think it's fun to use and I consider the subnet calculator to be the best one on the internet. If you click around with NTN tools, note that you can use query strings to build your requests. As long as you have javascript enabled on a modern web browser, the query string is appended to the URL each time you make a request. This means you can send someone a subnet calculator result by sending them a link as follows: `https://neverthenetwork.com/tools/subnet?ip_address=10.0.0.0&subnet_mask=/29`. This works with all the tools. 

In addition I made it look kinda like a terminal window, which might not be the best possible UI, but I really enjoy it.

### NTN Notes
NTN Notes is a technical networking blog and is probably the reason you're here. The things I write about can be broadly categorized into one of the following:

1) Topics I wanted to learn more about - Example: [Locator/ID Separation Protocol - LISP](https://neverthenetwork.com/notes/lisp/)

2) Things I've noticed engineers struggling with - Example: [A Power Users Guide to the Linux CLI](https://neverthenetwork.com/notes/linux_cli/)

This means that if you are wanting to find an introduction to NAT or VLANs, you'll need to look elsewhere. These two categories really define what I'm passionate about. Of course this is very broad, but you can expect to see lots of posts about automation and new networking tech. I tend to think lower level, so I might not write much about something like ACI directly, instead you can expect to read about things like COOP or MP-BGP. Of course this isn't a hard rule, but a general rule based on my interests.

I try to follow basic technical writing guidelines with my posts, but in many ways I'm still learning. If I do something that stands out as bad style, I'd love to hear about it. I also strive for accuracy, I mostly reference RFCs, vendor documentation and notes from people much smarter than me. Of course I'll also give credit to non-trivial insights that aren't my own in the footnotes. 

If there are any questions or comments about NTN, I'd love to hear about them in the discussion forum. At the bottom of each of my posts there is a link to the NTN discord topic about the post. Feel free to correct me, call me names or leave nice comments on any of my posts.

