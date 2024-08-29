# Real-Time Depth Map Streaming

This project implements a real-time depth map streaming application using advanced depth estimation models. It allows users to visualize depth information from their webcam feed in real-time, leveraging two different depth estimation models.
(note: please use GPU for best results, tested on an L4 24GB Nvidia GPU)

## Table of Contents

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Technologies and Libraries Used](#technologies-and-libraries-used)
4. [Project Structure](#project-structure)
5. [Setup and Installation](#setup-and-installation)
6. [Usage](#usage)
7. [Methodology](#methodology)
8. [Models Used](#models-used)


## Project Overview

This application provides a web interface for real-time depth map visualization. It uses a webcam to capture video frames, processes them using depth estimation models, and displays the resulting depth map alongside the original video feed.

## Features

- Real-time video capture from webcam
- Two depth estimation models to choose from:
  - Depth-Anything-V2
  - MiDaS (DPT-BEiT-Base-384)
- Interactive web interface for model selection and streaming control
- Close to Real-time depth map visualization on GPU 

## Technologies and Libraries Used

- **Backend**:
  - FastAPI: For creating the web server and WebSocket endpoints
  - OpenCV (cv2): For image processing
  - PyTorch: For running the depth estimation models
  - NumPy: For numerical operations on arrays
  - Uvicorn: ASGI server for running the FastAPI application

- **Frontend**:
  - HTML5
  - JavaScript (Vanilla JS)
  - WebSocket API

- **Models**:
  - Depth-Anything-V2-small
  - MiDaS (DPT-BEiT-Base-384)

- **Utilities**:
  - Requests: For downloading model checkpoints
  - tqdm: For progress bars during downloads

## Project Structure

```
depth_map_project/
├── backend/
│   ├── __init__.py
│   ├── main.py           
│   ├── model_loader.py    
│   └── midas_loader.py    
├── frontend/
│   └── index.html         
├── utils/
│   └── checkpoint_downloader.py  
├── checkpoints/           
├── requirements.txt       
└── README.md              
```

## Setup and Installation

1. Clone the repositories:
   ```bash
   git clone https://huggingface.co/spaces/depth-anything/Depth-Anything-V2
   cd Depth-Anything-V2
   git clone https://github.com/ChinmayK0607/Assignment-AC.git
   ```

2. Install the requirements:
   ```bash
   pip install -r Depth-Anything-V2/requirements.txt
   pip install -r Assignment-AC/requirements.txt
   ```

3. Download the model checkpoints:
   ```bash
   python utils/checkpoint_downloader.py
   ```

## Usage

1. Start the backend server:
   ```bash
   uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
   ```

2. Open a web browser and navigate to `http://localhost:8000`

3. Allow access to your webcam when prompted

4. Use the interface to select a model and start/stop the depth map streaming

## Methodology

1. **Video Capture**: The application captures video frames from the user's webcam using the browser's MediaDevices API.

2. **Frame Processing**: Captured frames are sent to the backend server via WebSocket.

3. **Depth Estimation**: The backend processes each frame using the selected depth estimation model (Depth-Anything-V2 or MiDaS).

4. **Visualization**: The resulting depth map is colorized and sent back to the frontend for display.

5. **Real-time Streaming**: This process repeats for each frame, creating a real-time depth map stream.

## Models Used

1. **Depth-Anything-V2**: A state-of-the-art depth estimation model that can generate high-quality depth maps for various scenes.

2. **MiDaS (DPT-BEiT-Base-384)**: A robust depth estimation model known for its performance across different datasets and scene types.

## Side-Note
The checkpoints directory needs to be moved inside the Depth-Anything repo for proper imports. Also all files from the backend and frontend need to be moved to the same directory, as different behaviours on different machines have been noticed while testing. Keeping all files, without folders in the Depth-Anything-V2 repo for best results. 
The directory structure should look something like this: 
![image](https://github.com/user-attachments/assets/1b3745ed-921b-4587-88dc-a95958ba4fba)
