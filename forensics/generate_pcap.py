"""
CTF Networking/Forensics challenge - pcap generator.

Creates capture.pcap containing a full cleartext FTP login session.
The flag is the FTP password, visible with a simple Wireshark filter
(tcp.port == 21, or "Follow TCP Stream").

Requires: pip install scapy
Run:      python generate_pcap.py   -> writes capture.pcap
"""

from scapy.all import Ether, IP, TCP, Raw, wrpcap

SRC, DST = "192.168.20.10", "192.168.30.50"
SPORT, DPORT = 49152, 21
FLAG = "flag{ftp_cl34rt3xt_sn1ff}"

# (payload, direction): True = client->server, False = server->client
CONVERSATION = [
    (b"220 SecureVault FTP server ready\r\n", False),
    (b"USER backup_admin\r\n", True),
    (b"331 Password required for backup_admin\r\n", False),
    (f"PASS {FLAG}\r\n".encode(), True),
    (b"230 Login successful\r\n", False),
    (b"SYST\r\n", True),
    (b"215 UNIX Type: L8\r\n", False),
    (b"QUIT\r\n", True),
    (b"221 Goodbye\r\n", False),
]


def build_packets():
    pkts = []
    seq_c, seq_s = 1000, 5000
    for payload, client_to_server in CONVERSATION:
        if client_to_server:
            pkt = (Ether() / IP(src=SRC, dst=DST)
                   / TCP(sport=SPORT, dport=DPORT, flags="PA",
                         seq=seq_c, ack=seq_s)
                   / Raw(load=payload))
            seq_c += len(payload)
        else:
            pkt = (Ether() / IP(src=DST, dst=SRC)
                   / TCP(sport=DPORT, dport=SPORT, flags="PA",
                         seq=seq_s, ack=seq_c)
                   / Raw(load=payload))
            seq_s += len(payload)
        pkts.append(pkt)
    return pkts


if __name__ == "__main__":
    wrpcap("capture.pcap", build_packets())
    print("capture.pcap written (FTP login, flag in cleartext password)")
