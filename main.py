import sys
import cv2
from datetime import datetime

BARCODE_ACTIONS = {"123456": "photo", "000000": "exit"}

# HID keycode map (partial, add more as needed)
KEY_MAP = {
    4: "a",
    5: "b",
    6: "c",
    7: "d",
    8: "e",
    9: "f",
    10: "g",
    11: "h",
    12: "i",
    13: "j",
    14: "k",
    15: "l",
    16: "m",
    17: "n",
    18: "o",
    19: "p",
    20: "q",
    21: "r",
    22: "s",
    23: "t",
    24: "u",
    25: "v",
    26: "w",
    27: "x",
    28: "y",
    29: "z",
    30: "1",
    31: "2",
    32: "3",
    33: "4",
    34: "5",
    35: "6",
    36: "7",
    37: "8",
    38: "9",
    39: "0",
    40: "\n",  # Enter
}


def decode_hid_event(buffer):
    """Decode HID report to character"""
    shift = buffer[0] == 0x02
    keycode = buffer[2]
    if keycode == 0 or keycode not in KEY_MAP:
        return ""
    char = KEY_MAP[keycode]
    return char.upper() if shift else char


def main():
    print("Listening for barcode scans on /dev/hidraw0...")

    barcode = ""
    try:
        with open("/dev/hidraw0", "rb") as f:
            while True:
                data = f.read(8)
                char = decode_hid_event(data)
                if char == "\n":
                    print(f">> {barcode}")
                    action = BARCODE_ACTIONS.get(barcode)
                    if action == "photo":
                        # img = capture_photo()
                        img = None
                        if img is not None:
                            filename = f"./output/{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
                            cv2.imwrite(filename, img)
                            print(f"Photo saved to {filename}")
                        else:
                            print("Failed to capture photo.")
                    elif action == "exit":
                        print("Exiting.")
                        sys.exit(0)
                    else:
                        print("Unknown barcode.")
                    barcode = ""
                else:
                    barcode += char
    except KeyboardInterrupt:
        print("Interrupted.")
    except FileNotFoundError:
        print("/dev/hidraw0 not found. Is the device attached?")
    except PermissionError:
        print("Permission denied on /dev/hidraw0. Try running with sudo.")


if __name__ == "__main__":
    main()
