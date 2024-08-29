import asyncio
import cv2
import numpy as np
import torch
import uvicorn
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from starlette.websockets import WebSocketDisconnect
import base64
from model_loader import model as original_model, device
from midas_loader import midas_model
import time

app = FastAPI()

app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Define the target size for resizing
TARGET_WIDTH = 640
TARGET_HEIGHT = 480

async def process_frame_original(frame):
    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    with torch.no_grad():
        depth = original_model.infer_image(img_rgb)
    return depth

async def process_frame_midas(frame):
    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    depth = midas_model.infer_image(img_rgb)
    return depth

async def prepare_depth_map(depth):
    depth_normalized = (depth - depth.min()) / (depth.max() - depth.min())
    depth_normalized = (depth_normalized * 255).astype(np.uint8)
    depth_colormap = cv2.applyColorMap(depth_normalized, cv2.COLORMAP_INFERNO)
    _, buffer = cv2.imencode('.jpg', depth_colormap)
    depth_map_base64 = base64.b64encode(buffer).decode('utf-8')
    return depth_map_base64

@app.websocket("/ws/{model}")
async def websocket_endpoint(websocket: WebSocket, model: str):
    await websocket.accept()
    frame_count = 0
    start_time = time.time()
    try:
        while True:
            data = await websocket.receive_bytes()
            nparr = np.frombuffer(data, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            # Resize the frame
            frame = cv2.resize(frame, (TARGET_WIDTH, TARGET_HEIGHT))

            if model == "original":
                depth = await process_frame_original(frame)
            elif model == "midas":
                depth = await process_frame_midas(frame)
            else:
                await websocket.close(code=4000)
                return

            depth_map_base64 = await prepare_depth_map(depth)
            await websocket.send_text(depth_map_base64)

            # Calculate and print FPS
            frame_count += 1
            elapsed_time = time.time() - start_time
            if elapsed_time > 1:  # Update FPS every second
                fps = frame_count / elapsed_time
                print(f"FPS: {fps:.2f}")
                frame_count = 0
                start_time = time.time()

    except WebSocketDisconnect:
        print("Client disconnected")

@app.get("/")
async def get():
    with open("frontend/index.html", "r") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
