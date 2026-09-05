

import tkinter as tk
from tkinter import messagebox


# ---------- CORE LOGIC (same as CLI version) ----------

def ip_to_binary(ip):
    octets = ip.split('.')
    return ''.join([format(int(octet), '08b') for octet in octets])


def binary_to_ip(binary):
    octets = [str(int(binary[i:i + 8], 2)) for i in range(0, 32, 8)]
    return '.'.join(octets)


def cidr_to_mask_binary(cidr):
    return '1' * cidr + '0' * (32 - cidr)


def get_cidr_from_input(mask_input):
    if '.' in mask_input:
        return ip_to_binary(mask_input).count('1')
    return int(mask_input)


def calculate_subnet(ip, cidr):
    ip_bin = ip_to_binary(ip)
    mask_bin = cidr_to_mask_binary(cidr)

    network_bin = ''.join(
        '1' if ip_bin[i] == '1' and mask_bin[i] == '1' else '0'
        for i in range(32)
    )
    broadcast_bin = network_bin[:cidr] + '1' * (32 - cidr)

    network_ip = binary_to_ip(network_bin)
    broadcast_ip = binary_to_ip(broadcast_bin)

    host_bits = 32 - cidr
    total_hosts = 2 ** host_bits

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


# ---------- GUI PART ----------

def on_calculate():
    ip = ip_entry.get().strip()
    mask_input = mask_entry.get().strip()

    try:
        cidr = get_cidr_from_input(mask_input)
        result = calculate_subnet(ip, cidr)

        output_text = (
            f"Subnet Mask       : {result['subnet_mask']}  (/{cidr})\n"
            f"Network Address   : {result['network']}\n"
            f"Broadcast Address : {result['broadcast']}\n"
            f"First Usable Host : {result['first_host']}\n"
            f"Last Usable Host  : {result['last_host']}\n"
            f"Total Hosts       : {result['total_hosts']}\n"
            f"Usable Hosts      : {result['usable_hosts']}"
        )
        result_label.config(text=output_text, justify="left")

    except Exception as e:
        messagebox.showerror("Error", f"Sahi IP aur mask/CIDR daaliye.\n({e})")


# Window setup
window = tk.Tk()
window.title("Subnet Calculator")
window.geometry("400x400")
window.resizable(False, False)

tk.Label(window, text="Subnet Calculator", font=("Arial", 16, "bold")).pack(pady=10)

tk.Label(window, text="IP Address (e.g. 192.168.1.10):").pack()
ip_entry = tk.Entry(window, width=30)
ip_entry.pack(pady=5)

tk.Label(window, text="CIDR (24) or Mask (255.255.255.0):").pack()
mask_entry = tk.Entry(window, width=30)
mask_entry.pack(pady=5)

tk.Button(window, text="Calculate", command=on_calculate, bg="#4CAF50", fg="white").pack(pady=10)

result_label = tk.Label(window, text="", font=("Courier", 10), justify="left")
result_label.pack(pady=10)

window.mainloop()