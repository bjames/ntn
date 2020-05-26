title: Practical Automation - mod_acl
category:
- Route/Switch
- Automation
- Programming
published: 2019-12-31
update_interval: monthly
author: Brandon James
summary: Managing access lists is one of the more painful parts of being a network engineer. Once you've finishing working out what should or should not be allowed, you write the ACL and then paste it into all your devices. The minute you finish, the requirements change or the business lets you know what you just broke. In the future, SGTs and SDN promise to fix this problem, but you might not be there yet. `mod_acl` is a simple and fast way to manage ACLs. 


Managing access lists is one of the more painful parts of being a network engineer. Once you've finishing working out what should or should not be allowed, you write the ACL and then paste it into all your devices. The minute you finish, the requirements change or the business lets you know what you just broke. In the future, SGTs and SDN promise to fix this problem, but you might not be there yet. `mod_acl` is a simple and fast way to manage ACLs. 

If you want to skip the fluff and get right to the code, you can clone my repo on [github](https://github.com/bjames/mod_acl). 

## Preliminary Notes on ACLs

This article assumes you are familiar with writing IOS and NXOS access-lists, but there are a few items I feel are worth reiterating, especially in the context of scripting. `mod_acl` takes an access-list as input, but doesn't do any sort of sanity checking, so it's important to know how ACLs function.[^1]

1. Cisco ACLs have an implicit __deny__ at the end. This becomes especially important when you are pushing ACLs to every router in your network.
2. An ACL that hasn't been created can be configured (ie applied to an interface, VTY line, etc.). In this case, the ACL is immediately used when created. _Because of the implicit deny_ you can easily lock yourself out of a device with an ACL applied to the management interface.
3. NXOS will automatically convert IOS style ACL lines into NXOS ACL lines, this can make script configuration much easier. 
4. Unfortunately, IOS and NXOS treat `remarks` differently. In IOS, remarks do not have a line number and do not show up in the output of `show ip access-list`. The opposite is true for NXOS.

### Working with ACL remarks in IOS and NXOS

To illustrate the difference in line numbering, let's look at the following ACL

```
ip access-list extended TEST
 remark permit accounting
 permit ip 192.168.200.0 0.0.0.255 any
 remark permit IT
 permit ip 192.168.210.0 0.0.0.255 any
 remark log unauthorized attempts
 deny ip any any log
```  

When pasted into an IOS device, this becomes:

```
ntn-ios#sh ip access-list TEST
Extended IP access list TEST
	10 permit ip 192.168.200.0 0.0.0.255 any
	20 permit ip 192.168.210.0 0.0.0.255 any
	30 deny ip any any log
ntn#sh run | sec ip access-list extended TEST
ip access-list extended TEST
 remark permit accounting
 permit ip 192.168.200.0 0.0.0.255 any
 remark permit IT
 permit ip 192.168.210.0 0.0.0.255 any
 remark log unauthorized attempts
 deny ip any any log
```

When pasted into an NXOS device, this becomes:

```
ntn-nxos# sh ip access-list TEST

IP access list TEST
	10 remark permit accounting
	20 permit ip 192.168.200.0/24 any
	30 remark permit IT
	40 permit ip 192.168.210.0/24 any
	50 remark log unauthorized attempts
	60 deny ip any any log
ntn-nxos#sh run | sec "ip access-list TEST"
ip access-list TEST
  10 remark permit accounting
  20 permit ip 192.168.200.0/24 any
  30 remark permit IT
  40 permit ip 192.168.210.0./24 any
  50 remark log unauthorized attempts
  60 deny ip any any log
```

Inserting lines into NXOS ACLs is pretty intuitive, you simply drop into the ACL configuration and prepend the line number on your remark.

```
ntn-nxos(config-acl)# 5 remark disallow accounts payable
ntn-nxos(config-acl)# 6 deny ip 192.168.200.128/28 any
ntn-nxos(config-acl)# end
ntn-nxos# sh ip access-list TEST

IP access list TEST
	5 remark disallow accounts payable
	6 deny ip 192.168.200.128/28 any
	10 remark permit accounting
	20 permit ip 192.168.200.0/24 any
	30 remark permit IT
	40 permit ip 192.168.210.0/24 any
	50 remark log unauthorized attempts
	60 deny ip any any log
```

You can also insert remarks into IOS ACLs, but it's not quite as intuitive.

```
ntn-ios(config-ext-acl)#remark disallow accounts payable
ntn-ios(config-ext-acl)#5 deny ip 192.168.200.128 0.0.0.15 any
ntn-ios(config-ext-acl)#end
ntn-ios#sh run | sec ip access-list extended test
ip access-list extended TEST
 remark disallow accounts payable
 deny   ip 192.168.200.128 0.0.0.15 any
 permit ip any any

```

This will insert the remark into the running configuration above the ACL line that follows. If no ACL line follows, the remark is added to the bottom of the ACL. 

## Options for Pushing ACLs

1. Rip and Replace
	
	By rip and replace, I mean deleting the ACL and recreating it. This is what I prefer to do, it enforces consistency and line ordering. However, caution should be used when modifying ACLs on management interfaces and VTY lines using this method.[^2] __*Due to the implict deny*, this will result in *brief* packet loss as the ACL is being recreated.__ Depending on how the ACL is used, this could be perfectly acceptable.
	
	Here's how the rip and replace method looks on the CLI:
	
```
ntn(config)#no ip access-list extended TEST 
ntn(config)#ip access-list extended TEST 
ntn(config-ext-nacl)#permit ip host 192.168.1.1 any 
ntn(config-ext-nacl)#permit ip host 192.168.1.2 any 
ntn(config-ext-nacl)#deny ip any any log
```
	
2. Modify in Place

	This is what I do with ACLs applied in places that either cannot handle short disruptions or when the rip and replace method could cause loss of management access. 
	
	There are two issues with this method. 
	
	1. By default you only have 9 lines in between each ACL entry. Since ACL order can be important, this method requires careful planning. 
	2. [As mentioned above](#preliminary-notes-on-acls), NXOS counts `remark` entries as ACL lines, IOS does not. When you modify in place, you need to be mindful of this. If you use remarks, line numbers on IOS and NXOS won't match, so you'll need to create distinct script [configuration files](#configuration) for each device type. 

	Here's how the modify in place method looks on the CLI:
	
```
ntn(config-ext-nacl)#do sh ip access-list TEST
Extended IP access list TEST
    10 permit ip host 192.168.1.1 any
    20 permit ip host 192.168.1.2 any
    30 deny ip any any log
ntn(config)#ip access-list extended TEST
ntn(config)#	21 permit ip any any log
ntn(config-ext-nacl)#do sh ip access-list TEST
Extended IP access list TEST
    10 permit ip host 192.168.1.1 any
    20 permit ip host 192.168.1.2 any
    21 permit ip any any log
    30 deny ip any any log
ntn(config-ext-nacl)#
```
	
`mod_acl` implements both Rip and Replace and Modify in Place. The method used is determined by the scripts `append` flag.

## `mod_acl`'s Implementation

`mod_acl` is actually a really simple script. In general, the scripts flow is as follows:

1. Verify Configuration
2. Request Credentials
3. Validate Credentials against the first device in the device list
4. Use Pool.map() to spawn _n_ processes (where in _n_ is the number of threads specified in the YAML file).[^3]
	
	__Note:__ The following takes place within threads spawned by Pool.map() 
	
	i. Open an SSH session to the device
	
	ii. If Nexus, call `nxos_mod_acl` function, if IOS, call `ios_mod_acl`
	
	iii. Modify the ACL, deleting it first if append is set to False in the YAML file. __Note:__ This is literally the only difference between the rip-and-replace (append set to False) and modify-in-place (append set to True) methods in the script. 
	
	iv. The script then enters access-list configuration mode and inputs the contents of `acl_lines`.
	
	v. Thread exits
	
5. The script does some basic processing on the output for validation purposes.

## Configuration

Script configuration is done through a YAML file consisting of a few options:

- threads: This is the number of processes spawned by the script
- append: Whether to run the script in rip-and-replace or append mode
- extended: Extended or standard ACL (__note:__ Nexus does not have a concept of standard vs extended ACLs, this is handled by the script)
- acl_name: The name of the ACL
- acl_lines: A list of the lines in the ACL. The pipe is required. It tells the YAML interpreter that [line breaks are significant](https://yaml.org/spec/1.2/spec.html#id2760844). These are the ACL lines the script inputs after entering ACL configuration mode.
- device_list: A list of device hostnames or IP addresses and device_types (must be one of cisco_ios or cisco_nxos).

You tell the script which YAML file to use when you [run the it](#usage), so feel free to use names that are significant to your environment.  

### Example Configuration - Rip and Replace

When using the rip and replace method we can use the same YAML file for IOS and NXOS.

```
threads: 8
append: False
extended: True
acl_name: ntn
acl_lines: |
 remark deny traffic from desktop
 deny ip host 172.16.12.148 any
 remark permit traffic from jumpbox
 permit ip host 172.16.12.20 any
device_list:
  - hostname: 172.16.12.112
    device_type: cisco_ios
  - hostname: 172.16.12.110
    device_type: cisco_ios
  - hostname: 172.16.12.109
    device_type: cisco_ios
  - hostname: 172.16.12.111
    device_type: cisco_nxos
  - hostname: 172.16.12.222
    device_type: cisco_nxos
```

### Example Configuration - Append

When using the append method, you should split your configuration into two separate files, one for NXOS and one for IOS devices. The script will execute successfully either way, but due to the [differences in line numbering device types](#preliminary-notes-on-acls), it's safest to split the configuration file.

__IOS Configuration File__

```
threads: 8
append: True
extended: True
acl_name: ntn
acl_lines: |
 remark permit traffic from laptop
 15 permit ip host 172.16.12.160 any
device_list:
  - hostname: 172.16.12.112
    device_type: cisco_ios
  - hostname: 172.16.12.110
    device_type: cisco_ios
  - hostname: 172.16.12.109
    device_type: cisco_ios
```

__NXOS Configuration File__

```
threads: 8
append: True
extended: True
acl_name: ntn
acl_lines: |
 35 remark permit traffic from laptop
 36 permit ip host 172.16.12.160 any
device_list:
  - hostname: 172.16.12.111
    device_type: cisco_nxos
  - hostname: 172.16.12.222
    device_type: cisco_nxos
```


## Validation

I went as simple as possible on validation. It's mostly a manual process with a few cues to tell the user whether or not they need to check on any of the devices. 

To illustrate, Here's an example of what this looks like:

```
[bjames@lwks1 mod_acl]$ ./venv/bin/python mod_acl.py ntn_acl.yml 
ntn will be modified using mode replace
Is this correct? [y/n] y
Username: ntn
Password: 
error 172.16.12.222
172.16.12.112 completed
172.16.12.109 completed
172.16.12.110 completed
172.16.12.111 completed

FULL RESULTS
_________________
[{'device': '172.16.12.112',
  'device_type': 'cisco_ios',
  'result': 'Extended IP access list ntn\n'
            '    10 deny ip host 172.16.12.148 any\n'
            '    20 permit ip host 172.16.12.20 any'},
 {'device': '172.16.12.110',
  'device_type': 'cisco_ios',
  'result': 'Extended IP access list ntn\n'
            '    10 deny ip host 172.16.12.148 any\n'
            '    20 permit ip host 172.16.12.20 any'},
 {'device': '172.16.12.109',
  'device_type': 'cisco_ios',
  'result': 'Extended IP access list ntn\n'
            '    10 deny ip host 172.16.12.148 any\n'
            '    20 permit ip host 172.16.12.20 any'},
 {'device': '172.16.12.111',
  'device_type': 'cisco_nxos',
  'result': '\n'
            'IP access list ntn\n'
            '        10 remark deny traffic from desktop\n'
            '        20 deny ip 172.16.12.148/32 any \n'
            '        30 remark permit traffic from jumpbox\n'
            '        40 permit ip 172.16.12.20/32 any \n'},
 {'device': '172.16.12.222',
  'device_type': 'cisco_nxos',
  'result': NetMikoTimeoutException('Connection to device timed-out: cisco_nxos 172.16.12.222:22')}]

SUMMARY RESULTS
_________________
{'ios': [{'device_type': 'cisco_ios',
          'hostname': '172.16.12.112',
          'result_lines': 3},
         {'device_type': 'cisco_ios',
          'hostname': '172.16.12.110',
          'result_lines': 3},
         {'device_type': 'cisco_ios',
          'hostname': '172.16.12.109',
          'result_lines': 3}],
 'ios_diff': False,
 'nexus': [{'device_type': 'cisco_nxos',
            'hostname': '172.16.12.111',
            'result_lines': 6},
           {'device_type': 'cisco_nxos',
            'hostname': '172.16.12.222',
            'result_lines': 0}],
 'nexus_diff': True}
[bjames@lwks1 mod_acl]$ 
```

IOS and Nexus have different output for `show ip access-list` so the __SUMMARY RESULTS__ output lists them separately. `result_lines` is the number of lines returned by `show ip access-list`. The flags `ios_diff` and `nxos_diff` are set to `True`, when the number of result_lines don't match for that specific device type. If these flags are set to true, I look over the __FULL RESULTS__ for the devices with the incorrect number of lines and then log into the device if necessary. 

You could go much fancier with your validation, but this is simple and works great for my use. 

## Usage

Run the script with `./venv/bin/python mod_acl.py mod_acl.yml`

## Code

The latest copy of the script, along with a copy of the GPL v3 license, is available on my [github](https://github.com/bjames/mod_acl). I've copied the script below for reference:

```
from multiprocessing import Pool
from functools import partial
from netmiko import ConnectHandler, NetMikoAuthenticationException, NetMikoTimeoutException
from yaml import safe_load
from pprint import pprint
from sys import argv
from json import dumps
from datetime import datetime

import getpass

def ssh_connect(hostname, device_type, username, password):

    device = {
        'device_type': device_type,
        'ip': hostname,
        'username': username,
        'password': password
    }

    return ConnectHandler(**device)


def get_valid_credentials(hostname, device_type):

    """
        gets username and password, opens an ssh session to verify the credentials
        then closes the ssh session

        returns username and password

        Doing this prevents multiple threads from locking out an account due to mistyped creds
    """

    # attempts to get the username, prompts if needed
    username = input('Username: ')

    # prompts user for password
    password = getpass.getpass()

    authenticated = False

    while not authenticated:

        try:

            test_ssh_session = ssh_connect(hostname, device_type, username, password)
            test_ssh_session.disconnect()

        except NetMikoAuthenticationException:

            print('authentication failed on ' + hostname + ' (CTRL + C to quit)')

            username = input('Username: ')
            password = getpass.getpass()

        except NetMikoTimeoutException:

            print('SSH timed out on ' + hostname)
            raise

        else:

            # if there is no exception set authenticated to true
            authenticated = True

    return username, password


def nxos_mod_acl(ssh_session, device, acl_name, acl_lines, append):

    """
        Updates ACLs on cisco_nxos devices
    """

    if not append:
        # remove the old ACL
        ssh_session.send_config_set('no ip access-list {}'.format(acl_name))

    # create the config set for the new ACL
    config_set = ['ip access-list {}'.format(acl_name)]
    config_set = config_set + acl_lines.splitlines()

    # command input on nexus devices is slow, so we use a delay_factor of 10 to slow down the input and prevent timeouts
    ssh_session.send_config_set(config_set, delay_factor = 10)

    result = ssh_session.send_command('show ip access-list {}'.format(acl_name))

    return result


def ios_mod_acl(ssh_session, device, acl_name, acl_lines, append, extended):

    """
        Updates ACLs on cisco_ios devices
    """

    if not append:
        # remove the old ACL
        if extended:
            ssh_session.send_config_set('no ip access-list extended {}'.format(acl_name))
        else:
            ssh_session.send_config_set('no ip access-list standard {}'.format(acl_name))

    # create the config set for the new ACL
    if extended:
        config_set = ['ip access-list extended {}'.format(acl_name)]
    else:
        config_set = ['ip access-list standard {}'.format(acl_name)]

    config_set = config_set + acl_lines.splitlines()

    ssh_session.send_config_set(config_set)

    result = ssh_session.send_command('show ip access-list {}'.format(acl_name))

    return result


def mod_acl(acl_name, acl_lines, append, extended, username, password, device):

    try:

        ssh_session = ssh_connect(device['hostname'], device['device_type'], username, password)

    except Exception as e:

        print('error {}'.format(device['hostname']))
        return {'device': device['hostname'], 'device_type': device['device_type'], 'result': e}


    try:

        if device['device_type'] == 'cisco_ios':

            result = ios_mod_acl(ssh_session, device, acl_name, acl_lines, append, extended)

        elif device['device_type'] == 'cisco_nxos':

            result = nxos_mod_acl(ssh_session, device, acl_name, acl_lines, append)

    except Exception as e:

        print('error {}'.format(device['hostname']))
        return {'device': device['hostname'], 'result': 'Failed\n{}'.format(e)}

    print('{} completed'.format(device['hostname']))

    return {'device': device['hostname'], 'device_type': device['device_type'], 'result': result}


def verify(acl_name, append):

    """
        Asks the user to verify settings in the YAML file
    """

    if append:

        mode = 'append'

    else:

        mode = 'replace'

    print('{} will be modified using mode {}'.format(acl_name, mode))

    user_input = input('Is this correct? [y/n] ').lower()

    if user_input[0] == 'y':

        return True

    else:

        return False


def validation(results):

    """
        Basic validation
        
        It's up to the user to read the results and verify consistancy between the length of ACLs on each device.

        If nexus_diff or ios_diff is True, then a difference was found between the number of lines for devices of that device type
    """

    validation_results = {'nexus': [], 'ios': [], 'nexus_diff': False, 'ios_diff': False}

    nexus_first_count = -1
    ios_first_count = -1

    for device in results:

        try:
            line_count = len(device['result'].splitlines())
        except AttributeError:
            line_count = 0

        result = {
            'hostname': device['device'],
            'device_type': device['device_type'],
            'result_lines': line_count
        }

        if device['device_type'] == 'cisco_nxos':
            
            if nexus_first_count == -1:
                nexus_first_count = line_count
            elif nexus_first_count != line_count:
                validation_results['nexus_diff'] = True

            validation_results['nexus'].append(result)
        elif device['device_type'] == 'cisco_ios':

            if ios_first_count == -1:
                ios_first_count = line_count
            elif ios_first_count != line_count:
                validation_results['ios_diff'] = True

            validation_results['ios'].append(result)

    return validation_results


def main():

    try:

        script_settings = safe_load(open(argv[1]))

    except IndexError:

        print('Please specify a configuration file')
        exit()


    # End the script if the settings are incorrect
    if not verify(script_settings['acl_name'], script_settings['append']):
        exit()

    # Get working credentials from the user
    username, password = get_valid_credentials(script_settings['device_list'][0]['hostname'], script_settings['device_list'][0]['device_type']) 

    # Spawn the number of threads configured in the YAML file
    with Pool(script_settings['threads']) as pool:

        results = pool.map(partial(mod_acl,
                         script_settings['acl_name'],
                         script_settings['acl_lines'],
                         script_settings['append'],
                         script_settings['extended'],
                         username,
                         password),
                 script_settings['device_list'])

    print('\nFULL RESULTS\n_________________')

    pprint(results)

    print('\nSUMMARY RESULTS\n_________________')
    validation_results = validation(results)

    pprint(validation_results)


main()
```

[^1]: I _highly_ recommend running the script against a set of test devices prior to pushing to prod. This will help ensure your ACL is formatted correctly. I can't be held liable for anything you break using this script :).
[^2]: During my testing ACLs applied to VTY lines did not affect the current VTY session. Nonetheless, this could change in the future, so I'd err on the side of caution.
[^3]: If _m_ > _n_, where _m_ is the number of devices, the device list is broken into chunks of _m_/_n_ and is iterated by Pool.map()