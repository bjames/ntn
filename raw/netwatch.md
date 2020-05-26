title: Practical Automation - Netwatch
published: 2019-09-12
category:
- Automation
- Programming
author: Brandon James
summary: In this article I give a brief introduction to my Netwatch script. 


Small data gathering utilities are one of my favorite forms of automation. They provide immediate value and have no risk of failure. Netwatch runs a set of commands periodically against a group of network devices. It features concurrency, error handling and just the right amount of customization. Netwatch was inspired by a [post on Reddit](https://www.reddit.com/r/Cisco/comments/d2ndqq/dump_switch_commands_to_a_file_on_a_schedule/) and the *nix utility `watch`. 

If you want to skip the fluff and get right to the code, you can clone my repo on [github](https://github.com/bjames/netwatch).

## Implementation Goals

1. Execution should take place on each device simultaneously to get a full picture of the network at a single moment in time.
2. The script should be reusable without any modifications to the script itself.
3. The output should include accurate timestamps so we can correlate events across multiple devices.
4. Output should be written to a file each time the main loop executes, that way if the script is stopped or dies we don't lose the data up to that point.
5. The script should be able to complete it's task without using task scheduler or Cron. As these require configuration to take place outside of the script.


## Installation

Requires python 3+. I strongly suggest creating a new virtual environment for use with this script. I broadly cover this here.

1. install virtualenv if it's not already installed `python -m pip install virtualenv`

2. create a new virtualenv `python -m virtualenv venv`

3. clone the repository `git clone https://github.com/bjames/netwatch`

4. activate the virtualenv
    * Linux/OS X `source ./venv/bin/activate`
    * Windows `venv\Scripts\activate`

5. install the required libraries `python -m pip install -r netwatch/requirements.txt'

## Configuration

In the YAML file, anything defined under the default section can be overridden on a per-device basis. The YAML file below demonstrates overriding the device_type and command list. 

```
# Number of devices to run commands on in parallel
threads: 4
# Time to sleep in between iterations (seconds)
sleep_time: 300
# maximum iterations (set to 0 to repeat forever)
max_iter: 288
# If true, the results are output to one file per device
file_output: true
# If true, the results are printed to the screen
print_output: true
# default settings that may be overridden on a per device basis
default:
  # commands to run
  commands:
    - show int status
    - show cdp neighbors
  # cisco_ios or cisco_nxos
  device_type: cisco_ios
  port: 22
# list devices and device specific config
device_list:
 - hostname: IOS-SWITCH-1A
 - hostname: NXOS-SWITCH-1A
   device_type: cisco_nxos
   commands: 
    - show vlan brief
    - show ip route
```

* This configuration runs `show int status` followed by `show cdp neighbors` on IOS-SWITCH-1A and `show vlan brief` followed by `show ip route` on NXOS-SWITCH-1A. The script runs every 300 seconds and repeats 288 times or once every 5 minutes for 24 hours. 

* The script uses python's multiprocessing library's Pool.map() function. As long as you give the script enough threads (one per device), the command execution will start on each device at roughly the same time. In the above configuration, we've told the script it can spawn up to 4 threads, but in this case only 2 threads will actually be used. I've used 16 threads on Linux VM with 2 cores and 4GB of RAM without any performance degradation, but your mileage my vary. 

You can read more about how I handle concurrency [here](https://neverthenetwork.com/notes/automation_concurrency/) and how I handle script configuration [here](https://neverthenetwork.com/notes/automation_config/).

## Usage

1. Run the script `python ./netwatch.py`. You can also specify a configuration file `python ./netwatch.py myconfig.yaml`.
	* The script will validate your credentials against the first device in the device list before execution begins. This is done to prevent account lockouts.
2. The script will run until it is either stopped or the `max_iter` value is reached. If `file_output` is set to `true`, the script creates one log file per device and appends the output to the log files following each iteration.

## Example Output

```
!!!!!!! show int status on sbx-nxos-mgmt.cisco.com at 2019-09-12 22:35:32.990650


--------------------------------------------------------------------------------
Port          Name               Status    Vlan      Duplex  Speed   Type
--------------------------------------------------------------------------------
mgmt0         DO NOT TOUCH CONFI connected routed    full    1000    --         

--------------------------------------------------------------------------------
Port          Name               Status    Vlan      Duplex  Speed   Type
--------------------------------------------------------------------------------
Eth1/1        --                 connected trunk     full    1000    10g        
Eth1/2        --                 connected trunk     full    1000    10g        
Eth1/3        --                 connected 1         full    auto    10g        
Eth1/4        --                 connected 1         full    auto    10g        
Eth1/5        L3 Link            connected routed    full    1000    10g        
< REDACTED FOR BREVITY>  
Po11          --                 connected trunk     full    1000    --         
Lo1           --                 connected routed    auto    auto    --         
Lo100         --                 connected routed    auto    auto    --         
Vlan1         --                 down      routed    auto    auto    --
Vlan100       mgmt svi - DEMO PL connected routed    auto    auto    --
Vlan101       prod svi - DEMO PL connected routed    auto    auto    --
Vlan102       dev svi - DEMO PLE connected routed    auto    auto    --
Vlan103       test svi - DEMO PL connected routed    auto    auto    --
Vlan104       security svi - DEM connected routed    auto    auto    --
Vlan105       iot svi - DEMO PLE connected routed    auto    auto    --

!!!!!!! show cdp neighbors on sbx-nxos-mgmt.cisco.com at 2019-09-12 22:35:33.895258

Capability Codes: R - Router, T - Trans-Bridge, B - Source-Route-Bridge
                  S - Switch, H - Host, I - IGMP, r - Repeater,
                  V - VoIP-Phone, D - Remotely-Managed-Device,
                  s - Supports-STP-Dispute

Device-ID          Local Intrfce  Hldtme Capability  Platform      Port ID

Total entries displayed: 0

!!!!!!! show int status on sbx-nxos-mgmt.cisco.com at 2019-09-12 22:35:56.499806


--------------------------------------------------------------------------------
Port          Name               Status    Vlan      Duplex  Speed   Type
--------------------------------------------------------------------------------
mgmt0         DO NOT TOUCH CONFI connected routed    full    1000    --         

--------------------------------------------------------------------------------
Port          Name               Status    Vlan      Duplex  Speed   Type
--------------------------------------------------------------------------------
Eth1/1        --                 connected trunk     full    1000    10g        
Eth1/2        --                 connected trunk     full    1000    10g        
Eth1/3        --                 connected 1         full    auto    10g        
Eth1/4        --                 connected 1         full    auto    10g        
Eth1/5        L3 Link            connected routed    full    1000    10g        
< REDACTED FOR BREVITY>    
Po11          --                 connected trunk     full    1000    --         
Lo1           --                 connected routed    auto    auto    --         
Lo100         --                 connected routed    auto    auto    --         
Vlan1         --                 down      routed    auto    auto    --
Vlan100       mgmt svi - DEMO PL connected routed    auto    auto    --
Vlan101       prod svi - DEMO PL connected routed    auto    auto    --
Vlan102       dev svi - DEMO PLE connected routed    auto    auto    --
Vlan103       test svi - DEMO PL connected routed    auto    auto    --
Vlan104       security svi - DEM connected routed    auto    auto    --
Vlan105       iot svi - DEMO PLE connected routed    auto    auto    --

!!!!!!! show cdp neighbors on sbx-nxos-mgmt.cisco.com at 2019-09-12 22:35:57.305606

Capability Codes: R - Router, T - Trans-Bridge, B - Source-Route-Bridge
                  S - Switch, H - Host, I - IGMP, r - Repeater,
                  V - VoIP-Phone, D - Remotely-Managed-Device,
                  s - Supports-STP-Dispute

Device-ID          Local Intrfce  Hldtme Capability  Platform      Port ID

Total entries displayed: 0

!!!!!!! show int status on sbx-nxos-mgmt.cisco.com at 2019-09-12 22:36:18.511021


--------------------------------------------------------------------------------
Port          Name               Status    Vlan      Duplex  Speed   Type
--------------------------------------------------------------------------------
mgmt0         DO NOT TOUCH CONFI connected routed    full    1000    --         

--------------------------------------------------------------------------------
Port          Name               Status    Vlan      Duplex  Speed   Type
--------------------------------------------------------------------------------
Eth1/1        --                 connected trunk     full    1000    10g        
Eth1/2        --                 connected trunk     full    1000    10g        
Eth1/3        --                 connected 1         full    auto    10g        
Eth1/4        --                 connected 1         full    auto    10g        
Eth1/5        L3 Link            connected routed    full    1000    10g        
< REDACTED FOR BREVITY>  
Po11          --                 connected trunk     full    1000    --         
Lo1           --                 connected routed    auto    auto    --         
Lo100         --                 connected routed    auto    auto    --         
Vlan1         --                 down      routed    auto    auto    --
Vlan100       mgmt svi - DEMO PL connected routed    auto    auto    --
Vlan101       prod svi - DEMO PL connected routed    auto    auto    --
Vlan102       dev svi - DEMO PLE connected routed    auto    auto    --
Vlan103       test svi - DEMO PL connected routed    auto    auto    --
Vlan104       security svi - DEM connected routed    auto    auto    --
Vlan105       iot svi - DEMO PLE connected routed    auto    auto    --

!!!!!!! show cdp neighbors on sbx-nxos-mgmt.cisco.com at 2019-09-12 22:36:19.516013

Capability Codes: R - Router, T - Trans-Bridge, B - Source-Route-Bridge
                  S - Switch, H - Host, I - IGMP, r - Repeater,
                  V - VoIP-Phone, D - Remotely-Managed-Device,
                  s - Supports-STP-Dispute

Device-ID          Local Intrfce  Hldtme Capability  Platform      Port ID

Total entries displayed: 0

!!!!!!! show int status on sbx-nxos-mgmt.cisco.com at 2019-09-12 22:36:35.806752


--------------------------------------------------------------------------------
Port          Name               Status    Vlan      Duplex  Speed   Type
--------------------------------------------------------------------------------
mgmt0         DO NOT TOUCH CONFI connected routed    full    1000    --         

--------------------------------------------------------------------------------
Port          Name               Status    Vlan      Duplex  Speed   Type
--------------------------------------------------------------------------------
Eth1/1        --                 connected trunk     full    1000    10g        
Eth1/2        --                 connected trunk     full    1000    10g        
Eth1/3        --                 connected 1         full    auto    10g        
Eth1/4        --                 connected 1         full    auto    10g        
Eth1/5        L3 Link            connected routed    full    1000    10g        
< REDACTED FOR BREVITY>  
Po11          --                 connected trunk     full    1000    --         
Lo1           --                 connected routed    auto    auto    --         
Lo100         --                 connected routed    auto    auto    --         
Vlan1         --                 down      routed    auto    auto    --
Vlan100       mgmt svi - DEMO PL connected routed    auto    auto    --
Vlan101       prod svi - DEMO PL connected routed    auto    auto    --
Vlan102       dev svi - DEMO PLE connected routed    auto    auto    --
Vlan103       test svi - DEMO PL connected routed    auto    auto    --
Vlan104       security svi - DEM connected routed    auto    auto    --
Vlan105       iot svi - DEMO PLE connected routed    auto    auto    --

!!!!!!! show cdp neighbors on sbx-nxos-mgmt.cisco.com at 2019-09-12 22:36:19.516013

Capability Codes: R - Router, T - Trans-Bridge, B - Source-Route-Bridge
                  S - Switch, H - Host, I - IGMP, r - Repeater,
                  V - VoIP-Phone, D - Remotely-Managed-Device,
                  s - Supports-STP-Dispute

Device-ID          Local Intrfce  Hldtme Capability  Platform      Port ID

Total entries displayed: 0

!!!!!!! show int status on sbx-nxos-mgmt.cisco.com at 2019-09-12 22:36:35.806752


--------------------------------------------------------------------------------
Port          Name               Status    Vlan      Duplex  Speed   Type
--------------------------------------------------------------------------------
mgmt0         DO NOT TOUCH CONFI connected routed    full    1000    --         

--------------------------------------------------------------------------------
Port          Name               Status    Vlan      Duplex  Speed   Type
--------------------------------------------------------------------------------
Eth1/1        --                 connected trunk     full    1000    10g        
Eth1/2        --                 connected trunk     full    1000    10g        
Eth1/3        --                 connected 1         full    auto    10g        
Eth1/4        --                 connected 1         full    auto    10g        
Eth1/5        L3 Link            connected routed    full    1000    10g        
< REDACTED FOR BREVITY>       
Po11          --                 connected trunk     full    1000    --         
Lo1           --                 connected routed    auto    auto    --         
Lo100         --                 connected routed    auto    auto    --         
Vlan1         --                 down      routed    auto    auto    --
Vlan100       mgmt svi - DEMO PL connected routed    auto    auto    --
Vlan101       prod svi - DEMO PL connected routed    auto    auto    --
Vlan102       dev svi - DEMO PLE connected routed    auto    auto    --
Vlan103       test svi - DEMO PL connected routed    auto    auto    --
Vlan104       security svi - DEM connected routed    auto    auto    --
Vlan105       iot svi - DEMO PLE connected routed    auto    auto    --

!!!!!!! show cdp neighbors on sbx-nxos-mgmt.cisco.com at 2019-09-12 22:36:36.812270

Capability Codes: R - Router, T - Trans-Bridge, B - Source-Route-Bridge
                  S - Switch, H - Host, I - IGMP, r - Repeater,
                  V - VoIP-Phone, D - Remotely-Managed-Device,
                  s - Supports-STP-Dispute

Device-ID          Local Intrfce  Hldtme Capability  Platform      Port ID

Total entries displayed: 0
```

## Full Source

```
from netmiko import ConnectHandler, NetMikoAuthenticationException, NetMikoTimeoutException, logging
from time import sleep
from datetime import datetime
from sys import argv
from functools import partial
from multiprocessing import Pool
from yaml import safe_load

import getpass


def print_output(device_result):

    for i in range(len(device_result['results'])):

        print('\n!!!!!!! {} on {} at {}\n\n{}'.format(device_result['commands'][i],
                                                device_result['hostname'],
                                                device_result['timestamps'][i],
                                                device_result['results'][i]))


def write_output(device_result):

    with open('netwatch_output_{}.log'.format(device_result['hostname']), 'a') as outfile:

        for i in range(len(device_result['results'])):

            outfile.write('\n!!!!!!! {} on {} at {}\n\n{}'.format(device_result['commands'][i],
                                                    device_result['hostname'],
                                                    device_result['timestamps'][i],
                                                    device_result['results'][i]))


def execute_commands(device_settings, username, password):

    """
        Runs commands on a device and returns a dictionary object with the device name and the results
    """

    output = []
    timestamps = []

    try:

        ssh_session = ssh_connect(device_settings['hostname'], device_settings['device_type'],
                                device_settings['port'], username, password)

    # write any exceptions to output so they are recorded in the results
    except Exception as e:

        output = ['Exception occured before SSH connection: {}'.format(e)] * len(device_settings['commands'])
        timestamps = [datetime.now()] * len(device_settings['commands'])

    # only executes if no exceptions occur
    else:

        for command in device_settings['commands']:

            try:

                output.append(ssh_session.send_command(command))

            except IOError:

                output.append('COMMAND TIMED OUT')

            except Exception as e:

                output.append('Exception after SSH connection: {}'.format(e))
            
            finally:

                timestamps.append(datetime.now())

    device_result = {
        'hostname': device_settings['hostname'],
        'commands': device_settings['commands'],
        'results': output,
        'timestamps': timestamps
    }

    return device_result


def ssh_connect(hostname, device_type, port, username, password):

    """
        connects to a device and returns a netmiko ssh object
    """

    device = {
        'device_type': device_type,
        'ip': hostname,
        'username': username,
        'password': password,
        'port': port
    }

    return ConnectHandler(**device)


def get_validate_credentials(hostname, device_type, port):

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

            test_ssh_session = ssh_connect(hostname, device_type, port, username, password)
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


def merge_settings(device, script_config):

    ''' merges the default and device specific dictionaries '''

    device_settings = script_config['default'].copy()
    device_settings.update(device)

    return device_settings


def set_device_settings(script_config):

    '''
        creates an array of devices containing device specific
        script configuration
    '''

    device_settings = []

    for device in script_config['device_list']:

        device_setting = merge_settings(device, script_config)
        device_settings.append(device_setting)

    return device_settings


def main():

    try:

        config_file_name = argv[1]

    except IndexError:

        config_file_name = 'netwatch.yml'

    # pull data from config file
    script_config = safe_load(open(config_file_name))

    # create the device settings list
    device_settings = set_device_settings(script_config)

    # get valid credentials from the user
    username, password = get_validate_credentials(device_settings[0]['hostname'], device_settings[0]['device_type'], device_settings[0]['port'])
    
    iter = 0
    while script_config['max_iter'] == 0 or script_config['max_iter'] > iter:

        print('running commands')

        # execute on each device in the device list in parallel 
        with Pool(script_config['threads']) as pool:

            # create a partial function, then use pool.map passing in the device_settings list
            device_results = pool.map(partial(execute_commands,
                                            username=username,
                                            password=password),
                                device_settings)

        iter += 1

        # Iterate over our device_results and write it to a file/print to screen
        for device_result in device_results:

            if script_config['file_output']:

                try:

                    write_output(device_result)

                except Exception as e:

                    print('Exception occured while writing to file for {}'.format(device_result['hostname']))
                    print(e)

            if script_config['print_output']:

                    print_output(device_result)

        print('loop has excuted {} time(s), last execution completed at {}'.format(iter, datetime.now()))
        print('maxium iterations is {} (when set to 0 loop executes forever)'.format(script_config['max_iter']))

        if script_config['max_iter'] > iter:

            print('sleeping for {} seconds (CTRL+C to quit)'.format(script_config['sleep_time']))
            sleep(script_config['sleep_time'])

main()
```