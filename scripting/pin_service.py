"""
CTF Scripting challenge - weak PIN service.

Listens on TCP 31337. Clients get one PIN guess per connection;
the PIN is 3 digits (000-999) - trivially brute-forceable, which IS
the challenge: write a script (solver.py) instead of guessing by hand.

Run:  python pin_service.py
"""

import socket
import threading

HOST, PORT = "0.0.0.0", 31337
PIN = "042"
FLAG = "flag{brut3_f0rc3_ch4mp}"

BANNER = b"SecureVault PIN pad. Enter 3-digit PIN: "


def handle(conn: socket.socket, addr):
    try:
        conn.sendall(BANNER)
        guess = conn.recv(16).decode(errors="ignore").strip()
        if guess == PIN:
            conn.sendall(f"CORRECT. {FLAG}\n".encode())
        else:
            conn.sendall(b"WRONG\n")
    finally:
        conn.close()


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind((HOST, PORT))
        srv.listen()
        print(f"PIN service listening on {HOST}:{PORT}")
        while True:
            conn, addr = srv.accept()
            threading.Thread(target=handle, args=(conn, addr),
                             daemon=True).start()


if __name__ == "__main__":
    main()
