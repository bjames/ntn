import subprocess

from .ntnutil import validate_ip_or_hostname


def ping_host(hostname, count=10, deadtime=5):

    ping_response = subprocess.Popen(["/bin/ping", '-c{}'.format(count), '-w{}'.format(deadtime), hostname], stdout=subprocess.PIPE).stdout.read()

    ping_response = ping_response.decode('ascii')

    return ping_response


def ping(hostname, count = 10, deadtime = 5):

    try:
        
        validated_hostname = validate_ip_or_hostname(hostname)

    except ValueError as e:

        return e

    ping_response = subprocess.Popen(["/bin/ping", '-c{}'.format(count), '-w{}'.format(deadtime), validated_hostname], stdout=subprocess.PIPE).stdout.read()

    ping_response = ping_response.decode('ascii')

    return ping_response


if __name__ == '__main__':

    test_cases = ['wowowowow wowow', 'rm -rf', 'wow.wow', '192.168.88.1', '192.168', 'google.com rm']

    for case in test_cases:

        print(case)
        print(ping(case))

