title: How I Automate - Concurrency
published: 2019-08-01
category:
- Automation
- Programming
author: Brandon James
summary: Interacting with Network Devices can often be I/O limited. A function runs, waits for a response from the device, then another function runs so on and so forth. This is made worse by the fact that scripts are often run against multiple devices. After all the purpose of scripting is to speed up repetitive tasks. 

Interacting with Network Devices can often be I/O limited. A function runs, waits for a response from the device, then another function runs so on and so forth. This is made worse by the fact that scripts are often run against multiple devices. After all the purpose of scripting is to speed up repetitive tasks. 

One of the scripts I maintain is used to test the POTS lines my enterprise uses for out-of-band connectivity at our branches and call centers. Dial-up modems are slow, you make a call, the line rings, remote end picks up, the modems eventually train up and you finally get a connection. With some of our international locations I've seen this process take nearly a full minute. Before I added multiprocessing, this script could take over 2 hours to complete. Now it finishes in roughly 20 minutes.

I typically write scripts without concurrency first, using my little 3560-CX as a test device. Once the script is complete, I write a bit of logic to execute the script against multiple devices simultaneously. That logic is discussed below.

### Using the Multiprocessing Library

Python provides two easy ways to add concurrency to your scripts. The first is [threading](https://docs.python.org/3/library/threading.html) and the second is [multiprocessing](https://docs.python.org/3/library/multiprocessing.html). I use the multiprocessing primarily because it offers an extremely convenient function called 'Pool'. There are technical reason to use one over the other. Python has something called the Global Interpreter Lock or GIL. The GIL prevents more than one thread from controlling the Python interpreter at any given time. This means that for any CPU bound tasks, threading won't provide much of a speedup. The multiprocessing library works around this by spawning one Python process per thread. Since Network Automation is IO bound, one could use the threading library, but I don't mind the extra overhead and enjoy the convenience of the pool function.

#### functools.partial()

Partial takes a function and list of values (corresponding to the arguments the function takes) as input and then returns a new function with those arguments statically assigned.

```python
from functools import partial

def sum_four_digits(num1, num2, num3, num4):
    print num1 + num2 + num3 + num4
    
partial_one_free_variable = partial(sum_four_digits, 1, 2, 3)
partial_no_free_variables = partial(sum_four_digits, 1, 2, 3, 4)
```

Calling these two functions results in the following:

```
>>> partial_one_free_variable(0)
6
>>> partial_one_free_variable(4)
10
>>> partial_no_free_variables()
10
```

partial\_no\_free\_variables() will always use num1 = 1, num2 = 2, num3 = 3 and num4 = 4. Likewise, partial\_one\_free\_variable will always use num1 = 1, num2 = 2 and num3 = 3. In this case, partial\_one\_free\_variable ends up just adding 6 to whatever number we call it with. 

My typical use case in scripting is to create functions that already have the username and password set so I can spawn processes using multiprocessing.pool().

```python
import getpass, partial

def my_network_automation_function(script_settings, username, password):

	pass
	
if __name__ == '__main__':

	username = getpass.getuser()
	password = getpass.getpass()
	
	partial_function = partial(my_network_automation_function, username = username, password = password)
```

#### pool.map()

Map takes a function and an iterable as input, then based on the number of processes you've given it, it cuts the iterable (of length _n_) into _n/processes_ chunks and then executes them in order. Putting this together with our previous example, we get:

```python
from functools import partial
from time import sleep
from multiprocessing import Pool

def sum_four_digits(num1, num2, num3, num4):
    print('sleep for four seconds')
    sleep(4)
    print(num1 + num2 + num3 + num4)
    
if __name__ == '__main__':
    
    partial_one_free_variable = partial(sum_four_digits, 1, 2, 3)
    numbers = [0, 1, 2, 3, 5, 6, 7, 8]

    number_of_processes = 4

    with Pool(number_of_processes) as pool:
        pool.map(partial_one_free_variable, numbers)
```

I added sleep(4) to sum_four_digits in order to make the multiprocessing impact more obvious. The result of running this is as follows:

```bash
[bjames@lws1 ~]$ ./venv3/bin/python threaded.py 
sleep for four seconds
sleep for four seconds
sleep for four seconds
sleep for four seconds
8
sleep for four seconds
6
sleep for four seconds
7
9
sleep for four seconds
sleep for four seconds
11
12
13
14
```

While the execution is in order, we don't get the results in order. This is because computers do a lot and when 4 threads start up simultaneously there is no way to determine which one is going to finish first. This isn't of much concern for two reasons.  

1. When automating network tasks, it's unlikely that your threads will complete at the same time. Different devices will take different amount of times to complete.

2. The map function handles this extremely well. If a result is returned from the function called using pool.map(). The results are stored in an array in the order of execution (as opposed to the order of completion). 

I've modified our example above to illustrate this:

```python
from functools import partial
from time import sleep
from multiprocessing import Pool

def sum_four_digits(num1, num2, num3, num4):

    return num1 + num2 + num3 + num4
    
def main():
    
    partial_one_free_variable = partial(sum_four_digits, 1, 2, 3)
    numbers = [0, 1, 2, 3, 5, 6, 7, 8]

    number_of_processes = 4

    with Pool(number_of_processes) as pool:
        results = pool.map(partial_one_free_variable, numbers)

    print(results)

main()
```

Which yields the following:

```bash
[bjames@lws1 ~]$ ./venv3/bin/python threaded.py 
[6, 7, 8, 9, 11, 12, 13, 14]
```

pool.map() waits until all processes have completed before returning. For automation, that's generally what I want. Just for awareness, I'll mention that pool.map_async() returns a MapResult object immediately. This allows you to execute other code in your parent processes, but you still won't be able to operate on the results until all the processes have terminated. There are cases where this can be useful. 

I won't go into much detail, but the use of pool.map_async() is shown below:

```python
with Pool(number_of_processes) as pool:

    results = pool.map_async(partial_one_free_variable, numbers)

    print('we are now executing other code')

    # prints the results once they are avaliable
    print(results.get())
```

This results in roughly the same thing as the pool.map() function, but to get the results, we call results.get() which waits for the result to be available, then it returns it. There are ways to share data between threads, which could be used to act on data as soon as it's available, but that's not in the scope of this post. 

### Structuring your Code for Concurrency
Parallel code has to be structured differently than serial code. There are times where you can simply use pool.map() to call the function you want to use multiprocessing on and as I mentioned before, I don't add concurrency until the very end. However, there are some things you should keep in mind as you work.

#### Validate your credentials before spawning processes
In my organization, our scripts generally aren't run by any sort of automated process. They tend to be run under a user's account who has R/W access to the network devices being modified. During the change window, the user logs on, runs the script which then prompts them for credentials (this isn't entirely true - I've written a submodule that gets the credentials ahead of time and simply sleeps until the change window). The worst thing that could happen at this point is for the script to try to log on to 8 devices simultaneously and locking out their account because they accidentally hit caps lock.

In order to avoid that situation, I use a function called get_validate_credentials(), which returns credentials that we know are valid:

```python
def get_validate_credentials(device):

    ''' 
        gets username and password, opens an ssh session to verify the credentials, then closes the ssh session
        returns username and password
        Doing this prevents multiple threads from locking out an account due to mistyped creds
    '''

    # attempts to get the username, prompts if needed
    username = getpass.getuser()

    # prompts user for password
    password = getpass.getpass()

    authenticated = False

    while not authenticated:

        try:
            
            test_ssh_session = ssh_connect(device, username, password)
            test_ssh_session.disconnect()

        except NetMikoAuthenticationException:

            print 'authentication failed on ' + device + ' (CTRL + C to quit)'

            username = raw_input('Username: ')
            password = getpass.getpass()

        except NetMikoTimeoutException:

            print 'SSH timed out on ' + device
            raise

        else:

            # if there is no exception set authenticated to true
            authenticated = True

    return username, password
```

#### Make the number of threads configurable
Different scenarios call for a different number of threads. For instance, I regularly run our IOS upgrade script with a single thread, because if I'm upgrading a single site I want to do the closet switches before the distribution switches, otherwise I may end up rebooting the distribution while the new code is still being transferred to the closets. I typically use [YAML for script configuration](https://neverthenetwork.com/notes/automation_config). 

#### Shore up your exception handling
Exceptions occur on a per process basis (at least using the pool.map() function). Some of my scripts connect to devices more than once during the execution and often in different threads. If an exception occurs early on in the script, I don't want to allow later parts of the script to run against that device, but I do want the script to continue executing.

I'll often use an array of dictionaries to store both the results and settings of the script. Within that dictionary, I keep track of any exceptions that occur within my child threads. A simple example of this follows:

```python

from functools import partial
from time import sleep
from multiprocessing import Pool
from random import randint

def snooze(sleep_time):

    '''
        calls time.sleep() using sleep_time as the amount of time to sleep
        raises a value error if we try to sleep more than 5 seconds
    '''

    if sleep_time > 5:

        raise ValueError("We can't sleep in!")

    sleep(sleep_time)

def sum_four_digits(num1, num2, num3, function_values):

    '''
        takes three numbers and a dictionary as input
        the dictionary MUST have a key called number containing an int
        otherwise a KeyError will be raised
    '''


    sleep_time = randint(1,10)
    
    try:

        snooze(sleep_time)

    # if you need the exception message, it can be added to the dictionary as well
    except ValueError as e:

        function_values['exception'] = e

    else:
        
        try:
            
            function_values['sum'] = num1 + num2 + num3 + function_values['number']

        # note the we don't have to keep the exception text
        except KeyError as e:

            function_values['exception'] = e

    finally:

        return function_values
    
def main():

    # in practice this would be imported from a YAML file
    script_values = [
                        {'number': 0},
                        {'number': 1},
                        {'number': 2},
                        {'number': 3},
                        {'number': 4},
                        {'numbers': 5},
                        {'number': 6},
                        {'number': 7},
                        {'number': 8}
                    ]

    number_of_processes = 4

    with Pool(number_of_processes) as pool:
        
        # call map on a copy of sum_four_digits() where 1, 2 and 3 are already set
        script_values = pool.map(partial(sum_four_digits, 1, 2, 3), script_values)

    for value in script_values:

        # This key only exists if an exception occurred
        if value.get('exception') is not None:

            print(repr(value['exception']))

        else:

            print('1 + 2 + 3 + ' + str(value['number']) + ' = ' + str(value['sum']))

main()

```

If you run the code above, you might get something like the following:

```bash
[bjames@lws1 ~]$ ./venv3/bin/python threaded.py 
1 + 2 + 3 + 0 = 6
ValueError("We can't sleep in!")
1 + 2 + 3 + 2 = 8
ValueError("We can't sleep in!")
ValueError("We can't sleep in!")
KeyError('number')
1 + 2 + 3 + 6 = 12
ValueError("We can't sleep in!")
1 + 2 + 3 + 8 = 14
```

This results in us being able to either take actions due to an error that occurred on a device or avoid applying further changes to that device. 

#### Putting it all together

I've written a simple script to update existing ACLs on both IOS and NXOS to illustrate how this works in the context of Network Automation. This is actually very similar to the script I wrote to automate ACL pushes at work. In this script we:

1. Read the scripts configuration from a YAML file

2. Prompt for credentials

3. Verify the credentials are valid (using a submodule that's similar to the example I gave earlier)

4. Spawn _n_ processes based on the script's configuration

5. Simultanuously update the ACLs on _n_ devices

6. Print the results to the screen. Here I just used Pretty Print, but at work I'll often have the script send an email upon completion. 

```python
from multiprocessing import Pool
from functools import partial
from contextlib import contextmanager
from netmiko import NetMikoTimeoutException, ConnectHandler
from yaml import safe_load
from pprint import pprint

from bjames_netmiko_auth.bjames_netmiko_auth import get_valid_credentials

def connect_ssh(hostname, device_type, username, password):

    device = {
        'device_type': device_type,
        'ip': hostname,
        'username': username,
        'password': password
    }

    return ConnectHandler(**device)


def nxos_mod_acl(ssh_session, device, acl_name, acl_lines):

    # remove the old ACL
    ssh_session.send_config_set('no ip access-list {}'.format(acl_name))

    # create the config set for the new ACL
    config_set = ['ip access-list {}'.format(acl_name)]
    config_set = config_set + acl_lines.splitlines()

    ssh_session.send_config_set(config_set)

    result = ssh_session.send_command('show ip access-list {}'.format(acl_name))

    return result


def ios_mod_acl(ssh_session, device, acl_name, acl_lines):

    # remove the old ACL
    ssh_session.send_config_set('no ip access-list extended {}'.format(acl_name))

    # create the config set for the new ACL
    config_set = ['ip access-list extended {}'.format(acl_name)]
    config_set = config_set + acl_lines.splitlines()

    ssh_session.send_config_set(config_set)

    result = ssh_session.send_command('show ip access-list {}'.format(acl_name))

    return result


def mod_acl(acl_name, acl_lines, username, password, device):

    try:

        ssh_session = connect_ssh(device['hostname'], device['device_type'], username, password)

    except Exception as e:

        print('error {}'.format(device['hostname']))
        return {'device': device['hostname'], 'result': e}


    try:

        if device['device_type'] == 'cisco_ios':

            result = ios_mod_acl(ssh_session, device, acl_name, acl_lines)

        elif device['device_type'] == 'cisco_nxos':

            result = nxos_mod_acl(ssh_session, device, acl_name, acl_lines)

    except Exception as e:

        print('error {}'.format(device['hostname']))
        return {'device': device['hostname'], 'result': e}

    print('{} completed'.format(device['hostname']))

    return {'device': device['hostname'], 'result': result}


def main():

    script_settings = safe_load(open('mod_acl.yml'))
    username, password = get_valid_credentials(admin=True)

    with Pool(script_settings['threads']) as pool:

        results = pool.map(partial(mod_acl,
                         script_settings['acl_name'],
                         script_settings['acl_lines'],
                         username,
                         password),
                 script_settings['device_list'])

    pprint(results)
```

And here's an example configuration file:

```yaml
# The name of the ACL
threads: 8
# valid device types are cisco_ios and cisco_nxos
device_list:
    - hostname: BRANCH1_DIST1
      device_type: cisco_ios
    - hostname: BRANCH1_DIST2
      device_type: cisco_ios
    - hostname: DC1_CORE1
      device_type: cisco_nxos
    - hostname: DC1_CORE2
      device_type: cisco_nxos
acl_name: LOCK_IT_DOWN
acl_lines: |
 remark Utility Server A
 permit ip host 192.168.1.100 any
 remark Allowed Subnet
 permit ip 192.168.10.0 0.0.0.255 any
```

I hope this post has been both valuable and informative. If you have any questions or comments, please don't hesitate to send me an [email](mailto:brandon@neverthenetwork.com).
