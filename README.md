# 🛡️ KVM Security & Network Segregation Manager (`kvm-sec-manager`)

A Python-based CLI security tool designed to audit KVM/libvirt hypervisor configurations, ensuring strict network segregation and preventing unauthorized interface leakage between isolated test environments and host networks.

---

## 🚀 Key Features

* **Network Segregation Audit**: Scans active and defined KVM networks, validating forward modes (e.g., verifying isolated NAT or custom internal subnets).
* **VM Interface Leak Detection**: Inspects virtual machine XML definitions to detect misconfigurations—such as isolated test VMs (e.g., Kali Linux) accidentally attached to the host's default network bridge.
* **Static & Runtime Analysis**: Evaluates VM security postures regardless of whether the virtual machines are currently running or powered off.
* **Hypervisor Integration**: Connects securely to the local `qemu:///system` libvirt daemon.

---

## 📁 Project Structure

```
kvm-sec-manager/
├── manager.py          # Main Python auditing script
├── Dockerfile          # Containerized tool definition with libvirt bindings
└── README.md
```

# ⚙️ Local Usage
## Prerequisites

### Make sure python3-libvirt is installed on your Debian host:

sudo apt update
sudo apt install python3-libvirt

## Run the Auditor

### Run the script pointing to your custom isolated network (e.g., zamknieta):

python3 manager.py -n zamknieta

# 🐳 Docker Usage (Containerized Execution)

You can run the tool inside a container while securely mounting the host's libvirt socket:
## 1. Build the image

docker build -t kvm-sec-manager .

## 2. Run the container against the host KVM daemon

docker run --rm -v /var/run/libvirt/libvirt-sock:/var/run/libvirt/libvirt-sock kvm-sec-manager -n zamknieta

# 🛠️ Tech Stack

    Language: Python 3.11

    Virtualization API: libvirt-python

    Containerization: Docker (Debian/Slim base with system bindings)