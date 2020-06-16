import ipaddress

from warnings import filterwarnings
from numpy import uint32, bitwise_and, bitwise_xor

def calculate_hash(rp_address, group, mask):

    """
        Implements the PIM SM hash algorithm defined in RFC 7761 as:

        Value(G,M,C(i))=
            (1103515245 * ((1103515245 * (G&M)+12345) XOR C(i)) + 12345) mod 2^31
    """

    filterwarnings("ignore", category=RuntimeWarning)

    result = uint32(bitwise_and(group,mask))
    result = uint32(uint32(1103515245) * uint32(result) + uint32(12345))
    result = uint32(bitwise_xor(result, rp_address))
    result = uint32(uint32(1103515245) * uint32(result))
    result = uint32(uint32(result) + uint32(12345))
    result = uint32(uint32(result) % uint32(2**31))

    return str(result)

def ntnrphash(rp_address, group, mask_length):

    rp_address = uint32(ipaddress.IPv4Address(rp_address))
    group = uint32(ipaddress.IPv4Address(group))
    mask_length = uint32(mask_length)
    mask = uint32((2**mask_length) - 1 << 32-mask_length)

    return(calculate_hash(rp_address, group, mask))