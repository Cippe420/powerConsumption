import socket
import time


def main():
    HOST = "127.0.0.1"
    PORT = 12345  # stessa porta usata nel forwarding
    print("daje")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        while True:
            data = sock.recv(4096)
            if not data:
                break
            lines = data.decode().splitlines()
            for line in lines:
                print(line)


if __name__ == "__main__":
    main()
