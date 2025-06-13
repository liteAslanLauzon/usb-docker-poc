from fastapi import FastAPI, Response, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from pypylon import pylon
import base64
from fastapi import Request
import os
import tempfile
app = FastAPI()

try:
    camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
    camera.Open()
except Exception as e:
    raise RuntimeError(f"Camera setup failed: {e}")

@app.middleware("http")
async def log_request(request: Request, call_next):
    body = await request.body()
    print(f"Request: {request.method} {request.url} Headers: {dict(request.headers)} Body: {body.decode(errors='replace')}")
    response = await call_next(request)
    return response

@app.post("/capture")
def capture_photo(return_base64: bool = True):
    try:
        camera.StartGrabbingMax(1)
        grab_result = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

        if not grab_result.GrabSucceeded():
            raise HTTPException(status_code=500, detail="Camera capture failed")

        image = pylon.PylonImage()
        image.AttachGrabResultBuffer(grab_result)
        
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
            temp_path = temp_file.name

        image.Save(pylon.ImageFileFormat_Png, temp_path)

        with open(temp_path, "rb") as f:
            img_bytes = f.read()

        os.remove(temp_path)
        grab_result.Release()

        if return_base64:
            return JSONResponse(content={"image_base64": base64.b64encode(img_bytes).decode()})
        else:
            return Response(content=img_bytes, media_type="image/png")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/test")
def test_response():
    return {"status": "ok", "message": "FastAPI is running"}


@app.post("/capture_disp")
def capture_and_stream_image():
    try:
        camera.StartGrabbingMax(1)
        grab_result = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

        if not grab_result.GrabSucceeded():
            raise HTTPException(status_code=500, detail="Camera capture failed")

        image = pylon.PylonImage()
        image.AttachGrabResultBuffer(grab_result)

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
            temp_path = temp_file.name

        image.Save(pylon.ImageFileFormat_Png, temp_path)

        f = open(temp_path, "rb")
        grab_result.Release()

        return StreamingResponse(f, media_type="image/png")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
