import ipaddress


def subnet(ip_address, subnet_mask):

    try:

        if '/' in subnet_mask:

            subnet = (ipaddress.ip_network(ip_address + subnet_mask, strict=False))

        else:

            subnet = (ipaddress.ip_network(ip_address + '/' + subnet_mask, strict=False))


    except ValueError:

        return {'Error': 'Invalid subnet mask or IP address'}


    if subnet.num_addresses == 1:

        return {
            'Network Address': subnet.network_address,        
            'Subnet Mask': subnet.netmask,
            'CIDR': '/{}'.format(subnet.prefixlen),
            'Wildcard Bits': subnet.hostmask,
            'Number of Addresses': subnet.num_addresses,
        }
        
    elif subnet.num_addresses == 2:

        return {
            'Subnet Mask': subnet.netmask,
            'CIDR': '/{}'.format(subnet.prefixlen),
            'Wildcard Bits': subnet.hostmask,
            'Number of Addresses': subnet.num_addresses,
            'First Host': subnet.network_address,
            'Last Host': subnet.broadcast_address,
        }

    else:

        return {
            'Network Address': subnet.network_address,        
            'Subnet Mask': subnet.netmask,
            'CIDR': '/{}'.format(subnet.prefixlen),
            'Wildcard Bits': subnet.hostmask,
            'Broadcast Address': subnet.broadcast_address,
            'Number of Addresses': subnet.num_addresses,
            'First Host': subnet.network_address + 1,
            'Last Host': subnet.broadcast_address - 1,
        }