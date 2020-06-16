import re
from ipaddress import ip_address

def validate_ip_or_hostname(hostname):

    # ip address validation is done using the ipaddress module because it's easy
    ip = True


    try:

        ip_address(hostname)

    except ValueError:

        ip = False 

    # Try the IP first, if that doesn't work, we use the domain name
    if ip:

        return hostname

    else:
    
        # here we accept anything that is '.' seperated with no other non-alpha numeric characted
        domain_name = re.match(r'(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9][a-z0-9-]{0,61}[a-z0-9]', hostname)

        if domain_name:

            return domain_name.group()

    raise ValueError('Not a valid IP address or domain name')
