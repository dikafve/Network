import ipaddress

# ===== INPUT =====
alamat_awal = "192.168.1.0/24"
prefix_baru = 26

# ===== PROSES: membentuk objek jaringan dan memecahnya menjadi subnet =====
jaringan = ipaddress.ip_network(alamat_awal, strict=False)
subnet_list = list(jaringan.subnets(new_prefix=prefix_baru))

# ===== PROSES: perhitungan jumlah subnet =====
bit_dipinjam = prefix_baru - jaringan.prefixlen
jumlah_subnet = 2 ** bit_dipinjam

# ===== OUTPUT: informasi awal =====
print("=== INFORMASI JARINGAN AWAL ===")
print(f"Jaringan awal      : {jaringan}")
print(f"Subnet mask awal   : {jaringan.netmask}")
print(f"Prefix baru        : /{prefix_baru}")
print(f"Bit dipinjam       : {bit_dipinjam}")
print(f"Jumlah subnet      : {jumlah_subnet}")

# ===== PROSES: perhitungan host per subnet =====
bit_host = 32 - prefix_baru
total_ip = 2 ** bit_host
host_per_subnet = total_ip - 2

# ===== OUTPUT: informasi host =====
print()
print("=== INFORMASI HOST PER SUBNET ===")
print(f"Bit host           : {bit_host}")
print(f"Total IP/subnet    : {total_ip}")
print(f"Host usable/subnet : {host_per_subnet}")

# ===== LOOP 1: menampilkan subnet valid =====
print()
print("=== DAFTAR SUBNET VALID ===")
for subnet in subnet_list:
    print(f"{subnet.network_address}/{prefix_baru}")

# ===== LOOP 2: tabel alokasi IP =====
kolom = "{:<15}{:<15}{:<15}{:<15}{}"
print()
print("=== TABEL ALOKASI IP ===")
print(kolom.format("Network ID", "Host Pertama", "Host Terakhir",
                   "Broadcast", "Jumlah Host"))
print("-" * 75)
for subnet in subnet_list:
    host_pertama = subnet.network_address + 1
    host_terakhir = subnet.broadcast_address - 1
    jumlah_host = subnet.num_addresses - 2
    print(kolom.format(str(subnet.network_address), str(host_pertama),
                       str(host_terakhir), str(subnet.broadcast_address),
                       jumlah_host))

# ===== FITUR TAMBAHAN: cek IP milik subnet yang mana =====
daftar_uji = ["192.168.1.10", "192.168.1.64", "192.168.1.130",
              "192.168.1.255", "192.168.2.5"]
print()
print("=== CEK KEANGGOTAAN IP DALAM SUBNET ===")
for teks_ip in daftar_uji:
    ip_uji = ipaddress.ip_address(teks_ip)
    ketemu = False
    for subnet in subnet_list:
        if ip_uji in subnet:
            if ip_uji == subnet.network_address:
                peran = "Network ID"
            elif ip_uji == subnet.broadcast_address:
                peran = "Broadcast"
            else:
                peran = "Host valid"
            print(f"{teks_ip:<15} -> {subnet} ({peran})")
            ketemu = True
    if not ketemu:
        print(f"{teks_ip:<15} -> di luar {jaringan}")

# ===== HASIL AKHIR =====
daftar = ", ".join(f"{s.network_address}/{prefix_baru}" for s in subnet_list)
print()
print("=== HASIL AKHIR ===")
print(f"Jumlah subnet      : {len(subnet_list)}")
print(f"Host usable/subnet : {host_per_subnet}")
print(f"Subnet valid       : {daftar}")