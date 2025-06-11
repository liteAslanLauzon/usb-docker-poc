import sys
import numpy as np
import cv2
import pypylon.pylon as pylon
from datetime import datetime

CAMERA_INDEX = 0
BARCODE_ACTIONS = {"TAKE PHOTO,": "photo", "CLOSE": "exit", "q": "exit"}

def capture_photo() -> np.ndarray | None:
    """
    Captures a single image from the first connected Basler camera
    and returns it as a NumPy array (BGR format).

    Returns:
        np.ndarray | None: Captured image as a NumPy array if successful, else None.
    """
    try:
        # Connect to the first available camera
        camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
        camera.Open()

        # Grab a single image
        camera.StartGrabbingMax(1)
        converter = pylon.ImageFormatConverter()
        converter.OutputPixelFormat = pylon.PixelType_BGR8packed
        converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

        img_array = None

        while camera.IsGrabbing():
            grab_result = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

            if grab_result.GrabSucceeded():
                image = converter.Convert(grab_result)
                img_array = image.GetArray()
            else:
                print("Failed to grab image.")

            grab_result.Release()

        camera.Close()
        return img_array
    except pylon.GenericException as e:
        print(f"Error: {e}")


def main():
    print("Scan a barcode...")
    while True:
        try:
            barcode = input(">> ").strip()
            action = BARCODE_ACTIONS.get(barcode)
            if action == "photo":
                img = capture_photo()
                if img is not None:
                    print("Photo captured.")
                    cv2.imwrite(f"./output/{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg", img)
                else:
                    print("Failed to capture photo.")
            elif action == "exit":
                print("Exiting.")
                sys.exit(0)
            else:
                print("Unknown barcode.")
        except KeyboardInterrupt:
            print("Interrupted.")
            break

if __name__ == "__main__":
    main()
