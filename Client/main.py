import requests
import sys
import cv2
import numpy as np

# Base URL of your server
BASE_URL = "http://192.168.192.24:8000"


def send_capture() -> None:
    try:
        response = requests.post(f"{BASE_URL}/capture")
        print("📸 Capture triggered!")
        print(f"Status Code: {response.status_code}")
        print("Response:")
        print(response.json())
        print()
    except requests.RequestException as e:
        print(f"Capture request failed: {e}")
        print()

def send_capture_disp()-> None:
    try:
        response = requests.post(f"{BASE_URL}/capture_disp")
        print("📸 Capture with display triggered!")
        print(f"Status Code: {response.status_code}")
        img_array = np.asarray(bytearray(response.content), dtype=np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

        img_resized = cv2.resize(img, (800, 600))
        cv2.imshow("Captured Image", img_resized)
        print("Press any key to close the image window.")
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    except requests.RequestException as e:
        print(f"Capture with display request failed: {e}")
        print()


def send_test(data: str) -> None:
    try:
        response = requests.post(f"{BASE_URL}/test", json={"message": data})
        print(f"✅ Sent to /test: {data}")
        print(f"Status Code: {response.status_code}")
        print("Response body:")
        print(response.text)
        print()
    except requests.RequestException as e:
        print(f"Test request failed: {e}")
        print()


def main() -> None:
    while True:
        user_input = input(
            "Enter string (type 'capture' to take photo, 'q' to quit): "
        ).strip()
        if user_input.lower() == "q":
            print("👋 Quitting program. Goodbye!")
            sys.exit(0)
        elif user_input.lower() == "capture":
            send_capture()
        elif user_input.lower() == "capture_disp":
            send_capture_disp()
        else:
            send_test(user_input)


if __name__ == "__main__":
    main()
