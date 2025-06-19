import socket
import struct
from pypylon import pylon
import tempfile
import os
import sys

HOST = "0.0.0.0"
PORT = 9000

try:
    camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
    camera.Open()
    print("Camera initialized")
except Exception as e:
    raise RuntimeError(f"Camera setup failed: {e}")


def capture_image_bytes():
    camera.StartGrabbingMax(1)
    grab_result = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

    if grab_result.GrabSucceeded():
        image = pylon.PylonImage()
        image.AttachGrabResultBuffer(grab_result)

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
            temp_path = temp_file.name

        image.Save(pylon.ImageFileFormat_Png, temp_path)

        with open(temp_path, "rb") as f:
            img_data = f.read()

        os.remove(temp_path)
        grab_result.Release()
        return img_data
    else:
        return None


# Start TCP server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind((HOST, PORT))
    server.listen()
    print(f"TCP camera server listening on {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        print(f"Connected by {addr}")
        with conn:
            try:
                request = conn.recv(1024).strip()
                print(f"Received: {request}")

                if request == b"capture":
                    img_bytes = capture_image_bytes()
                    if img_bytes:
                        # Send 4-byte length followed by image
                        conn.sendall(struct.pack(">I", len(img_bytes)) + img_bytes)
                        print(f"Sent image ({len(img_bytes)} bytes)")
                    else:
                        conn.sendall(b"FAIL")
                        print("Capture failed")
                elif request == b'shutdown':
                    conn.sendall(b'Shutting down')
                    print("Shutdown requested")
                    camera.Close()
                    sys.exit(0)
                else:
                    conn.sendall(b"UNKNOWN_COMMAND")
                    print("Unknown command received")
            except Exception as e:
                print(f"Error handling connection: {e}")
