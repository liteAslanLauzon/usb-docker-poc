import base64
import threading
import requests
import time
from io import BytesIO
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pypylon import pylon
from fastapi.responses import JSONResponse

app = FastAPI()

# Store last scanned barcode
barcode_buffer = ""

# Initialize camera once
camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
camera.Open()


# --- Models ---
class BarcodeData(BaseModel):
    barcode: str


# --- Background Thread: Listen to barcode (simulated input) ---
def barcode_listener():
    while True:
        try:
            scanned = input().strip()  # Simulated scan from keyboard-style USB device
            if scanned:
                # Send barcode to our own API
                try:
                    requests.post(
                        "http://127.0.0.1:8000/barcode", json={"barcode": scanned}
                    )
                except Exception as e:
                    print(f"Failed to post barcode: {e}")
        except Exception as e:
            print(f"Barcode listener error: {e}")
        time.sleep(0.1)


# Start listener thread
threading.Thread(target=barcode_listener, daemon=True).start()

# --- API Routes ---


@app.post("/barcode")
def receive_barcode(data: BarcodeData):
    global barcode_buffer
    barcode_buffer = data.barcode
    print(f"Received barcode: {data.barcode}")
    return {"message": "Barcode received", "barcode": data.barcode}


@app.get("/barcode")
def get_last_barcode():
    if not barcode_buffer:
        raise HTTPException(status_code=404, detail="No barcode scanned yet.")
    return {"barcode": barcode_buffer}


@app.post("/capture")
def capture_image():
    try:
        camera.StartGrabbingMax(1)
        grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

        if grabResult.GrabSucceeded():
            image = pylon.PylonImage()
            image.AttachGrabResultBuffer(grabResult)

            # Save to buffer instead of file
            stream = BytesIO()
            image.Save(pylon.ImageFileFormat_Png, stream)
            base64_img = base64.b64encode(stream.getvalue()).decode("utf-8")

            grabResult.Release()
            return JSONResponse(content={"image_base64": base64_img})
        else:
            raise HTTPException(status_code=500, detail="Camera grab failed")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Capture error: {e}")
