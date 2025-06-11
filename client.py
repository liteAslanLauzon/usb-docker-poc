import requests
import threading
import time
import base64

# CONFIG
API_URL = "http://<SERVER_IP>:8000"  # Replace <SERVER_IP> with server IP or hostname


def send_barcode(barcode):
    try:
        response = requests.post(f"{API_URL}/barcode", json={"barcode": barcode})
        if response.status_code == 200:
            print(f"✅ Barcode sent: {barcode}")
        else:
            print(f"❌ Failed to send barcode: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"Error posting barcode: {e}")


def get_photo_and_save(filename="captured.png"):
    try:
        response = requests.post(f"{API_URL}/capture")
        if response.status_code == 200:
            img_data = response.json()["image_base64"]
            with open(filename, "wb") as f:
                f.write(base64.b64decode(img_data))
            print(f"📸 Image saved as {filename}")
        else:
            print(f"❌ Failed to get image: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"Error fetching photo: {e}")


def barcode_input_loop():
    print("📥 Waiting for barcode scans (press Enter after scan)...")
    while True:
        try:
            code = input().strip()
            if code:
                send_barcode(code)
        except Exception as e:
            print(f"Error reading input: {e}")
        time.sleep(0.1)


def command_loop():
    print("⌨️ Type 'photo' to trigger a capture, or just scan a barcode.")
    while True:
        cmd = input(">>> ").strip().lower()
        if cmd == "photo":
            get_photo_and_save()
        elif cmd:
            send_barcode(cmd)


# --- Choose one loop to run ---
if __name__ == "__main__":
    # Use this if barcode comes from scanner + manual commands for photo
    threading.Thread(target=barcode_input_loop, daemon=True).start()
    command_loop()

    # Or if barcode and camera are both automated:
    # barcode_input_loop()
