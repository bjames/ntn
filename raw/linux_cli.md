---
title: A Power User's Guide to the Linux CLI
tags:
- Cheatsheets
- Linux
publication_date: 2019-10-10
author: Brandon James
---

# A Power User's Guide to the Linux CLI

I am a huge fan of Linux[^1]. In the office most of my real work happens through a Red Hat jumpbox, this website is hosted on Ubuntu and I've been using Linux on my personal machines since 2010[^2]. At first, I was using Linux because I'm a nerd and that's what we do, but I continue to use it because it increase my productivity. 

This document is meant to be act as a Linux CLI reference. I plan on expanding the document as I have time and hope it ends up being a complete reference for Linux power users.

<H1> Index </H1>

[TOC]

## The Unix Philosophy

Linux falls under the "Unix-like" class of operating systems, all of these operating systems follow something known as the Unix Philosophy. The Unix Philosophy has a long and somewhat storied history that you can read about in the first Chapter of [*The Art of Unix Programming* by Eric Steven Raymond](http://www.catb.org/~esr/writings/taoup/html/ch01s06.html). While the book is geared towards programmers, understanding the Unix philosophy is sure to make you a better user of Linux as well.

I think of the following quote from [Doug McIlroy](https://archive.org/details/bstj57-6-1899/page/n3) when I think of the Unix Philosophy:

i) Make each program do one thing well. To do a new job, build afresh rather than complicate old programs by adding new features.

ii) Expect the output of every program to become the input to another, as yet unknown, program. Don't clutter output with extraneous information. Avoid stringently columnar or binary input formats. Don't insist on interactive input.

iii) Design and build software, even operating systems, to be tried early, ideally within weeks. Don't hesitate to throw away the clumsy parts and rebuild them.

iv) Use tools in preference to unskilled help to lighten a programming task, even if you have to detour to build the tools and expect to throw some of them out after you've finished using them.

As a Linux user, it's important to keep the first two in mind. Realizing that the Linux CLI consists of a collection of small programs that can act as input to each other and all follow a similar output format is the first step to Linux mastery. If you search for 'bash one-liners' you will find long strings of text that can be difficult to decipher. Once you realize that you are actually looking at multiple commands being chained together you can (usually) make sense of how the 'one-liner' works. 

## Defining the Linux CLI

Since Linux can vary from distribution to distribution, I think it's important to define what I'm talking about when I say "the Linux CLI". The Linux CLI consists of a POSIX compliant shell and a set of text-based utilities. There are certain utilities you can expect to be available by default, but we don't really have a standard for this[^3]. Unless otherwise noted, any programs or commands that I mention should be available by default on most Linux distributions, but I'd be hesitant to guarantee that they'll be available on _all_ Linux distributions. 

__Note:__ In this document I will use the terms __Linux CLI__, __bash__ and __shell__ interchangeably. If there is a standard Linux shell, it's bash, but some Linux distributions do ship with alternative shells such as ksh, fish or zsh.

## Man Pages

Most Linux CLI commands and programs have listings in the system manual. To view a man page, simply type `man <command>` where command is the name of the command or program you want to know more about. The `man` program itself even has a man page, type `man man` to try it out. If for some reason you can't find the `man` page you are looking for you can use `man -k <keyword>` to get a list of `man` pages containing a specific keyword. You can also perform a basic search within a man page by typing `/<keyword>` and then using `n` to jump to the next result or `N` to jump to the previous result. For more advance searches, you can pipe `man` into [`grep -n`].

In addition to being a quick way to view manual entries, the `man` program belongs to a class of CLI programs called [pagers](#pagers). Pagers give you a way to view the entire contents of a file without the need for a scrollbar. With `man` you can move up and down with `j` and `k`, skip forward a screenful with the spacebar or jump to a specific line number by typing it and pressing enter. 

As you read this guide, I encourage you to skim the man pages for the utilities I mention. 

__Note:__ Man pages are so effective that I rarely need to turn to the web for my Linux CLI questions. I actually considered stopping after writing this section because the man pages explain everything _far_ better than I can.  

## Navigation

File navigation is one of the places new CLI users get hung up, but once you get the basics, it really is quicker and easier than managing files with a GUI.

* A few notes on the Linux directory layout.

	i) The root of the Linux filesystem is `/` or the root directory (not to be confused with the root user). This is not quite the same as being in the root of the C:\\ drive on a Windows machine. In Linux, all drives are mounted under the root filesystem. 

	ii) All users have a home directory, it traditionally resides under `/home/<username>`. The `~` symbol refers to the current users home directory.

	iii) Files and folders can be referenced by either absolute or relative paths. 
	 	
	 * An absolute path is when you refer to the file or folder by it's full path starting at the root directory. As an example, if you have a folder called 'scripts' in your home directory the absolute path to a script within that directory is `/home/bjames/scripts/update_files.sh`. 
	 
	 * There a couple ways to refer to a file or folder by relative paths
	 
	 	1) Referencing the file or folder without a preceding `/` uses your current working directory as the base directory. Using the script above, the relative path from your home directory would be `scripts/update_files.sh`

     	2) Linux provides two useful shortcuts for relative paths 
     	
      	* When within a folder, you can refer to the folder as `.`. Again, from our home folder `./scripts/update_files.sh` or from the scripts folder `./update_files.sh` are both relative paths to the update_files.sh script.

	  	* `..` refers to the parent directory. As an example, let's say the absolute path of your working directory is the scripts folder from above, `/home/bjames/scripts/`. If you needed to access notes.txt stored in your home directory, you could do so with the following relative path: `../notes.txt`. Note that you can use `..` multiple times in a single path. For instance `../../` refers to `/home/`.

* `ls` Lists the contents of the current directory. It can be combined with arguments like `ls -l` to format the output as a list, `ls -a` to include hidden files in the output or `ls -h` to print the file size in a human readable format. Arguments can also be stacked, for example `ls -lah` formats the output as a list, includes hidden files and uses human readable file sizes. Many Linux flavors [alias](#command-aliases-bash-functions-and-.bashrc) `ls -lah` to `ll`, which means running the command `ll` actually runs `ls -lah`. 
```
[bjames@lwks1 Documents]$ ls -lah
total 183M
drwxr-xr-x.  8 bjames bjames 4.0K Sep  8 17:24  .
drwx------. 36 bjames bjames 4.0K Sep  8 17:23  ..
drwxrwxr-x.  2 bjames bjames 4.0K Jul 12 13:51  ACI
-rw-------.  1 bjames bjames 230K Sep  7 00:10 'LISP - edit.aup'
drwxrwxr-x.  3 bjames bjames 4.0K Sep  4 21:20 'LISP - edit_data'
-rw-rw-r--.  1 bjames bjames  12M Sep  4 23:42  LISP.mp3
drwxrwxr-x. 12 bjames bjames 4.0K Aug 18 16:27  notes
-rw-rw-r--.  1 bjames bjames  53M Sep  5 15:45  output2.mkv
-rw-rw-r--.  1 bjames bjames 118M Sep  5 15:41  output.mkv
-rw-rw-r--.  1 bjames bjames 108K Jul 12 16:36  UA_TRAILRUN_50K_TRAINING_PLAN_2018.pdf
drwxrwxr-x.  6 bjames bjames 4.0K Jul 12 10:57  Zoom
```

* `pwd` Prints the path of the current working directory
```
[bjames@lwks1 Documents]$ pwd
/home/bjames/Documents
```

* `cd` Changes the working directory. `cd ~` or just `cd` by itself takes you to your home directory. You can `cd` using absolute paths `cd /var/log/`. You can also `cd` using relative paths `cd scripts` takes you to scripts or `cd ../notes` takes you to the sibling folder `notes`. 

That covers the basics of navigating on the Linux CLI. Here's an example putting it all together. 

i) We start out in my home directory, which contains 12 folders and no files.
```
[bjames@lwks1 ~]$ pwd
/home/bjames  
[bjames@lwks1 ~]$ ls
Desktop    Downloads  Pictures  Public  Templates  Videos
Documents  Music      Projects  snap    tmp
```

ii) From there we `cd` to my Projects folder using a relative path 
```
[bjames@lwks1 ~]$ cd Projects/
[bjames@lwks1 Projects]$ ls
neverthenetwork
```
iii) If we want to go to my Videos folder, we can do so in a few ways. Three are shown below:

* Returning to the parent folder and then navigating to the Video folder, both using relative paths.

```
[bjames@lwks1 Projects]$ pwd
/home/bjames/Projects
[bjames@lwks1 Projects]$ cd ..
[bjames@lwks1 ~]$ cd Videos/
[bjames@lwks1 Videos]$ pwd
/home/bjames/Videos
``` 

* The absolute path

```
[bjames@lwks1 Projects]$ cd /home/bjames/Videos/
[bjames@lwks1 Videos]$ pwd
/home/bjames/Videos 
```

* A single relative path

```
[bjames@lwks1 Projects]$ cd ../Videos/
[bjames@lwks1 Videos]$ pwd
/home/bjames/Videos
```

## Pagers

If you've read many linux guides, you've probably seen someone use `cat file.txt` to print the content of a file to the screen. This does work, but there is a much better solution. `more` and `less` both belong to a class of programs known as pagers. Pagers work by breaking files into pages or screenfuls of data so you don't need to scroll back up to see the rest of your file. The two programs operate similarly, but do have a few differences. 

* `less` - Operates similarly to `vi` and allows forward and backward movement through the file. The output of the file is not copied to your scrollback buffer[^4]. 
	* Basic navigation `[space]` - Move forward one screenful, `j` move forward one line, `k` move backward one line, `q` quit
	* The pager used by `man` operates similarly to less
	* `less file.txt`
* `more` - Much simpler than `less`
	* Basic navigation [space] - Move forward one screenful
	* `more file.txt`
	
Read the man pages (`man less` and `man more`) for *more* on both of these. 

## Searching with grep, locate and which

### grep

`grep` is used to find strings matching a pattern within a file. In the most basic case, you might use `grep` to search for a specific string within a file:

```
[bjames@lwks1 pages]$ grep "specific string" linux_cli.md
Grep is used to find strings matching a pattern within a file. In the most basic case, you might use grep to search for a specific string within a file:
```

However, the real power of `grep` lies in regular expressions. Current versions of `grep` support three *flavors* of regex. They are standard `grep` regex, extended `grep` regex and perl regex. I find myself using extended `grep` for most things. In the below example, we use extended regular expressions to find IP addresses within this markdown file. 

```
[bjames@lwks1 pages]$ grep -noE '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}' linux_cli.md
193:172.16.12.1
194:172.16.12.127
194:172.16.12.130
<redacted for breavity>
833:104.27.130.254
835:104.27.131.254
876:192.168.88.1
```

__Note:__ in the above output, I also included the `-n` argument, this tells `grep` to print the line number the match was found on. I also used the `-o` argument, which tells grep we want only the matching part of the line. Also note the regex above won't only find valid IPs, for instance 999.999.999.999 is not a valid IP, but would be considered a match. The regex to only match valid IPs is significantly more complicated. When using `grep` it's generally best to use regex that's good enough to find what you are looking for.

In addition to searching a single file, `grep` can be used to search multiple files using either a wildcard such as `grep <pattern> *.log`, a single directory `grep <pattern> ~/logs/` or a directory and it's subdirectories `grep -r <pattern> ~/logs/` (here the `-r` argument stands for recursive). 

```
[bjames@lwks1 pages]$ grep -Eo '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}' *.md
automation_concurrency.md:192.168.1.100
automation_concurrency.md:192.168.10.0
<redacted for brevity>
wlc_cli.md:192.168.0.20
wlc_cli.md:192.168.1.20
```

__Note:__ Above we found every IP address, subnet mask or wildcard mask used in any NTN article. 

`grep` can also be used with [pipes](#redirection-operators) to search the output of another file `<command> | grep <pattern>`

```
[bjames@lwks1 pages]$ ls -lah | grep linux
-rw-rw-r--.  1 bjames bjames  23K Sep 24 23:46 linux_cli.md
```

#### My most used `grep` arguments

`-E` use extended regular expressions.

`-v` inverse matching, prints all lines that don't match the pattern

`-o` only output the matching string

`-r` recursively search sub-directories

`-n` print the line number the match occurred on

`-i` case insensitive search

`-I` ignore binary files

`-B [n]` print __n__ lines of context before the match

`-A [n]` print __n__ lines of context after the match 

`grep` has tons of options and can be used for finding just about anything you'd need to find. I *highly* recommend reading `man grep` as the need arises. 

### locate

`locate` is used to find files based on their names. It can be used with either basic wildcards or regular expressions. 

```
[bjames@lwks1 pages]$ locate -i *run*.pdf
/home/bjames/Documents/UA_TRAILRUN_50K_TRAINING_PLAN_2018.pdf
```

__Note:__ The `-i` argument tells locate to perform a case-insensitive search

This is useful if I remember all or part of the name of a file, but don't remember where it was saved. 

### which

`which` returns the path of a shell command. This is especially useful for user installed programs and aliases. 

```
[bjames@lwks1 pages]$ which ll
alias ll='ls -l --color=auto'
	/usr/bin/ls
```

## SSH

Linux has a built in SSH client, called OpenSSH[^5]. Basic usage is very simple.
```
[bjames@lwks1 ~]$ ssh labtoolbox
bjames@labtoolbox's password: 
bjames@labtoolbox:~$ 
```
You can also specify a username
```
[bjames@lwks1 ~]$ ssh root@labtoolbox
root@labtoolbox's password: 
root@labtoolbox:~$ 
```
__Usability Tip__ most Linux distributions ship with a program called bash-completion installed. If it's installed you can use tab-completion to fill in the hostname based on your known-hosts and ssh-config files. If there are multiple matches it will print out a list of matching hosts. This can be useful if you are having trouble remembering an IP or hostname. 

```
[bjames@lwks1 ~]$ ssh 172.16.12.1
172.16.12.127  172.16.12.130  172.16.12.132  172.16.12.137  
```
### Logging SSH Sessions

As network engineers we often need to log our ssh sessions to a file. This can be done using the `tee` program as follows.

```
[bjames@lwks1 ~]$ ssh 172.16.12.127 | tee logfile.log
```

This is a good time to introduce the concept of `|` or pipes. `ssh` and `tee` are two seperate programs. Linux CLI programs such as `ssh` often read from standard input (commonly called stdin) write to standard output (commonly called stdout). When using a terminal emulator, stdout is printed on the terminal and stdin is input to the terminal. `|` is one of the redirection operators in Linux. In this case, we are redirecting the output of `ssh` to the input of `tee` which in turn writes to logfile.log. For more details, read the section titled [IO Redirection](#io-redirection).

__Note:__`ssh`, `tee` and output redirection are examples of the first two points of the Unix Philosophy at the top of this page. `ssh` and `tee` are both small programs that do one thing well.  In addition, we've made the output of `ssh` the input of `tee`. Redirection is an important part of effective CLI use.

### The Known Hosts File
The first time you log into a device you'll be prompted to add it's RSA key to the known hosts file.
```
[bjames@lwks1 ~]$ ssh 192.168.88.1
The authenticity of host '192.168.88.1 (192.168.88.1)' can't be established.
RSA key fingerprint is SHA256:tXxQqN842Uoe/35JLTOOllo5liFu3qOERiid54iIW1Y.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '192.168.88.1' (RSA) to the list of known hosts.
bjames@192.168.88.1's password: 
```
If the key changes, you'll be presented with an error message.
```
[bjames@lwks1 ~]$ ssh 192.168.88.1
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@    WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!     @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
IT IS POSSIBLE THAT SOMEONE IS DOING SOMETHING NASTY!
Someone could be eavesdropping on you right now (man-in-the-middle attack)!
It is also possible that a host key has just been changed.
The fingerprint for the RSA key sent by the remote host is
SHA256:HrknWcZ9j3/gt8TY7iqtsOXgJgEypFzuDD8Mydi5y1o.
Please contact your system administrator.
Add correct host key in /home/bjames/.ssh/known_hosts to get rid of this message.
Offending RSA key in /home/bjames/.ssh/known_hosts:10
RSA host key for 192.168.88.1 has changed and you have requested strict checking.
Host key verification failed.
```
This can be fixed by manually deleting the key from the known_hosts file or you can use `ssh-keygen -R <hostname>` to remove the key from the file.
```
[bjames@lwks1 ~]$ ssh-keygen -R 192.168.88.1
# Host 192.168.88.1 found: line 10
/home/bjames/.ssh/known_hosts updated.
Original contents retained as /home/bjames/.ssh/known_hosts.old
```
### SSH Configuration File

The SSH configuration file is used to control how your system connects to other systems via SSH. There are actually multiple SSH configuration files on most systems. Commonly, `/etc/ssh/ssh_config` will contain some basic system-wide configuration as well as example configuration that has been commented out. On modern systems, your system-wide SSH configuration will include any `.conf` file in `/etc/ssh/ssh_config.d/`. In addition to the system-wide configuration files, each user can have a configuration file under `~/.ssh/config`. In general I've found it best to edit user configuration files first and system-wide configuration files only when necessary.

The SSH Configuration file has a simple syntax. 

```
# This is a line comment

Host <hostname, IP or pattern>
	# any number of options can be listed here
	Cipher aes128-ctr
# Use ssh-keys for all other hosts
Host *
	IdentityFile ~/.ssh/id_rsa
```

__Note:__ The SSH Configuration file has it's own man page, you can read it with `man ssh_config`

### SSH Arguments

Many of the options you configure in the SSH Configuration file have equivalent arguments. The one I use most frequently is `ssh -c <cipher> <hostname>` when connecting to older devices that don't use modern SSH ciphers.

```
[bjames@lwks1 ~]$ ssh oldhost1
Unable to negotiate with oldhost1 port 22: no matching cipher found. Their offer: aes128-cbc,3des-cbc,aes192-cbc,aes256-cbc
[bjames@lwks1 ~]$ ssh -c aes256-cbc oldhost1
```

For more SSH arguments read `man ssh`

### SSH Keys

SSH can use public key authentication instead of password authentication. As long as your keys are managed correctly, this is both more convenient and secure than password authentication. To use key based authentication, you must first generate a private key. 

```
[bjames@lwks1 ~]$ ssh-keygen 
Generating public/private rsa key pair.
Enter file in which to save the key (/home/bjames/.ssh/id_rsa): test_key
Enter passphrase (empty for no passphrase): 
Enter same passphrase again: 
Passphrases do not match.  Try again.
Enter passphrase (empty for no passphrase): 
Enter same passphrase again: 
Your identification has been saved in test_key.
Your public key has been saved in test_key.pub.
The key fingerprint is:
SHA256:F/hmGkdfO1F+S1fm8cVtJAKHiI7sOQFpAEONwvZjZ5Y bjames@lwks1
The key's randomart image is:
+---[RSA 3072]----+
|Boo.   . ..oo .+B|
|.=+.  . .... . *O|
|o..o o. . o   oo*|
|   ++E.  o o ..o+|
|  ..=o  S * . o. |
|    +    B     . |
|     .  .        |
|                 |
|                 |
+----[SHA256]-----+
```

__Note:__ I strongly recommend setting a passphrase, especially in a shared environment. If you can't be bothered to type your passphrase more than once per session, you can use `ssh-agent` to store the passphrase. 

`ssh-keygen` generates two files `<key_name>` and `<key_name>.pub`. Once you've generated an SSH key pair, you need to copy the public key, `<key_name>.pub` to the systems you need to authenticate against. 

__Note:__ In practice, you'll probably want to use default of `~/.ssh/id_rsa`

```
[bjames@lwks1 ~]$ ssh-copy-id -i test_key.pub test.neverthenetwork.com
/usr/bin/ssh-copy-id: INFO: Source of key(s) to be installed: "test_key.pub"
/usr/bin/ssh-copy-id: INFO: attempting to log in with the new key(s), to filter out any that are already installed
/usr/bin/ssh-copy-id: INFO: 1 key(s) remain to be installed -- if you are prompted now it is to install the new keys
bjames@test.neverthenetwork.com's password: 

Number of key(s) added: 1

Now try logging into the machine, with:   "ssh 'test.neverthenetwork.com'"
and check to make sure that only the key(s) you wanted were added.
```

This program works by copying your `<key_name>.pub` to `~/.ssh/authorized_keys`. Which can be done manually from systems that don't have `ssh-copy-id` installed. In addition, this might not work on non-unix-like systems. In which case you'll need to copy the contents of `<key_name>.pub` to the authorized key store manually. 

Once the key has been copied, you can log in to the remote system by specifying the identity file using `ssh -i` or by modifying your ssh configuration to always use a specific identity file for one or every host. 

```
[bjames@lwks1 ~]$ ssh -i test_key test.neverthenetwork.com 
Enter passphrase for key 'test_key': 
Welcome to Ubuntu 18.04.2 LTS (GNU/Linux 4.15.0-55-generic x86_64)

bjames@test:~$ 
```

__Note:__ There are several methods to maintain a list of authorized SSH keys across all your systems. One common method is to include an `authorized_keys` file in a configuration management system. There are also centralized methods such as storing the keys in LDAP. 

#### SSH Agent

I'm only going to cover the absolute basic use of `ssh-agent` for more information consult `man ssh-agent`. `ssh-agent` can be used to store ssh keys and is especially useful in the case of ssh keys using passphrases. To use `ssh-agent`, it first needs to be started. 

```
[bjames@lwks1 ~]$ eval `ssh-agent`
Agent pid 21285
```

You probably noticed the use of the `eval` command. `eval` takes input from a file or stdin and evaluates it as if it was entered on the CLI. In this case, calling `ssh-agent` by itself would've resulted in the following output to stdout. 

```
[bjames@lwks1 ~]$ ssh-agent
SSH_AUTH_SOCK=/tmp/ssh-k4tysoOInoQM/agent.21285; export SSH_AUTH_SOCK;
SSH_AGENT_PID=21285; export SSH_AGENT_PID;
echo Agent pid 21285;
```

These are bash commands that create new [environment variables](#environment-variables) called `SSH_AUTH_SOCK` and `SSH_AGENT_PID` and then prints them to the screen. `eval` causes these bash commands to be run in the current shell.

Once our `ssh-agent` is running, we can use `ssh-add` to add keys to the `ssh-agent`. By default it tries to add `~./ssh/id_rsa`, but you can specify a key using `ssh-add <key_name>`. Once that's been done you can use the identity file without being prompted for the passphrase.

```
[bjames@lwks1 ~]$ ssh-add test_key
Enter passphrase for test_key: 
Identity added: test_key (bjames@lwks1)
[bjames@lwks1 ~]$ ssh -i test_key goaccess.neverthenetwork.com 
Welcome to Ubuntu 18.04.2 LTS (GNU/Linux 4.15.0-55-generic x86_64)

bjames@goaccess:~$ 
```

__Note:__ This also works with identity files that have been specified using the ssh configuration file

## Vim

`vim` is commonly the default CLI text editor on linux distributions. This means that you need to know how to edit files using vim. But don't fret, even if you only know the basics, `vim` can be a joy to use. I've never bothered to learn any of `vim`'s advanced features and tend to use VSCode for development and making large edits, but I still really enjoy using `vim` and it's keyboard centric interface for edits from the terminal.

`vim` has a several modes, but here I'm going to cover the *basics* of __normal__ and __insert__. For more information I recommend `man vim` or `vimtutor`, which launches a fantastic interactive guide to `vim`.

### Normal Mode Commands
`j` move the cursor down

`k` move the cursor up

`l` move the cursor right

`h` move the cursor left

`.` repeat the last insert

`i` switch to insert mode at the current cursor location

`I` switch to insert mode at the beginning of the current line

`a` switch to insert mode in the position following the cursor

`A` switch to insert mode at the end of the line

`:w` save the file

`:wq` or `:x`save the file and quit

`:q` quit

`:q!` quit ignoring prompts about the file not being saved

### Insert Mode
`ESC` switch to Normal Mode

## Job Management

Linux provides a set of utilities and commands to help you handle multiple process within a single CLI session. 

### Finding Jobs and Processes

To view jobs running in your current session use the `jobs` command

```
[bjames@lwks1 ~]$ jobs
[1]   Running                 ping -q 8.8.8.8 &
[2]   Running                 ping 4.2.2.2 > ping.out &
[3]+  Stopped                 man bash
[4]-  Running                 sudo tcpdump -w out.pcap &
```

To view processes running under the current user and, use `ps ux`

```
[bjames@lwks1 ~]$ ps ux
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
bjames    2297  0.0  0.0  20556 10668 ?        Ss   19:32   0:00 /usr/lib/system
<redacted for brevity>
bjames   16593  0.0  0.0 226752  3608 pts/0    R+   21:44   0:00 ps ux
```

To view all processes on the system, use `ps aux`

```
[bjames@lwks1 ~]$ ps aux
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root         1  0.0  0.0 171856 14844 ?        Ss   19:31   0:03 /usr/lib/system
<redacted for brevity>
bjames   16763  0.0  0.0 226752  3604 pts/0    R+   21:45   0:00 ps aux
```

__Note:__ `ps` has tons of options, but `ps aux` and `ps ux` tend to provide the most useful information, especially when combined with [`grep`](#grep). `a` tells `ps` to include all users in the output, `u` tells `ps` to format the output as seen above and `x` tells `ps` to include processes that aren't assigned to a tty. Refer to `man ps` for more information

`top` gives you a list of processes sorted by resource use

```
[bjames@lwks1 ~]$ top

top - 21:53:12 up  2:21,  1 user,  load average: 0.26, 0.37, 0.39
Tasks: 369 total,   1 running, 365 sleeping,   3 stopped,   0 zombie
%Cpu(s):  0.7 us,  0.4 sy,  0.0 ni, 98.8 id,  0.0 wa,  0.1 hi,  0.0 si,  0.0 st
MiB Mem :  64430.3 total,  59678.8 free,   2847.9 used,   1903.7 buff/cache
MiB Swap:  32280.0 total,  32280.0 free,      0.0 used.  60759.1 avail Mem 

  PID USER      PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND    
 2343 bjames    20   0 1739572 106636  81552 S   3.0   0.2   1:56.88 Xorg       
 2584 bjames    20   0 4790964 227384 113140 S   2.7   0.3   1:44.76 gnome-she+ 
13769 bjames    20   0  674600  65880  40592 S   2.0   0.1   0:04.11 terminator 
```

__Note:__ By default, `top` sorts by CPU utilization. Pressing `f` brings up a menu that allows you to select a different column to sort by. 

### Stopping Jobs and Processes

To end the current job, press `CTRL+C`. This sends SIGINT[^6] to the current process. SIGINT asks the process to gracefully shutdown. There may be instances where this doesn't work, but in general it will end the process in the foreground.

```
[bjames@lwks1 neverthenetwork]$ ping 8.8.8.8
PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=54 time=9.08 ms
64 bytes from 8.8.8.8: icmp_seq=2 ttl=54 time=8.97 ms
64 bytes from 8.8.8.8: icmp_seq=3 ttl=54 time=10.3 ms
64 bytes from 8.8.8.8: icmp_seq=4 ttl=54 time=9.02 ms
^C
--- 8.8.8.8 ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 7ms
rtt min/avg/max/mdev = 8.971/9.329/10.250/0.537 ms
```

When `CTRL+C` doesn't work, `CTRL+Z` can be used as a workaround. This sends `SIGTSTP`, which tells the terminal to stop the current process. From there, you can kill the process, send it to the background or bring it back to the foreground.

Let's pretend that `ping` isn't listening to `CTRL+C`

```
[bjames@lwks1 neverthenetwork]$ ping 8.8.8.8
PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=54 time=9.41 ms
64 bytes from 8.8.8.8: icmp_seq=2 ttl=54 time=9.61 ms
64 bytes from 8.8.8.8: icmp_seq=3 ttl=54 time=8.87 ms
64 bytes from 8.8.8.8: icmp_seq=4 ttl=54 time=8.91 ms
^Z
[1]+  Stopped                 ping 8.8.8.8
[bjames@lwks1 neverthenetwork]$ jobs
[1]+  Stopped                 ping 8.8.8.8
[bjames@lwks1 neverthenetwork]$ kill %1
```

Notice that we didn't get the `ping statistics` lines after ping was killed. This is because we stopped the job forcefully with `kill` instead of using `CTRL+C`.

`kill` works on both jobs in the current terminal session and processes running outside of the current session. When preceded with `%` the number following the command refers to the job number  (as reported by `jobs`), without the `%` it refers to the Process-ID or PID. The PID of a process can be found using the `ps` or `top` commands. 

```
[bjames@lwks1 ~]$ ps ut | grep ping
bjames   14437  0.0  0.0 221516  2052 pts/0    S    21:31   0:00 ping -q 8.8.8.8
bjames   14505  0.0  0.0 221516  2076 pts/0    S    21:32   0:00 ping 4.2.2.2
bjames   21005  0.0  0.0 215744   832 pts/0    S+   21:59   0:00 grep --color=auto ping
[bjames@lwks1 ~]$ kill 14505
[2]   Terminated              ping 4.2.2.2 > ping.out
[bjames@lwks1 ~]$ ps ut | grep ping
bjames   14437  0.0  0.0 221516  2052 pts/0    S    21:31   0:00 ping -q 8.8.8.8
bjames   21064  0.0  0.0 215744   832 pts/0    S+   21:59   0:00 grep --color=auto ping
```

By default `kill` sends SIGTERM, but it can send any of the POSIX signals. `kill -l` lists the signals along with the number kill uses to refer to that signal. As an example, `kill -9 %1` would've killed ping using SIGKILL instead of SIGTERM. 

__Note:__ SIGKILL should really only be used for processes that can't be killed using SIGTERM or SIGINT. SIGKILL doesn't give the process a chance to clean up before exiting and in many cases SIGTERM will work in places SIGINT does not.

### Switching Between Jobs

You can start a job in the background by appending `&` to the command `ping -q 8.8.8.8 &`. You can also send the current process to the background by using `CTRL + Z` to stop the process and then `bg` to have the process run in the background. To bring a process back to the foreground, use `fg`. By default `fg` will bring the most recent job to the foreground, but you can specify a process using `fg %<jobnumber>`.

```
[bjames@lwks1 ~]$ sudo tcpdump -w out.pcap
tcpdump: listening on enp4s0, link-type EN10MB (Ethernet), capture size 262144 bytes
^Z
[1]+  Stopped                 sudo tcpdump -w out.pcap
[bjames@lwks1 ~]$ bg
[1]+ sudo tcpdump -w out.pcap &
[bjames@lwks1 ~]$ ping -q 8.8.8.8 &
[2] 26389
PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
[bjames@lwks1 ~]$ jobs
[1]-  Running                 sudo tcpdump -w out.pcap &
[2]+  Running                 ping -q 8.8.8.8 &
[bjames@lwks1 ~]$ fg
ping -q 8.8.8.8
^C
--- 8.8.8.8 ping statistics ---
10 packets transmitted, 10 received, 0% packet loss, time 23ms
rtt min/avg/max/mdev = 3.571/4.137/5.975/0.687 ms
[bjames@lwks1 ~]$ fg
sudo tcpdump -w out.pcap
^C492 packets captured
503 packets received by filter
0 packets dropped by kernel
[bjames@lwks1 ~]$ 
```

Note that this doesn't redirect the command's output, so it can get a little messy. Many commands have arguments that suppress some or all of their output. Above I used `tcpdump -w` to have tcpdump write to a file and `ping -q` to suppress all ping output with the exception of the summary statistics. Some commands don't have a built in way of doing this, but in those cases, we can use [IO Redirection](#io-redirection) as a workaround. 

#### Keeping Jobs Alive

Commands sent to the background only stay there until your current terminal session ends. This means that if your SSH session ends or you close the terminal window on your Linux desktop, all the jobs you've started die. Luckily, there are a couple of built in ways to keep jobs alive after a session ends.

##### `nohup`

When a session ends, `SIGHUP` is sent to all running jobs. When `SIGHUP` is received, jobs clean up and stop. `nohup` prevents programs from receiving `SIGHUP` when you exit and it also redirects their output to `nohup.out`.

```
[bjames@lwks1 ~]$ nohup ping 8.8.8.8 &
[1] 4620
nohup: ignoring input and appending output to 'nohup.out'
[bjames@lwks1 ~]$ exit
```

Later, we can look at the output by reading `nohup.out`

```
[bjames@lwks1 ~]$ more nohup.out 
PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=54 time=3.50 ms
64 bytes from 8.8.8.8: icmp_seq=2 ttl=54 time=4.06 ms
<redacted for brevity>
64 bytes from 8.8.8.8: icmp_seq=81 ttl=54 time=3.99 ms
64 bytes from 8.8.8.8: icmp_seq=82 ttl=54 time=3.91 ms
```

You can't re-attach to a job ran with `nohup`. To kill the job, you need to know the PID. 

```
[bjames@lwks1 ~]$ ps aux | grep ping
bjames    4620  0.0  0.0 221516  2012 pts/1    S    16:43   0:00 ping 8.8.8.8
bjames    5935  0.0  0.0 215744   896 pts/1    S+   16:49   0:00 grep --color=auto ping
[bjames@lwks1 ~]$ kill 4620
[1]+  Terminated              nohup ping 8.8.8.8
[bjames@lwks1 ~]$
```

##### `disown`

By default, disown removes the job from your active job list. Which also prevents `SIGHUP` from being sent to the job. You can also use `disown -h` to keep the job in your active job list, but to prevent `SIGHUP` from being sent to the job when your session ends. 

To use `disown`, start a job, send it to the background and then run `disown` or `disown %<job-number>`. 

```
[bjames@lwks1 ~]$ ping 8.8.8.8
PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=54 time=4.03 ms
64 bytes from 8.8.8.8: icmp_seq=2 ttl=54 time=3.85 ms
64 bytes from 8.8.8.8: icmp_seq=3 ttl=54 time=4.73 ms
64 bytes from 8.8.8.8: icmp_seq=4 ttl=54 time=4.34 ms
^Z
[1]+  Stopped                 ping 8.8.8.8
[bjames@lwks1 ~]$ bg
[1]+ ping 8.8.8.8 &
[bjames@lwks1 ~]$ 64 bytes from 8.8.8.8: icmp_seq=5 ttl=54 time=3.99 ms
64 bytes from 8.8.8.8: icmp_seq=6 ttl=54 time=4.05 ms
64 bytes from 8.8.8.8: icmp_seq=7 ttl=54 time=3.95 ms
dis64 bytes from 8.8.8.8: icmp_seq=8 ttl=54 time=3.97 ms
own64 bytes from 8.8.8.8: icmp_seq=9 ttl=54 time=5.58 ms

64 bytes from 8.8.8.8: icmp_seq=11 ttl=54 time=4.11 ms
[bjames@lwks1 ~]$exit
```

__Note:__`nohup` and `disown` are functionally the same except `nohup` handles IO redirection for you. Absent of any other [IO Redirection](#io-redirection), `disown`ed jobs will continue to send output to `stdout` until the current session ends.

I don't cover `screen` here as I don't use it myself, but if you find `disown` or `nohup` insufficient for your needs you might look at using `screen` instead.

## IO Redirection

IO Redirection is one of the more powerful features of the Linux command line. I only cover the essentials here, but it's rare that you'll need much more than what I've listed below. For more details try searching for Pipelines and REDIRECTION in `man bash`

### Standard Streams

POSIX compliant programs have three standard streams. `stdin` or standard input is the input you give to a program. `stdout` or standard output is the output from the program. `stderr` or standard error is a separate output stream (also written to the terminal) used for error messages. In keeping with the [Unix Philosophy](#unix-philosophy) these all have pretty predictable output (or take predictable input)[^8]. These streams are what allow [IO Redirection](#io-redirection) to take place.

### Redirection Operators

* `command1 | command2`
	- Redirects `stdout` from command1 to `stdin` of command2.
	- This type of redirection is known as a __pipe__
	- Example: using grep to search the output of `man bash`
	
```
[bjames@lwks1 ~]$ man bash | grep -n Pipelines
257:   Pipelines
```
* `command > outfile.txt`
	- Redirects `stdout` to outfile.txt, overwriting the file
	- Example: using `cat` to concatenate two files and sending the output to outfile.txt 
```
[bjames@lwks1 ~]$ cat cool.txt notcool.txt > outfile.txt
[bjames@lwks1 ~]$ more outfile.txt 
cool
not cool
```
* `command >> outfile.txt`
	- Redirects `stdout` to outfile.txt, appending the file
	- Example: using `cat` to concatenate two files and sending the output to outfile.txt after the command in the previous example has already been executed
```
[bjames@lwks1 ~]$ cat cool.txt notcool.txt >> outfile.txt
[bjames@lwks1 ~]$ more outfile.txt 
cool
not cool
cool
not cool	
```
* `command &> outfile.txt`
	- Redirects `stdout` and `stdin` to outfile.txt
	- Example: using `cat` to concatenate an existent file with a nonexistent file first only redirecting `stdout` and then redirecting `stdout` and `stderr`.
	- Appending looks exactly how you would expect `cat cool.txt doesntexist.txt &>> outfile.txt`
```
[bjames@lwks1 ~]$ cat cool.txt doesntexist.txt > outfile.txt
cat: doesntexist.txt: No such file or directory
[bjames@lwks1 ~]$ more outfile.txt 
cool
[bjames@lwks1 ~]$ cat cool.txt doesntexist.txt &> outfile.txt
[bjames@lwks1 ~]$ more outfile.txt 
cool
cat: doesntexist.txt: No such file or directory
```
* `command < infile.txt`
	- Redirects the contents of `infile.txt` to `stdin`
	- Example: Redirect a list of domains to `nslookup`'s `stdin`
```
[bjames@lwks1 ~]$ nslookup < domainlist.txt 
Server:		192.168.88.1
Address:	192.168.88.1#53

Non-authoritative answer:
Name:	neverthenetwork.com
Address: 174.138.44.218
Server:		192.168.88.1
Address:	192.168.88.1#53

Non-authoritative answer:
Name:	cisco.com
Address: 72.163.4.185
Name:	cisco.com
Address: 2001:420:1101:1::185
Server:		192.168.88.1
Address:	192.168.88.1#53

Non-authoritative answer:
Name:	juniper.com
Address: 192.107.16.40
Server:		192.168.88.1
Address:	192.168.88.1#53

Non-authoritative answer:
Name:	arista.com
Address: 64.68.200.46

[bjames@lwks1 ~]$ 	
```

### Chaining Redirection Operators

* Example: Redirect domainlist.txt to `nslookup`, pipe the output into `grep` and redirect `grep`'s output to result.txt
```
[bjames@lwks1 ~]$ nslookup < domainlist.txt | grep -B 2 64.68.200.46 > result.txt
[bjames@lwks1 ~]$ more result.txt 
Non-authoritative answer:
Name:	arista.com
Address: 64.68.200.46
```
* Example: Concatenate two domain lists, `grep` the output for the word 'cisco' and perform an `nslookup` for each result
```
[bjames@lwks1 ~]$ cat domainlist.txt domainlist2.txt | grep cisco | nslookup
Server:		192.168.88.1
Address:	192.168.88.1#53

Non-authoritative answer:
Name:	cisco.com
Address: 72.163.4.185
Name:	cisco.com
Address: 2001:420:1101:1::185
Server:		192.168.88.1
Address:	192.168.88.1#53

Non-authoritative answer:
Name:	sanfrancisco.com
Address: 104.27.130.254
Name:	sanfrancisco.com
Address: 104.27.131.254
Name:	sanfrancisco.com
Address: 2606:4700:30::681b:82fe
Name:	sanfrancisco.com
Address: 2606:4700:30::681b:83fe
```

## Command Aliases, Bash Functions and .bashrc

The `alias` command is used to create command aliases. As an example, lets create a new alias called `isotime`. Let's say `date +"%Y-%m-%dT%H%M%S"` gives us the date and time in the format we'd like. This isn't a fun command to type, so lets create an alias.

```
[bjames@lwks1 ~]$ alias isotime="date +"%Y-%m-%dT%H%M%S""
[bjames@lwks1 ~]$ isotime
2019-10-09T091650
```

__Note:__The `date` command has a argument that returns ISO 8601 formatted timestamps, but it includes colons in the timestamp. If we want to add timestamps to files, colons may cause problems.

Aliases are great for simple, hard to remember strings of commands, but they can't be used for anything that requires variables. Luckily, bash is both a shell and a functional programming language. So for anything that requires variables, we can write functions. 

In the [SSH](#ssh) section we learned that you can log ssh sessions using `ssh hostname | tee logfile.log`. This isn't difficult to remember, but we might as well shorten the command a bit if we are going to be typing it regularly. This is a task that lends itself well to bash functions. 

```
function logssh()
{
    currtime=$(isotime);
    ssh $1 | tee -a ~/sshlogs/$1-$currtime.log;
}
```

When working with bash functions `$n` refers to the nth command line argument. This means $1 refers to the string following `logssh`. 

__Note:__ I'm not going to go into detail on writing bash scripts here. That's outside of the scope of this document. I do want to give you a basic example of what they are and how to use them.

To make the function available, we can simply paste the entire function into our terminal. 

```
[bjames@lwks1 ~]$ alias isotime="date +"%Y-%m-%dT%H%M%S""
[bjames@lwks1 ~]$ function logssh()
> {
> 
>     currtime=$(isotime);
>     ssh $1 | tee -a ~/sshlogs/$1-$currtime.log;
> 
> }
[bjames@lwks1 ~]$ logssh 192.168.88.1
```
__Note:__ In this function, we leveraged the alias we created earlier. For completeness, I recreate the alias below. 

There is one problem with this method, the function and alias we just created are only available in the current terminal session. Future and concurrent sessions can't make use of the function and alias we just created. 

### .bashrc

`.bashrc` is a file that contains bash commands that are ran when a new terminal session is started. Each user has their own `.bashrc` file located at `~/.bashrc`. If we want `isotime` and `logssh` to be available for future terminal sessions, we can add them to our `.bashrc`. 

```
alias isotime="date +"%Y-%m-%dT%H%M%S""
function logssh()
{
    currtime=$(isotime);
    ssh $1 | tee -a ~/sshlogs/$1-$currtime.log;
}
```

Upon login, the `alias` command is ran and the `logssh` function is created and ready to be ran. It should also be noted that `.bashrc` commands that write to `stdout` _will_ write to `stdout` when the session starts. 

__Note:__ On my personal machines I like to add `fortune | cowsay` to the bottom of my `.bashrc` so that I'm greeted by a cow each time I open a new terminal window. Fortune and Cowsay aren't usually installed by default, but are most likely available through your distribution's package manager.

```
 ________________________
< firewall needs cooling >
 ------------------------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
[bjames@lwks1 ~]$
```

## Queue

Things I plan on adding as time allows

* Network Utilities
	- tcpdump
	- dig and nslookup
	- netcat
	- whois
	- traceroute, tracepath and mtr
	- ping
	- dhcping
* File Transfer
	- Clients: SCP, SFTP, FTP
	- Servers: Python Simple HTTP Server
* Text Manipulation
	- sed
	- awk
	- cat
* SSH
	- Tunneling

[^1]: My apologies to Richard Stallman, [GNU+Linux](https://www.gnu.org/gnu/linux-and-gnu.en.html) just doesn't roll of the tongue quite as well.
[^2]: And Fedora since the 'Beefy Miracle' release in 2011!
[^3]: The [Linux Standard Base](http://refspecs.linuxfoundation.org/LSB_4.1.0/LSB-Core-generic/LSB-Core-generic/command.html#CMDUTIL) is the closest thing we have to a standard. It contains a very small subset of the programs you'd find on a typical Linux installation. 
[^4]: This is due to a feature called alternate screen. I generally don't mind altscreen, but there are ways to [effectively disable it](https://www.shallowsky.com/linux/noaltscreen.html).
[^5]: OpenSSH is a widely used product of the OpenBSD Project, another Unix-like operating system. 
[^6]: The wikipedia entry on [POSIX signals](https://en.wikipedia.org/wiki/Signal_(IPC)#POSIX_signals) is a pretty good reference for what each signal actually means.
