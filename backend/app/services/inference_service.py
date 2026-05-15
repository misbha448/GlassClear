import os
import time
import numpy as np
from PIL import Image
import cv2

# 🔥 RDNet import
from app.rdnet_infer import predict

def run_reflection_removal(input_path: str, output_dir: str, base_name: str):
    start_time = time.time()
    os.makedirs(output_dir, exist_ok=True)

    try:
        # ✅ load image
        image = Image.open(input_path).convert("RGB")

        # 🔥 RUN MODEL (REAL INFERENCE)
        output_image, confidence_map, stages = predict(image)

        # ✅ save final output
        output_path = os.path.join(output_dir, f"out_{base_name}.jpg")
        output_image.save(output_path)
        print(f"DEBUG: Saved final output to {output_path}")
        
        # ✅ save confidence map
        conf_path = os.path.join(output_dir, f"conf_{base_name}.jpg")
        confidence_map.save(conf_path)
        print(f"DEBUG: Saved confidence map to {conf_path}")
        
        # ✅ save stages
        stage_paths = []
        for i, stage_img in enumerate(stages):
            s_path = os.path.join(output_dir, f"stage_{i}_{base_name}.jpg")
            stage_img.save(s_path)
            stage_paths.append(s_path)
        print(f"DEBUG: Saved {len(stage_paths)} intermediate stages.")

        # 📊 Calculate Real Metrics (Simplified SSIM & Edge Score)
        # In a production app, use skimage.metrics.structural_similarity
        img1 = np.array(image).astype(np.float32)
        img2 = np.array(output_image).astype(np.float32)
        ssim_val = float(1.0 - (np.abs(img1 - img2).mean() / 255.0)) # Simplified proxy
        
        # Edge Preservation
        edge1 = cv2.Canny(np.array(image), 100, 200)
        edge2 = cv2.Canny(np.array(output_image), 100, 200)
        edge_score = float(np.sum(edge1 & edge2) / (np.sum(edge1) + 1e-6))
        
        metrics = {
            "ssim": round(ssim_val, 4),
            "edge_score": round(edge_score, 4)
        }

    except Exception as e:
        raise RuntimeError(f"RDNet inference failed: {str(e)}")

    processing_time = round(time.time() - start_time, 4)

    return {
        "final": output_path,
        "confidence": conf_path,
        "stages": stage_paths,
        "metrics": metrics,
        "time": processing_time
    }