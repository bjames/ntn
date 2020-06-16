import subprocess

from .ntnutil import validate_ip_or_hostname


def traceroute(hostname):

    try:

        validated_hostname = validate_ip_or_hostname(hostname)

    except ValueError as e:

        return(e)

    try:
        tracepath_response = subprocess.Popen(["/bin/traceroute", validated_hostname], stdout=subprocess.PIPE).stdout.read()
    except FileNotFoundError:
        tracepath_response = subprocess.Popen(["/usr/sbin/traceroute", validated_hostname], stdout=subprocess.PIPE).stdout.read()

    tracepath_response = tracepath_response.decode('ascii')

    return tracepath_response


if __name__ == '__main__':

    test_cases = ['wowowowow wowow', 'rm -rf', 'wow.wow', '192.168.88.1', '192.168', 'google.com rm']

    for case in test_cases:

        print(case)
        print(traceroute(case))