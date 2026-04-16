import argparse
import logging
import os
import sys
from datetime import datetime

# Import Scapy components
from scapy.all import Raw, conf, sniff
from scapy.layers.dns import DNS
from scapy.layers.http import HTTPRequest, HTTPResponse
from scapy.layers.inet import ICMP, IP, TCP, UDP
from scapy.layers.inet6 import IPv6

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("packet_analyzer.log"),
    ],
)
logger = logging.getLogger("packetAnalyzer")

conf.verb = 0


class PacketAnalyzer:
    def __init__(self, interface, filter_exp=None, log_file=None):
        self.interface = interface
        self.filter_exp = filter_exp
        self.log_file = log_file
        self.packet_count = 0
        self.running = False
        self.socket = None

    def start_capture(self, packet_count=0):
        """Hapa ndipo injini inapoanza kazi"""
        logger.info("-" * 60)
        logger.info("🚀 FRANK KARANI | NETWORK ANALYZER v1.0")
        logger.info("🛡️  IAA ARUSHA - CYBERSECURITY DIVISION")
        logger.info("-" * 60)
        logger.info("🚀 Starting capture on %s...", self.interface)

        try:
            sniff(
                iface=self.interface,
                filter=self.filter_exp,
                prn=self.process_packet,
                store=False,
                count=packet_count,
            )
        except PermissionError:
            logger.error("❌ Permission denied. Use sudo.")
            sys.exit(1)
        except Exception as e:
            logger.error("⚠️ Capture error: %s", str(e))

    def process_packet(self, packet):
        """Uchambuzi wa kila packet"""
        if IP in packet or IPv6 in packet:
            self.analyze_ip_packet(packet)

    def analyze_ip_packet(self, packet):
        if IP in packet:
            ip_src, ip_dst = packet[IP].src, packet[IP].dst
            version = "IPv4"
        elif IPv6 in packet:
            ip_src, ip_dst = packet[IPv6].src, packet[IPv6].dst
            version = "IPv6"

        timestamp = datetime.now().strftime("%H:%M:%S")
        base_info = f"[{timestamp}] {version} | {ip_src} ➔ {ip_dst}"

        if TCP in packet:
            logger.info(
                f"🔵 {base_info} | TCP | Ports: {packet[TCP].sport}➔{packet[TCP].dport}"
            )
        elif UDP in packet:
            logger.info(
                f"🟡 {base_info} | UDP | Ports: {packet[UDP].sport}➔{packet[UDP].dport}"
            )
        elif ICMP in packet:
            logger.info(f"🟢 {base_info} | ICMP (Ping)")

        if self.log_file:
            self.log_packet(packet)

    def log_packet(self, packet):
        with open(self.log_file, "a") as f:
            f.write(f"[{datetime.now()}] {packet.summary()}\n")


def main():
    # HAPA ndipo tunapoondoa kizuizi cha stderr ili uone error kama ipo
    # sys.stderr = open(os.devnull, "w")

    parser = argparse.ArgumentParser(description="🛡️ Frank Karani Sniffer")
    parser.add_argument("-i", "--interface", required=True, help="e.g. eth0 or any")
    parser.add_argument("-c", "--count", type=int, default=0)
    parser.add_argument("-l", "--log", default="packet_analyzer.log")

    args = parser.parse_args()
    analyzer = PacketAnalyzer(interface=args.interface, log_file=args.log)

    try:
        analyzer.start_capture(packet_count=args.count)
    except KeyboardInterrupt:
        logger.info("\n🛑 SESSION TERMINATED BY FRANK KARANI | IAA")
        sys.exit(0)


if __name__ == "__main__":
    main()
