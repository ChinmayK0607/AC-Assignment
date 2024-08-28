#!/bin/bash

# Set up error handling
set -e

# Clone Depth-Anything-V2
echo "Cloning Depth-Anything-V2..."
git clone https://huggingface.co/spaces/depth-anything/Depth-Anything-V2
cd Depth-Anything-V2

# Install requirements for Depth-Anything-V2
echo "Installing requirements for Depth-Anything-V2..."
pip install -r requirements.txt

# Clone the Assignment repository
echo "Cloning Assignment-AC repository..."
git clone https://github.com/ChinmayK0607/Assignment-AC.git

# Move into the Assignment-AC directory
cd Assignment-AC

# Install requirements for Assignment-AC
echo "Installing requirements for Assignment-AC..."
pip install -r requirements.txt
# download checkpoints
cd utils
python checkpoint_downloader.py 
cd .. 
# Run the backend using uvicorn
echo "Starting the backend server..."
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

echo "Setup complete and server is running!"