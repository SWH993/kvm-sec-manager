import argparse
import sys
import xml.etree.ElementTree as ET

try:
    import libvirt
except ImportError:
    print("[-] Error: 'libvirt-python' package is not installed.")
    print("[-] Install it via: sudo apt install python3-libvirt or pip install libvirt-python")
    sys.exit(1)


def audit_networks(connection: str, target_net_name: str) -> None:
    print(f"\n[*] Audit KVM Networks (Target: '{target_net_name}')")
    found_target = False

    nets = connection.listAllNetworks()
    for net in nets:
        name = net.name()
        active = net.isActive()
        xml_description = net.XMLDesc()

        root = ET.fromstring(xml_description)
        forward_mode = "none (isolated)"
        forward_element = root.find("forward")
        if forward_element is not None:
            forward_mode = forward_element.get("mode", "nat")

        print(f"    - Network: {name} | Active: {active} | Forward Mode: {forward_mode}")

        if name == target_net_name:
            found_target = True
            if forward_mode == "nat":
                print(f"      [+] Custom NAT network '{name}' verified. Ensure firewall/iptables rules block routing to default net.")
            else:
                print(f"      [!] Warning: Netowrk '{name}' uses unexpected forward mode: {forward_mode}")

    if not found_target:
        print(f"      [-] Warning: Target custom network '{name}' not found on host!")

def audit_vms(connection: str, target_net_name: str) -> None:
    print("\n[+] Auditing Virtual Machines ...")
    domains = connection.listAllDomains()
    
    for domain in domains:
        name = domain.name()
        state, _ = domain.state()
        state_str = "Running" if state == libvirt.VIR_DOMAIN_RUNNING else "Shut off"

        xml_description = domain.XMLDesc()
        root = ET.fromstring(xml_description)

        attached_networks = []
        for interface in root.findall(".//devices/interface[@type='network']"):
            source = interface.find('source')
            if source is not None:
                net_name = source.get('network')
                attached_networks.append(net_name)

        print(f"    - VM: {name} | State: {state_str} | Networks: {attached_networks}")

        if 'default' in attached_networks and target_net_name in attached_networks:
            print(f"     [!] SECURITY WARNIGN: VM '{name}' has interfaces on BOTH 'default' and isolated '{target_net_name}' networks!")
        elif target_net_name in attached_networks:
            print(f"     [+] VM '{name}' is correctly attached only to the isolated network.")

def main():
    parser = argparse.ArgumentParser(description="KVM Security & Network Segregation Auditor")
    parser.add_argument("-n", "--network", help="Name of your custom isolated/NAT network")
    args = parser.parse_args()

    print("[*] Connecting to local KVM daemon (qemu:///system)...")
    try:
        connection = libvirt.openReadOnly("qemu:///system")
        if connection is None:
            print("[-] Failed to open connection to qemu:///system")
            sys.exit(1)
    except libvirt.libvirtError as e:
        print(f"[-] Connection error: {e}")
        print("[-] Make sure you have permissions (run with sudo or add user to libvirt group).")
        sys.exit(1)

    audit_networks(connection, args.network)
    audit_vms(connection, args.network)

    connection.close()
    print("\n[+] Audit completed successfully.")

if __name__ == "__main__":
    main()