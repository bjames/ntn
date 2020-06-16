from whois import whois
from ipwhois import IPWhois
from ipaddress import ip_address

def ntnwhois(hostname):

    try:
        ip_addr = ip_address(hostname)
        ip_whois = IPWhois(ip_addr)
        return(ip_whois.lookup_rdap(depth=1))
    except ValueError:
        print('attr')
        return(whois(hostname))
