import torch
from PIL import Image
import torchvision.transforms as transforms
import yaml
import os
import sys
import numpy as np
import cv2

# 🔥 BASE DIR
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.join(BASE_DIR, "..")

sys.path.append(PROJECT_DIR)

from xreflection.models.rdnet_model import RDNetModel

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

yaml_path = os.path.join(BASE_DIR, "options", "train_rdnet.yml")

ckpt_path = os.path.join(
    BASE_DIR,
    "experiments",
    "train_sirs_rdnet",
    "checkpoints",
    "psnr=38.2008.ckpt"
)

# 🔥 LOAD CONFIG
with open(yaml_path, "r") as f:
    opt = yaml.safe_load(f)

opt["test_only"] = True

# 🔥 INIT MODEL
model = RDNetModel(opt)

# 🔥 LOAD WEIGHTS
checkpoint = torch.load(ckpt_path, map_location="cpu")
model.load_state_dict(checkpoint["state_dict"], strict=False)

print("🔥 MODEL LOADED SUCCESSFULLY:", type(model))
print("🔥 USING CHECKPOINT:", ckpt_path)

model.eval()

# 🔥 TRANSFORM (NO FORCED RESIZE)
transform = transforms.Compose([
    transforms.ToTensor()
])

# 🔥 IMPORTANT: make size divisible by 32
def make_divisible(image, divisor=32):
    w, h = image.size
    new_w = max(divisor, (w // divisor) * divisor)
    new_h = max(divisor, (h // divisor) * divisor)
    return image.resize((new_w, new_h))

# 🔥 PREDICT FUNCTION
def predict(image: Image.Image):
    original_size = image.size

    # ✅ FIX SIZE ISSUE
    image_resized = make_divisible(image)
    img = transform(image_resized).unsqueeze(0)

    with torch.no_grad():
        if hasattr(model, "use_ema") and model.use_ema:
            net = model.ema_model
        else:
            net = model.net_g

        x_cls_out, x_img_out = net(img)
        
        # Intermediate stages for Progressive Refinement
        stages = []
        for stage_tensor in x_img_out:
            # Process each stage tensor into a PIL image
            stage_img = stage_tensor[:, :3, ...].squeeze().permute(1, 2, 0).cpu().numpy()
            stage_img = np.clip(stage_img, 0, 1)
            stage_img = (stage_img * 255).astype(np.uint8)
            stages.append(Image.fromarray(stage_img).resize(original_size))

        # Final clean output
        final_tensor = x_img_out[-1][:, :3, ...]

    # Create Confidence Map (where the model changed the image the most)
    input_np = np.array(image_resized).astype(float) / 255.0
    output_np = final_tensor.squeeze().permute(1, 2, 0).cpu().numpy()
    diff = np.abs(input_np - output_np).mean(axis=-1)
    confidence_map = (diff / (diff.max() + 1e-6) * 255).astype(np.uint8)
    confidence_pil = Image.fromarray(confidence_map).resize(original_size)

    # 🔥 tensor → numpy
    output = final_tensor.squeeze().permute(1, 2, 0).cpu().numpy()

    # 🔥 clamp and ensure contiguous
    output = np.clip(output, 0, 1)
    output = (output * 255).astype(np.uint8)
    output = np.ascontiguousarray(output)

    # 🔥 sharpening
    kernel = np.array([[0, -1, 0],
                       [-1, 5,-1],
                       [0, -1, 0]])
    
    # Apply sharpening to the RGB image
    output = cv2.filter2D(output, cv2.CV_8U, kernel)

    # 🔥 contrast boost
    output = cv2.convertScaleAbs(output, alpha=1.1, beta=5)

    # 🔥 to PIL
    output_image = Image.fromarray(output)

    # 🔥 restore original size
    output_image = output_image.resize(original_size)

    return output_image, confidence_pil, stages