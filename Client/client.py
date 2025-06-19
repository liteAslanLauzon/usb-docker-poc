import socket
import sys
import struct
import cv2
import numpy as np
import time

HOST = "host.docker.internal"  # Replace with server IP
PORT = 9000

def client(): 

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST, PORT))
        except ConnectionRefusedError:
            print(f"Could not connect to server at {HOST}:{PORT}. Is the server running?")
            return
        print(f"Connected to server at {HOST}:{PORT}")

        while True:

            user_input = input(
                "Enter string (type 'capture' to take photo, 'q' to quit): "
            ).strip()
            if user_input.lower() == "q":
                print("Quitting program")
                sys.exit(0)
            if user_input.lower() == "serverq":
                s.sendall(b"shutdown")
                print("Quitting server")
            elif user_input.lower() == "capture":
                s.sendall(b"capture")
                start_time = time.time()
                raw_len = s.recv(4)
                img_len = struct.unpack(">I", raw_len)[0]

                img_data = b""
                while len(img_data) < img_len:
                    packet = s.recv(65536)
                    if not packet:
                        break
                    img_data += packet

                elapsed = time.time() - start_time
                print(f"Received image data of length: {len(img_data)} bytes in {elapsed:.3f} seconds")


if __name__ == "__main__":
    client()
