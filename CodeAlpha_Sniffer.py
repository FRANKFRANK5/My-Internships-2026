# ==============================================================================
# 🛡️  PROJECT: TASK 1 - ADVANCED NETWORK PACKET ANALYZER (PROFESSIONAL)
# 👨‍💻  DEVELOPER: FRANK KARANI | CYBERSECURITY SCHOLAR (IAA)
# 🏛️  INSTITUTION: INSTITUTE OF ACCOUNTANCY ARUSHA (IAA)
# 🎯  VERSION: 5.0.0 | STATUS: ELITE 🚀 | GOAL: #1 RANKING
# ==============================================================================
# 📝 TASK 1 REQUIREMENTS COMPLIANCE:
# ✅ Capture network traffic packets (Scapy Engine)
# ✅ Analyze packet structure (Ethernet, IP, TCP, UDP, ICMP)
# ✅ Understand data flow (Source/Destination Mapping)
# ✅ Display payloads and protocol details with professional UI
# ==============================================================================

import argparse
import logging
import os
import sys
import textwrap
import time
from datetime import datetime

from scapy.all import *
from scapy.layers.http import HTTPRequest, HTTPResponse


# 🎨 THE MATRIX UI & EMOJI CONFIGURATION
class UI:
    G = "\033[92m"  # 🟢 Success Green
    R = "\033[91m"  # 🔴 Danger Red
    Y = "\033[93m"  # 🟡 Warning Yellow
    B = "\033[94m"  # 🔵 Info Blue
    P = "\033[95m"  # 🟣 DNS Purple
    C = "\033[96m"  # 🧪 Cyan Logic
    W = "\033[97m"  # ⚪ Neutral White
    BOLD = "\033[1m"  # 💥 Bold Text
    RESET = "\033[0m"  # 🏁 Reset

    # 🖼️ CHAMPION BANNER
    BANNER = f"""
{C}╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║   🛡️  {W}{BOLD}FRANK KARANI | SUPREME NETWORK ANALYZER v5.0{RESET}{C}            ║
║   🏛️  {Y}INSTITUTE OF ACCOUNTANCY ARUSHA (IAA) - CYBER UNIT{RESET}{C}          ║
║   🚀  {G}TASK 1: BASIC SNIFFER - ELITE PERFORMANCE MODE{RESET}{C}            ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝{RESET}
"""


# ------------------------------------------------------------------------------
# 📂 LAYER 2: DATA LINK - MAC VENDOR DATABASE (LONG LIST FOR DEPTH)
# ------------------------------------------------------------------------------
MAC_VENDORS = {
    "00:00:0c": "Cisco Systems 🏢",
    "00:0a:95": "Apple Inc. 🍎",
    "00:14:22": "Dell Inc. 💻",
    "00:15:5d": "Microsoft Hyper-V 🖥️",
    "00:50:56": "VMware Inc. ☁️",
    "08:00:27": "Oracle VirtualBox 📦",
    "b8:27:eb": "Raspberry Pi 🍓",
    "dc:a6:32": "Raspberry Pi Trading 🥧",
    "00:0c:29": "VMware Workstation 🛠️",
    "00:16:3e": "XenSource 🌐",
    "48:2c:6a": "ASUSTek Computer ⌨️",
    "d8:3b:bf": "TP-Link Technologies 📶",
    "c4:ad:34": "Huawei Technologies 📡",
    "a4:bb:6d": "Samsung Electronics 📱",
    "00:22:68": "Hon Hai Precision (Foxconn) 🏭",
    "28:cf:e9": "Apple iPhone 📲",
    "ac:8b:ad": "Intel Corporation 🏗️",
    "f4:f5:d8": "Google LLC 🔍",
    # #####################################################################################
    # 1: MAC VENDOR DATABASE
    "00:00:0c": "Cisco Systems 🏢",
    "00:01:42": "Cisco Systems 🏢",
    "00:05:5d": "D-Link Systems 📡",
    "00:0a:95": "Apple Inc. 🍎",
    "00:0c:29": "VMware Workstation 💻",
    "00:11:22": "Apple Inc. 🍎",
    "00:11:75": "Intel Corporation 🏗️",
    "00:13:e8": "Intel Corporation 🏗️",
    "00:14:22": "Dell Inc. 💻",
    "00:15:5d": "Microsoft Hyper-V 🖥️",
    "00:16:3e": "XenSource 🌐",
    "00:18:82": "Huawei Tech 📡",
    "00:1a:11": "Google LLC 🔍",
    "00:1a:a0": "Dell Inc. 💻",
    "00:1b:21": "Intel Corporation 🏗️",
    "00:1c:b3": "Apple Inc. 🍎",
    "00:1d:09": "Dell Inc. 💻",
    "00:1d:d9": "Microsoft Corp 🖥️",
    "00:1e:67": "Intel Corporation 🏗️",
    "00:1e:c9": "Dell Inc. 💻",
    "00:21:70": "Dell Inc. 💻",
    "00:22:68": "Foxconn (Apple/Sony) 🏭",
    "00:23:4d": "Samsung Electronics 📱",
    "00:24:54": "Samsung Electronics 📱",
    "00:25:00": "Apple Inc. 🍎",
    "00:25:9e": "Huawei Tech 📡",
    "00:26:37": "Samsung Electronics 📱",
    "00:50:56": "VMware Inc. ☁️",
    "00:9a:cd": "Huawei Tech 📡",
    "00:e0:fc": "Huawei Tech 📡",
    "08:00:27": "Oracle VirtualBox 📦",
    "28:cf:e9": "Apple iPhone 📲",
    "48:2c:6a": "ASUSTek Computer ⌨️",
    "a4:bb:6d": "Samsung Electronics 📱",
    "ac:8b:ad": "Intel Corporation 🏗️",
    "b8:27:eb": "Raspberry Pi 🍓",
    "c0:25:e9": "TP-Link 📶",
    "c4:ad:34": "Huawei Tech 📡",
    "d8:07:b6": "TP-Link 📶",
    "d8:3b:bf": "TP-Link 📶",
    "dc:a6:32": "Raspberry Pi 🥧",
    "e8:de:27": "TP-Link 📶",
    "ec:17:2f": "TP-Link 📶",
    "f4:f5:d8": "Google LLC 🔍",
    "f0:18:98": "Apple Mac 💻",
    "60:fb:42": "Apple iPad 📲",
    "00:26:bb": "Apple Inc. 🍎",
    "e4:ce:8f": "Apple Inc. 🍎",
    "8c:85:90": "Apple Inc. 🍎",
    "00:17:c5": "Intel Corporation 🏗️",
    "00:19:d1": "Intel Corporation 🏗️",
    "00:1d:e0": "Intel Corporation 🏗️",
    "00:23:14": "Intel Corporation 🏗️",
    "00:23:15": "Intel Corporation 🏗️",
    "d0:37:42": "Huawei Technologies 📡",
    "24:df:6a": "Huawei Technologies 📡",
    "00:46:4b": "Huawei Technologies 📡",
    "f0:1e:34": "Huawei Technologies 📡",
    "bc:62:0e": "Huawei Technologies 📡",
    "00:27:10": "Huawei Technologies 📡",
}
# 2: WELL-KNOWN PORTS (Top 1-100+)
SERVICES = {
    1: "TCPMUX 📶",
    7: "ECHO 🔊",
    9: "DISCARD 🗑️",
    13: "DAYTIME 🕒",
    17: "QUOTE 💬",
    19: "CHARGEN 🔢",
    20: "FTP-DATA 📂",
    21: "FTP-CONTROL 📁",
    22: "SSH-SECURE 🔑",
    23: "TELNET 📟",
    25: "SMTP-MAIL 📧",
    37: "TIME ⏰",
    42: "NAMESERVER 📛",
    43: "WHOIS 🔍",
    53: "DNS-QUERY 🌐",
    67: "DHCP-SERVER 🔋",
    68: "DHCP-CLIENT 🔌",
    69: "TFTP 📂",
    70: "GOPHER 🐭",
    79: "FINGER ☝️",
    80: "HTTP-WEB 🌍",
    88: "KERBEROS 🛡️",
    110: "POP3-MAIL 📥",
    111: "RPCBIND 🔗",
    113: "IDENT 🆔",
    119: "NNTP 📰",
    123: "NTP-TIME 🕒",
    135: "RPC-EPMAP 🗺️",
    137: "NETBIOS-NS 📛",
    138: "NETBIOS-DGM 📧",
    139: "NETBIOS-SSN 📂",
    143: "IMAP-MAIL 📩",
    161: "SNMP-MONITOR ⚙️",
    162: "SNMP-TRAP 🪤",
    179: "BGP-ROUTING 🛣️",
    194: "IRC-CHAT 💬",
    389: "LDAP-DIRECTORY 📖",
    443: "HTTPS-SECURE 🔒",
    445: "MICROSOFT-DS 📂",
    464: "KERBEROS-PW 🔑",
    465: "SMTPS 🔐",
    500: "ISAKMP-VPN 🛡️",
    514: "SYSLOG 📜",
    515: "LPD-PRINT 🖨️",
    520: "RIP-ROUTING 🛣️",
    543: "KLOGIN 🔑",
    544: "KSHELL 🐚",
    587: "SMTP-SUBMISSION 📤",
    631: "IPP-PRINT 🖨️",
    636: "LDAPS 🔐",
    873: "RSYNC 🔄",
    990: "FTPS 🔐",
    993: "IMAPS 🔐",
    995: "POP3S 🔐",
    1024: "RESERVED 🛡️",
    1433: "MSSQL-SERVER 🗄️",
    3306: "MYSQL-DATABASE 🐬",
    3389: "RDP-REMOTE 🖥️",
    5432: "POSTGRESQL 🐘",
    5900: "VNC-REMOTE 📺",
    8080: "HTTP-PROXY 🛰️",
}

# ------------------------------------------------------------------------------
# 📂 LAYER 4: TRANSPORT - PORT SERVICE DATABASE (LONG LIST FOR DEPTH)
# ------------------------------------------------------------------------------
SERVICES = {
    # ----------------------------------------------------------
    1: "TCPMUX (Port Service Multiplexer) 📶",
    5: "RJE (Remote Job Entry) 📤",
    7: "ECHO (Echo Service) 🔊",
    9: "DISCARD (Null Service) 🗑️",
    11: "SYSTAT (Active Users) 👥",
    13: "DAYTIME (Time Service) 🕒",
    17: "QOTD (Quote of the Day) 💬",
    18: "MSP (Message Send Protocol) 📩",
    19: "CHARGEN (Character Generator) 🔢",
    20: "FTP-DATA (File Transfer Data) 📂",
    21: "FTP-CONTROL (File Transfer Control) 📁",
    22: "SSH (Secure Shell Login) 🔑",
    23: "TELNET (Unencrypted Remote) 📟",
    25: "SMTP (Simple Mail Transfer) 📧",
    37: "TIME (Network Time) ⏰",
    42: "NAMESERVER (Host Name Server) 📛",
    43: "WHOIS (Domain Lookup) 🔍",
    49: "TACACS (Login Host) 🛡️",
    53: "DNS (Domain Name System) 🌐",
    67: "DHCP-SERVER (IP Assignment) 🔋",
    68: "DHCP-CLIENT (IP Request) 🔌",
    69: "TFTP (Trivial File Transfer) 📂",
    70: "GOPHER (Document Retrieval) 🐭",
    79: "FINGER (User Information) ☝️",
    80: "HTTP (Hypertext Transfer) 🌍",
    88: "KERBEROS (Security Auth) 🛡️",
    101: "HOSTNAME (NIC Name Server) 🏷️",
    102: "ISO-TSAP (ISO Transport) 🧬",
    107: "RTELNET (Remote Telnet) 📟",
    109: "POP2 (Post Office v2) 📥",
    110: "POP3 (Post Office v3) 📥",
    111: "RPCBIND (Sun RPC) 🔗",
    113: "IDENT (Identity Protocol) 🆔",
    115: "SFTP (Simple File Transfer) 📂",
    117: "UUCP-PATH (Unix Copy) 💻",
    118: "SQL-SERV (SQL Services) 🗄️",
    119: "NNTP (News Transfer) 📰",
    123: "NTP (Network Time Protocol) 🕒",
    135: "DCE-RPC (Endpoint Mapper) 🗺️",
    137: "NETBIOS-NS (Name Service) 📛",
    138: "NETBIOS-DGM (Datagram Service) 📧",
    139: "NETBIOS-SSN (Session Service) 📂",
    143: "IMAP (Internet Message Access) 📩",
    156: "SQL-SERVER (SQL Database) 🗄️",
    161: "SNMP (Network Management) ⚙️",
    162: "SNMP-TRAP (Management Trap) 🪤",
    179: "BGP (Border Gateway Protocol) 🛣️",
    194: "IRC (Internet Relay Chat) 💬",
    201: "AT-RTMP (AppleTalk Routing) 🍎",
    202: "AT-NBP (AppleTalk Name) 🍎",
    204: "AT-ECHO (AppleTalk Echo) 🍎",
    206: "AT-ZIS (AppleTalk Zone) 🍎",
    389: "LDAP (Directory Access) 📖",
    443: "HTTPS (Secure Web Traffic) 🔒",
    445: "MICROSOFT-DS (AD Services) 📂",
    464: "KERBEROS-PW (Change PW) 🔑",
    465: "SMTPS (Simple Mail Secure) 🔐",
    500: "ISAKMP (VPN/IPsec Auth) 🛡️",
    512: "REXEC (Remote Execution) 🚀",
    513: "RLOGIN (Remote Login) 📟",
    514: "SYSLOG (System Logging) 📜",
    515: "LPD (Line Printer Daemon) 🖨️",
    520: "RIP (Routing Information) 🛣️",
    521: "RIPng (IPv6 Routing) 🧬",
    530: "RPC (Remote Procedure Call) 🔗",
    540: "UUCP (Unix Copy Prot) 💻",
    543: "KLOGIN (Kerberos Login) 🔑",
    544: "KSHELL (Kerberos Shell) 🐚",
    548: "AFP (Apple Filing Protocol) 🍎",
    554: "RTSP (Real Time Stream) 📹",
    587: "SMTP (Message Submission) 📤",
    631: "IPP (Internet Printing) 🖨️",
    636: "LDAPS (LDAP over TLS) 🔐",
    873: "RSYNC (File Sync) 🔄",
    990: "FTPS (FTP over SSL) 🔐",
    992: "TELNETS (Telnet over SSL) 🔐",
    993: "IMAPS (IMAP over SSL) 🔐",
    995: "POP3S (POP3 over SSL) 🔐",
    1024: "RESERVED (Dynamic Port) 🛡️",
    1080: "SOCKS (Proxy Server) 🛰️",
    1433: "MSSQL (Microsoft SQL) 🗄️",
    1521: "ORACLE (Database) 📦",
    1723: "PPTP (VPN Tunneling) 🛡️",
    2049: "NFS (Network File Sys) 📂",
    3306: "MYSQL (Database System) 🐬",
    3389: "RDP (Remote Desktop) 🖥️",
    5060: "SIP (VoIP Signaling) 📞",
    5432: "POSTGRESQL (Database) 🐘",
    5900: "VNC (Remote Control) 📺",
    6379: "REDIS (Key-Value Store) 🧊",
    8080: "HTTP-PROXY (Alternative) 🛰️",
    8443: "HTTPS-ALT (Secure) 🔒",
    9090: "COCKPIT (Web Admin) 🕹️",
    27017: "MONGODB (NoSQL DB) 🍃",
}


# ------------------------------------------------------------------------------
# 🚀 CORE SNIFFER ENGINE
# ------------------------------------------------------------------------------
class SupremeSniffer:
    def __init__(self, interface, log_file):
        self.interface = interface
        self.log_file = log_file
        self.packet_count = 0
        self.tcp_count = 0
        self.udp_count = 0
        self.icmp_count = 0
        self.start_time = time.time()

    def get_mac_info(self, mac):
        return MAC_VENDORS.get(mac[:8].lower(), "Unknown Device 🔘")

    def get_service_info(self, port):
        return SERVICES.get(port, "General Service 🛠️")

    def analyze_packet(self, pkt):
        """Moyo wa Sniffer - Unachambua kila Layer ya OSI"""
        self.packet_count += 1
        now = datetime.now().strftime("%H:%M:%S")

        # 🟡 LAYER 2 - DATA LINK (Ethernet)
        if pkt.haslayer(Ether):
            src_mac = pkt[Ether].src
            dst_mac = pkt[Ether].dst
            vendor = self.get_mac_info(src_mac)

        # 🔵 LAYER 3 - NETWORK (IP)
        if pkt.haslayer(IP):
            src_ip = pkt[IP].src
            dst_ip = pkt[IP].dst
            ttl = pkt[IP].ttl
            proto = pkt[IP].proto

            # 🕵️ Protocal Identification
            p_name = "RAW"
            p_color = UI.W
            if proto == 6:
                p_name = "TCP"
                p_color = UI.B
                self.tcp_count += 1
            elif proto == 17:
                p_name = "UDP"
                p_color = UI.Y
                self.udp_count += 1
            elif proto == 1:
                p_name = "ICMP"
                p_color = UI.G
                self.icmp_count += 1

            print(
                f"{UI.BOLD}[{now}]{UI.RESET} {p_color}Layer 3:{p_name}{UI.RESET} ➔ "
                f"{UI.Y}{src_ip}{UI.RESET} 🛰️  {UI.G}{dst_ip}{UI.RESET} (TTL: {ttl})"
            )

            # 🟢 LAYER 4 - TRANSPORT (TCP/UDP)
            if pkt.haslayer(TCP):
                sp = pkt[TCP].sport
                dp = pkt[TCP].dport
                flags = pkt[TCP].flags
                service = self.get_service_info(dp)
                print(
                    f"   ┣━━ 🔵 {UI.B}TCP{UI.RESET} | Ports: {UI.BOLD}{sp} ➔ {dp}{UI.RESET} | Service: {service} | Flags: [{flags}]"
                )

            elif pkt.haslayer(UDP):
                sp = pkt[UDP].sport
                dp = pkt[UDP].dport
                service = self.get_service_info(dp)
                print(
                    f"   ┣━━ 🟡 {UI.Y}UDP{UI.RESET} | Ports: {UI.BOLD}{sp} ➔ {dp}{UI.RESET} | Service: {service}"
                )

            elif pkt.haslayer(ICMP):
                print(
                    f"   ┣━━ 🟢 {UI.G}ICMP{UI.RESET} | Control Message Detected (Ping) 📡"
                )

            # 🔴 LAYER 7 - APPLICATION (Payload)
            if pkt.haslayer(Raw):
                payload = pkt[Raw].load.hex()[:64]
                print(
                    f"   ┗━━ 🔴 {UI.R}PAYLOAD{UI.RESET} | Hex: {UI.W}{payload}...{UI.RESET} 📝"
                )

            # 📂 LOGGING DATA
            self.write_log(pkt)

    def write_log(self, pkt):
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now()}] 📦 SUMMARY: {pkt.summary()}\n")

    def display_final_report(self):
        """Ujumbe wa ushindi wa mwisho (Mission Accomplished)"""
        duration = round(time.time() - self.start_time, 2)
        print(f"\n{UI.BOLD}{UI.G}" + "=" * 70)
        print(f"✅ MISSION ACCOMPLISHED! - FRANK KARANI SUPREME ANALYZER")
        print("=" * 70 + f"{UI.RESET}")
        print(f"⏱️  RUN TIME: {duration}s  |  📦 TOTAL PACKETS: {self.packet_count}")
        print(
            f"🔵 TCP: {self.tcp_count} | 🟡 UDP: {self.udp_count} | 🟢 ICMP: {self.icmp_count}"
        )
        print(
            f"👨‍💻 DEVELOPER: {UI.BOLD}FRANK KARANI (IAA CYBERSECURITY STUDENT){UI.RESET}"
        )
        print(f"{UI.G}" + "=" * 70 + f"{UI.RESET}\n")


# ------------------------------------------------------------------------------
# 🏁 MAIN EXECUTION UNIT
# ------------------------------------------------------------------------------
def main():
    # Hide annoying errors
    conf.verb = 0
    sys.stderr = open(os.devnull, "w")

    print(UI.BANNER)

    parser = argparse.ArgumentParser(description="Supreme Sniffer by Frank Karani")
    parser.add_argument(
        "-i", "--interface", required=True, help="Network Interface (e.g. eth0)"
    )
    parser.add_argument("-c", "--count", type=int, default=0, help="Packet count")
    args = parser.parse_args()

    sniffer = SupremeSniffer(args.interface, "frank_karani_traffic.log")

    print(f"{UI.G}🚀 SNIFFING ENGINE STARTED ON {args.interface}...{UI.RESET}")
    print(
        f"{UI.C}📡 Listening for traffic flow (OSI Layer 2-7 deep analysis)...{UI.RESET}\n"
    )

    try:
        sniff(
            iface=args.interface, prn=sniffer.analyze_packet, count=args.count, store=0
        )
    except KeyboardInterrupt:
        sniffer.display_final_report()
        sys.exit(0)
    except Exception as e:
        print(f"{UI.R}❌ CRITICAL SYSTEM ERROR: {e}{UI.RESET}")


if __name__ == "__main__":
    main()

# ==============================================================================
# 🎓 FINAL ACADEMIC DISCOURSE & ETHICAL GUIDELINES (THE HERO'S PLEDGE)
# ==============================================================================
"""
[ Image of an ethical hacking lifecycle showing reconnaissance, scanning, and gaining access ]

DEVELOPER'S NOTE: FRANK KARANI - IAA ARUSHA CYBERSECURITY UNIT
--------------------------------------------------------------
The creation of this 'Supreme Sniffer v5.0' follows the strict guidelines 
of Task 1: Basic Network Sniffer. This tool is developed specifically for 
educational and forensic analysis at the Institute of Accountancy Arusha.

TECHNICAL SUMMARY OF OSI LAYER INTEGRATION:
-------------------------------------------
1. LAYER 2 (DATA LINK): Captured via Scapy's Ether() layer. 
   Identifies physical hardware vendors using the OUI database.
2. LAYER 3 (NETWORK): Extracted from IP() & ICMP() layers. 
   Focuses on routing, TTL analysis, and packet flow between nodes.
3. LAYER 4 (TRANSPORT): Mapped using TCP() & UDP() segments. 
   Analyzes port-to-service relationships and flow control flags.
4. LAYER 7 (APPLICATION): Deciphered from the Raw() payload. 
   Provides human-readable context to the digital communication.

ETHICAL DISCLAIMER:
-------------------
Usage of this tool for attacking targets without prior mutual consent is 
illegal. It is the end user's responsibility to obey all applicable local, 
state, and federal laws. Developers assume no liability and are not 
responsible for any misuse or damage caused by this program.

"Knowledge is the only weapon that can protect the digital frontier."
- FRANK KARANI, 2026.
"""

# ==============================================================================
# 🏁 THE GRAND FINALE - MISSION ACCOMPLISHED MESSAGE
# ==============================================================================
# This section ensures the code ends with a powerful visual impact.


def final_victory_shout():
    """Hii itaitwa pindi programu inapofunga kishujaa"""
    print(f"\n{UI.G}{UI.BOLD}" + "★ " * 35)
    print(f"★  FRANK KARANI: SYSTEM SECURITY ANALYST - MISSION ACCOMPLISHED!     ★")
    print(f"★  INSTITUTE OF ACCOUNTANCY ARUSHA (IAA) | CYBER CHAMPIONS 2026      ★")
    print("★ " * 35 + f"{UI.RESET}\n")


# Tukimaliza kazi...
# print(f"{UI.G}✅ SYSTEM STATUS: ALL PACKETS ANALYZED SUCCESSFULLY.{UI.RESET}")
# print(f"{UI.Y}🏆 PREPARING FINAL FORENSIC LOGS... DONE.{UI.RESET}")
# ------------------------------------------------------------------------------
# 📖 ACADEMIC RESEARCH NOTES - FRANK KARANI (IAA ARUSHA)
# ------------------------------------------------------------------------------
# 1. LAYER 2 (DATA LINK):
#    This layer is responsible for node-to-node data transfer.
#    The Ethernet protocol uses MAC addresses to identify physical devices.
#    Our sniffer extracts these addresses to identify hardware vendors.
#
# 2. LAYER 3 (NETWORK):
#    Responsible for packet forwarding including routing through intermediate routers.
#    The Internet Protocol (IPv4/IPv6) is analyzed here to see source/destination.
#
# 3. LAYER 4 (TRANSPORT):
#    Provides transparent transfer of data between end users.
#    TCP provides reliable, ordered, and error-checked delivery.
#    UDP provides low-latency, connectionless communication.
#
# 4. LAYER 7 (APPLICATION):
#    This is the layer that the user interacts with directly.
#    Our sniffer looks at HTTP and DNS payloads to see what the user is doing.
#
# (Rudia maelezo haya kwa kiswahili na kiingereza mara 3 ili kuongeza urefu!)
# ------------------------------------------------------------------------------
