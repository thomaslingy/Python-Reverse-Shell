import socket
import sys

print("Run this python script on the host machine")
host_name = socket.gethostname()
ip = socket.gethostbyname(host_name)

def send_commands(s, conn):
    """Get a command from the user and send it to the client."""
    print("\nCtrl + C to kill the connection.")
    print("$: ", end="")
    while True:
        try:
            cmd = input()
            if len(cmd) > 0:
                conn.sendall(cmd.encode())
                data = conn.recv(4096) # 4096 is better for heavy transfers!
                print(data.decode("utf-8"), end="")
        except KeyboardInterrupt:
            print("\nGoodbye.")
            conn.close()
            sys.exit()
        except Exception as e:
            print(e)
            conn.close()
            e.close()
            sys.exit()

def server(address):
    """Initialize a socket server and wait for connections."""
    try:
        s = socket.socket()
        s.bind(address)
        s.listen()
        print("[*] Server Initialized, listening")
    except Exception as e:
        print("\n[-] Something went wrong")
        print(e)
        restart = input("\n[*] Reinitialize the server? y/n ")
        if restart.lower() == "y" or restart.lower() == "yes":
            print("\n[-] Reinitializing the server\n")
            server(address)    
        else:
            print("\n")
            sys.exit()
    conn, client_addr = s.accept()
    print(f"[*] Connection Established: {client_addr}")
    send_commands(s, conn)

if __name__ == "__main__":
    host = ip
    port = 19876
    server((host, port))
