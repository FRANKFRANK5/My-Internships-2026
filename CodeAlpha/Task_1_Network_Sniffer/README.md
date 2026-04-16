# 🔍 TASK 01: BASIC NETWORK SNIFFER 📡

## 📝 Project Overview
This project involves the development of a **Network Packet Sniffer** using Python. The primary objective is to capture and analyze live network traffic to understand protocol structures, data encapsulation, and network communication patterns.

> **⚠️ Legal Disclaimer:** This tool is developed for educational purposes and authorized security auditing only. Unauthorized use on networks without permission is strictly prohibited.

---

## 🛠️ Technical Specifications
This sniffer focuses on capturing raw packets and extracting critical information from the Ethernet and IP layers.

### 📋 Captured Data Attributes:
| Attribute | Description |
| :--- | :--- |
| **Source IP** | The origin address of the packet. |
| **Destination IP** | The target address of the packet. |
| **Protocol** | The transport layer protocol (TCP, UDP, ICMP). |
| **Payload** | The actual data transmitted within the packet. |

---

## 💻 Implementation & Usage
The tool is built using the `Scapy` library, a powerful interactive packet manipulation program.

### ⚙️ Prerequisites:
- Python 3.x
- Root/Administrator privileges (required for raw socket access)
- Scapy library: `pip install scapy`

### 🚀 Running the Sniffer:
To start capturing live traffic on your default interface, execute:
```bash
sudo python3 CodeAlpha_Sniffer.py
```

---

## 🛡️ Security & Forensic Analysis
By analyzing the `frank_karani_traffic.log` file, security analysts can identify:
1. **Unusual Traffic Spikes:** Potential DDoS or scanning activity.
2. **Plaintext Data:** Identifying insecure protocols (like HTTP or FTP) that leak sensitive info.
3. **Malicious Communication:** Spotting unauthorized connections to C2 (Command & Control) servers.

---
**Developed by:** Frank Karani  
**Portfolio:** [GitHub Profile](https://github.com/FRANKFRANK5) 🛡️✨
