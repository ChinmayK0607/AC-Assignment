import torch
from depth_anything_v2.dpt import DepthAnythingV2

def load_model():
    model = DepthAnythingV2(encoder='vits', features=64, out_channels=[48, 96, 192, 384])
    model.load_state_dict(torch.load('checkpoints/depth_anything_v2_vits.pth', map_location='cpu'))
    model.eval()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    print(f"Model loaded on: {device}")
    return model, device

model, device = load_model()