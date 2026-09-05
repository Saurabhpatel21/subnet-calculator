
def ip_to_binary(ip):
    """IP address (jaise '192.168.1.10') ko 32-bit binary string mein badalta hai."""
    octets = ip.split('.')
    binary = ''.join([format(int(octet), '08b') for octet in octets])
    return binary


def binary_to_ip(binary):
    """32-bit binary string ko wapas IP address format mein badalta hai."""
    octets = [str(int(binary[i:i + 8], 2)) for i in range(0, 32, 8)]
    return '.'.join(octets)


def cidr_to_mask_binary(cidr):
    """CIDR number (jaise 24) ko 32-bit binary mask mein badalta hai.
    Example: /24 -> 11111111.11111111.11111111.00000000
    """
    return '1' * cidr + '0' * (32 - cidr)


def calculate_subnet(ip, cidr):
    """Main calculation logic."""
    ip_bin = ip_to_binary(ip)
    mask_bin = cidr_to_mask_binary(cidr)

    # STEP 1: Network Address = IP AND Mask (bit by bit)
    network_bin = ''.join(
        '1' if ip_bin[i] == '1' and mask_bin[i] == '1' else '0'
        for i in range(32)
    )

    # STEP 2: Broadcast Address = Network bits same, host bits sab '1'
    broadcast_bin = network_bin[:cidr] + '1' * (32 - cidr)

    network_ip = binary_to_ip(network_bin)
    broadcast_ip = binary_to_ip(broadcast_bin)

    # STEP 3: Total hosts = 2^(host bits)
    host_bits = 32 - cidr
    total_hosts = 2 ** host_bits

    # STEP 4: Usable hosts = total - 2 (network + broadcast reserved)
    # /31 aur /32 special cases hote hain (point-to-point / single host)
    if cidr <= 30:
        usable_hosts = total_hosts - 2
        first_host = binary_to_ip(format(int(network_bin, 2) + 1, '032b'))
        last_host = binary_to_ip(format(int(broadcast_bin, 2) - 1, '032b'))
    else:
        usable_hosts = total_hosts
        first_host = network_ip
        last_host = broadcast_ip

    return {
        'subnet_mask': binary_to_ip(mask_bin),
        'network': network_ip,
        'broadcast': broadcast_ip,
        'first_host': first_host,
        'last_host': last_host,
        'total_hosts': total_hosts,
        'usable_hosts': usable_hosts,
    }


def get_cidr_from_input(mask_input):
    """User CIDR (24) ya dotted mask (255.255.255.0) dono de sakta hai — dono handle karte hain."""
    if '.' in mask_input:
        mask_bin = ip_to_binary(mask_input)
        return mask_bin.count('1')
    return int(mask_input)


def main():
    print("=" * 40)
    print("       SUBNET CALCULATOR (CLI)")
    print("=" * 40)

    ip = input("Enter IP address (e.g. 192.168.1.10): ").strip()
    mask_input = input("Enter CIDR (e.g. 24) or mask (e.g. 255.255.255.0): ").strip()

    try:
        cidr = get_cidr_from_input(mask_input)
        result = calculate_subnet(ip, cidr)

        print("\n--- RESULT ---")
        print(f"IP Address        : {ip}")
        print(f"Subnet Mask       : {result['subnet_mask']}  (/{cidr})")
        print(f"Network Address   : {result['network']}")
        print(f"Broadcast Address : {result['broadcast']}")
        print(f"First Usable Host : {result['first_host']}")
        print(f"Last Usable Host  : {result['last_host']}")
        print(f"Total Hosts       : {result['total_hosts']}")
        print(f"Usable Hosts      : {result['usable_hosts']}")

    except Exception as e:
        print(f"Error: {e}. Sahi IP aur mask/CIDR daaliye.")


if __name__ == "__main__":
    main()