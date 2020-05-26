title: How I Automate - Script Configuration using YAML
published: 2019-02-17
category:
- Automation
author: Brandon James
summary: Code reuse is an important part of scripting. You should avoid needing to modify your script each time you run it. This is one way of doing so.

In the past when I was using TCL/Expect as my primary automation language, I would do most of my configuration within the script itself and then I'd just have the script grab a list of devices from a text document. Lately, I've been using YAML to provide both my list of devices and to configure various parameters within the script itself. 

### The YAML file

I'm not going to go into the details of what YAML is, or how exactly it works. Because it's incredibly easy to pick up, if you don't get the gist of it from my examples or just want more details, checkout [yaml.org](https://yaml.org/) and the [wikipedia entry on YAML](https://en.wikipedia.org/wiki/YAML). I'm using my [IOS Upgrade script's](https://github.com/bjames/ios_upgrade) YAML file  as an example.

```yaml
email_recipient: brandon@brandonsjames.com
# specify how many devices to upgrade at a single time (note, this is also the number of threads spawned at runtime)
threads: 1
# disruptive parts of the script will run at this time, leave blank to run immediately. Format HH:MM
change_time: '23:00'
# if set to true, the new image will copied to the device prior to the change
pre_copy: True
# default settings that may be overridden on a per device basis
default:
  # directory storing the IOS image
  remote_directory: http://192.168.0.113/
  # full IOS/NXOS filename (ie c3560cx-universalk9-mz.152-4.E4.bin)
  image_name: c2960-lanlitek9-mz.122-55.SE12.bin
  # md5 may be left blank to skip verification
  image_md5: 1ac4728753bb11ad6f22fd8f54763f8e
  # if true, invalid confregs will be set to 0x2102. Otherwise an exception will be raised. 
  fix_confreg: True
  # if true, device will be reloaded. If false code will only be copied
  install: True
  # maximum amount of time to wait (in seconds) before throwing an exception after reload command has been issued
  reload_max_time: 24000
  # some device images may not support the reload /verify command. It can be disabled here.
  reload_verify: False
  # perform a shelf reload for dual SUP devices in RPR mode
  reload_shelf_rpr: False
  # acceptable confreg settings
  confreg:
  - '0xF'
  - '0x2102'
  - '0x102'
# list devices and device specific config
target_devices:
 - hostname: 192.168.0.150
   image_name: c2960-lanlitek9-mz.150-2.SE11.bin
   image_md5: 885ed3dd7278baa11538a51827c2c9f8
 - hostname: 192.168.0.11
 - hostname: 192.168.10.11
   install: False
```

As you can see, I allow device specific configuration for a number of settings. I've found this to really increase the flexibility of my scripts. Generally, I try to make my scripts as reusable as possible and this type of flexibility keeps me from needing to write separate scripts for slight changes in device types or use cases. As you write your script you'll need to think about what can and cannot be different on a per device basis. 

### The Python Script
I load all the values from the YAML file into a python dictionary. I then use a function called merge_settings() to combine the default settings from the YAML with any device specific overrides and place the results into a list of dictionaries:

```python
import yaml

from pprint import pprint

def merge_settings(device, script_config):

    ''' merges the default and device specific dictionaries '''

    script_settings = script_config['default'].copy()
    script_settings.update(device)

    return script_settings


def set_script_settings(script_config):

    '''
        creates an array of devices containing device specific
        script configuration
    ''' 

    script_settings = []
    
    for device in script_config['target_devices']:

        device_settings = merge_settings(device, script_config)
        script_settings.append(device_settings)

    return script_settings


def main():

    # pull data from config file
    script_config = yaml.safe_load(open("script_config.yml"))


    print('________________RAW DICT______________')
    pprint(script_config)

    script_settings = set_script_settings(script_config)

    print('_______________MERGED DICT_____________')
    pprint(script_settings)
    
main()
```

*Note: pprint is only included to print our dictionary and list of dictionaries to the screen*

When this script is executed the following is output on the terminal:

```bash
[bjames@lws1 ~]$ venv3/bin/python import_script_settings.py 
________________RAW DICT______________
{'change_time': '23:00',
 'default': {'confreg': ['0xF', '0x2102', '0x102'],
             'fix_confreg': True,
             'image_md5': '1ac4728753bb11ad6f22fd8f54763f8e',
             'image_name': 'c2960-lanlitek9-mz.122-55.SE12.bin',
             'install': True,
             'reload_max_time': 24000,
             'reload_shelf_rpr': False,
             'reload_verify': False,
             'remote_directory': 'http://192.168.0.113/'},
 'email_recipient': 'brandon@brandonsjames.com',
 'pre_copy': True,
 'target_devices': [{'hostname': '192.168.0.150',
                     'image_md5': '885ed3dd7278baa11538a51827c2c9f8',
                     'image_name': 'c2960-lanlitek9-mz.150-2.SE11.bin'},
                    {'hostname': '192.168.0.11'},
                    {'hostname': '192.168.10.11', 'install': False}],
 'threads': 1}
_______________MERGED DICT_____________
[{'confreg': ['0xF', '0x2102', '0x102'],
  'fix_confreg': True,
  'hostname': '192.168.0.150',
  'image_md5': '885ed3dd7278baa11538a51827c2c9f8',
  'image_name': 'c2960-lanlitek9-mz.150-2.SE11.bin',
  'install': True,
  'reload_max_time': 24000,
  'reload_shelf_rpr': False,
  'reload_verify': False,
  'remote_directory': 'http://192.168.0.113/'},
 {'confreg': ['0xF', '0x2102', '0x102'],
  'fix_confreg': True,
  'hostname': '192.168.0.11',
  'image_md5': '1ac4728753bb11ad6f22fd8f54763f8e',
  'image_name': 'c2960-lanlitek9-mz.122-55.SE12.bin',
  'install': True,
  'reload_max_time': 24000,
  'reload_shelf_rpr': False,
  'reload_verify': False,
  'remote_directory': 'http://192.168.0.113/'},
 {'confreg': ['0xF', '0x2102', '0x102'],
  'fix_confreg': True,
  'hostname': '192.168.10.11',
  'image_md5': '1ac4728753bb11ad6f22fd8f54763f8e',
  'image_name': 'c2960-lanlitek9-mz.122-55.SE12.bin',
  'install': False,
  'reload_max_time': 24000,
  'reload_shelf_rpr': False,
  'reload_verify': False,
  'remote_directory': 'http://192.168.0.113/'}]
```

As you can see, we've ended up with separate dictionaries for each device. At this point the script_settings list can be iterated over and each element of the list has a dictionary. 

If you aren't familiar with dictionaries, they operate on key-value pairs, wherein in the above pprint output the items to the left of the colon are keys and to the right are the values. I've founding using dictionaries where possible really improves the readability of my code and makes things much easier on me. In the example below, we iterate over the script_settings list and print the hostname and image_name from each of each device. 

```python
for device_settings in script_settings:
    
    print(device_settings['hostname'])
    print(device_settings['image_name'])
```

Which outputs the following:

```
192.168.0.150
c2960-lanlitek9-mz.150-2.SE11.bin
192.168.0.11
c2960-lanlitek9-mz.122-55.SE12.bin
192.168.10.11
c2960-lanlitek9-mz.122-55.SE12.bin
```

I've found handling device specific script configuration in this way has been extremely powerful and a huge improvement over iterating through a file called 'device_list.txt'. 

*Note: This note was originally on my personal blog. I've backdated the post to show the day it was originally written*