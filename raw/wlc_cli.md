title: WLC CLI Cheatsheet
published: 2019-07-30
category:
- Wireless
- Cheatsheets
author: Brandon James
summary: The WLC CLI can be a little less than intuitive at times. I put together this quick reference with some of my most used WLC commands.

I'm on the WLC CLI much less often than NXOS or IOS so I haven't really committed all the commands to memory. This reference documents some of the useful things I do or have done in the past on the WLC CLI.

### Useful Show Commands

* Instead of: `show command | include`, the WLC uses: `grep include _regex_ "show command"`
    * This is a really useful tool which makes it easy to do things like gather all the joined APs at a site to verify they are in the correct AP group
    * You can also do an inverse match with `grep exclude`
    * The number of lines matched is reported at the end, this is useful for change validation
* List all WLANs: `show wlan`
* List all WLANs in an AP group: `show wlan apgroups`
* List all APs: `show ap summary`
    * List all APs in a specific subnet `grep include 10\.10\.10\. "show ap summary"`
* Show WLANs broadcast by a specific AP on a specific radio type: `show ap wlan 802.11[a|b|-abgn] _AP-NAME_` 
* List all FlexConnect Groups: `show flexconnect group summary`
* List all APs and AVC mappings in a FlexConnect Group: `show flexconnect group _GROUP-NAME_`
    * Appending 'aps' to the end of the command will list just the member APs

### AP Configuration

Generally APs should be configured automatically using the WLC, after all that's the entire point of using a WLC. However, when cleaning up existing environments or migrating to a new environment, it might be necessary to configure the APs directly.

* Change an APs Primary Controller
    * This is useful for migrating APs to a new controller or to fail over your infrastructure to your secondary controller while leaving the original WLC online:

    ```
    config ap primary-base DCA-WLC-01 BLG1-FLR1-AP1 192.168.0.20
    ```

    ```
    config ap primary-base _CONTROLLER-NAS-ID_ _AP-NAME_ _CONTROLLER_IP_ADDRESS_
    ```

    * Your primary WLC and secondary WLC cannot be the same

    * Changing an APs Secondary Controller is similar:

        ```
        config ap secondary-base DCB-WLC-01 BLG1-FLR1-AP1 192.168.1.20
        ```

        * To remove a secondary controller you set the controller to a blank NAS-ID and use 0.0.0.0 as the IP address

            ```
            config ap secondary-base '' BLG1-FLR1-AP1 0.0.0.0
            ```
            
            * If your new primary controller is your old secondary controller, this has to be done first
            
* Change an APs Group Name 
    ```
    config ap group-name BLG1-AP-GROUP BLG1-FLR1-AP1
    ```
    * config ap group-name _GROUP-NAME_ _AP-NAME_
    
* Change an APs Operational Mode
   ```
   config ap mode flexconnect submode none BLG1-FLR1-AP1
   ```
    * config ap mode _mode_ submode _submode_ _AP-NAME_
         * valid modes are: local, bridge, flex+bridge, flexconnect, monitor, rogue, se-connect, sensor, sniffer
         * valid submodes are: none, wips

#### Making batch AP configuration changes (Example: Batch migrating APs from their primary controller to the secondary)
*The following example works on linux machines, but a similar process can also be performed using an excel spreadsheet*

* Log into the WLC the APs are registered to, if you aren't already logging ssh sessions, log the session as follows:
    * `ssh DCA-WLC-01 | tee logfile.log`

* Issue the following commands
```
config paging disable
show ap join stats summary all
logout
```

* Then generate the script using the following:

    ```bash
    grep -P '192\.168\.20\.\d+.*\s{2}Joined' log.log \
    | awk '{print "config ap secondary-base '\'' '\'' " $3 " 0.0.0.0\nconfig ap primary-base DCA-WLC-01 " $3 " 192.168.0.20\nconfig ap secondary-base DCB-WLC-01 " $3 " 192.168.1.20"}' > paste_script.txt
    ```

    * Using grep, we select only APs in the 192.168.20.0/24 subnet that are currently joined to the controller:   
            
        * We also only want to modify APs that are actually joined to the controller, alternatively all joined APs can be grabbed with `grep -P '\s{2}Joined' log.log`

    * Then AWK to generate the script
    
        ```
        awk '{print "config ap secondary-base '\'' '\'' " $3 " 0.0.0.0\nconfig ap primary-base DCA-WLC-01 " $3 " 192.168.0.20\nconfig ap secondary-base DCB-WLC-01 " $3 " 192.168.1.20"}'
        ```

        * $3 represents column three, which contains the AP name
        * We first delete the old secondary, then configure the new primary and secondary controllers
    * Finally, redirection is used to output the paste script into a file

A similar process can be used for other batch AP changes. Keep in mind that in cases where the AP has to reboot the character 'y' is required between commands. Example

```
config ap group-name BLG1-AP-GROUP BLG1-FLR1-AP1
y
config ap group-name BLG1-AP-GROUP BLG1-FLR1-AP2
y
```

* This is trivial to add to our awk script above. Simply add `"\n y \n"` to the end
