DNS_ROOT_SERVERS = [
    {'name': 'a.root-servers.net', 'ip': '198.41.0.4'},
    {'name': 'b.root-servers.net', 'ip': '199.9.14.201'},
    {'name': 'c.root-servers.net', 'ip': '192.33.4.12'},
    {'name': 'd.root-servers.net', 'ip': '199.7.91.13'},
    {'name': 'e.root-servers.net', 'ip': '192.203.230.10'},
    {'name': 'f.root-servers.net', 'ip': '192.5.5.241'},
    {'name': 'g.root-servers.net', 'ip': '192.112.36.4'},
    {'name': 'h.root-servers.net', 'ip': '198.97.190.53'},
    {'name': 'i.root-servers.net', 'ip': '192.36.148.17'},
    {'name': 'j.root-servers.net', 'ip': '192.58.128.30'},
    {'name': 'k.root-servers.net', 'ip': '193.0.14.129'},
    {'name': 'l.root-servers.net', 'ip': '199.7.83.42'},
    {'name': 'm.root-servers.net', 'ip': '202.12.27.33'}
]

DNS_RESOLVER_LIST = [
    {'name': 'Google', 'ip': '8.8.8.8'},
    {'name': 'Level3', 'ip': '4.2.2.2'},
    {'name': 'CloudFlare', 'ip': '1.1.1.1'},
    {'name': 'Quad9', 'ip': '9.9.9.9'},
    {'name': 'OpenDNS', 'ip': '208.67.222.222'},
    {'name': 'Verisign', 'ip': '64.6.64.6'},
    {'name': 'AdGuard', 'ip': '176.103.130.130'},
    {'name': 'SafeDNS', 'ip': '195.46.39.39'},
    {'name': 'CleanBrowsing Security Filter', 'ip': '185.228.168.9'},
    {'name': 'CleanBrowsing Adult Filter', 'ip': '185.228.168.10'},
    {'name': 'CleanBrowsing Family Filter', 'ip': '185.228.168.168'},
    {'name': 'NeustarDNS Threat Prevention', 'ip': '156.154.70.2'},
    {'name': 'NeustarDNS Family Secure', 'ip': '156.154.70.3'},
    {'name': 'NeustarDNS Business Secure', 'ip': '156.154.70.4'},
]

DNS_RECORD_TYPES = [
    'A', 'AAAA', 'CNAME', 'CAA', 'MX', 'NS', 'PTR', 'SOA', 'SRV', 'TXT'
]

OUI_FILES = [
    {'url': 'http://standards-oui.ieee.org/oui/oui.csv', 'oui_length': 6, 'table_name': 'OUI_MAL'},
    {'url': 'http://standards-oui.ieee.org/oui28/mam.csv', 'oui_length': 7, 'table_name': 'OUI_MAM'},
    {'url': 'http://standards-oui.ieee.org/oui36/oui36.csv', 'oui_length': 9, 'table_name': 'OUI_MAS'},
    {'url': 'http://standards-oui.ieee.org/cid/cid.csv', 'oui_length': 6, 'table_name': 'OUI_CID'},
    {'url': 'http://standards-oui.ieee.org/iab/iab.csv', 'oui_length': 9, 'table_name': 'OUI_IAB'}
]

DATABASE = 'sqlite:///ntntools/ntn.db'

DATABASE_KEY = 'Th!s !s n0t cUst0mer Data'