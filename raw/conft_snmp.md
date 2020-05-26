title: Conf T via SNMP
published: 2017-01-26
category:
- Route/Switch
author: Brandon James
summary: On occasion there might be reasons to make configuration changes via SNMP. Here's how

Lately we've been hitting bugs that cause switches (specifically Cisco 4500-E's) to lose their SSH keys after reboots or crashes. Due to this we've changed our standard operating procedure for reboots to include enabling telnet. This workaround is great during planned outages, but it doesn't really help in the case of unplanned outages. I knew that it was possible to make configuration changes via SNMP, so today when I replaced a lab router and forgot to generate SSH keys, I took advantage of the situation and generated the keys via SNMP.

To do this, you'll need the following:
1. A tftp server

2. A text editor

3. A program that can sent SNMP SET requests (I used snmpset on a linux jumpbox)

4. A Cisco device without it's SSH keys. If you'd like to test this, you could use the 'crypto key zeroize rsa' command from config mode.

In your text editor, create a new text document. The name doesn't matter. Then input the config you'd like to upload. In this case: 

```
crypto key generate rsa mod 4096
end
```

Save this file in your tftp directory. Then run snmpset as follows:

```
# snmpset -v version -c RW_COMMUNITY IP_ADDRESS_OR_HOSTNAME oid.TFTPSERVER_IP s FILENAME
snmpset -v 2c -c SNMP_RW 192.168.0.150 .1.3.6.1.4.1.9.2.1.53.192.168.0.80 s new.cfg 
```

This was nearly instant on the 3945 that I did this on at work, but remember, it takes a little while to generate crypto keys. I'm following along at home with a 2960 and it took nearly a minute to generate the keys.

This OID works by merging the running config with your text document. The related MIB is called 'hostConfigSet' (found here). This is essentially what happens when we enter commands in config mode.

You can make just about any configuration change via SNMP. Naturally, this can be used to do all sorts of nasty things. Such as creating a new user and then changing the login type on your vty lines from TACACS to local. If you are using SNMP v1 or v2c, be sure to keep your community strings under lock and key and use ACLs to control where SNMP traffic can come from.

*Note: This note was originally on my personal blog. I've backdated the post to show the day it was originally written*