import numpy as np
import os
import cv2
from PIL import Image

# Config
DATASET_DIR = "models/data/disease_patches"
CLASSES = ["Healthy", "Stressed"]
IMG_SIZE = 64
SAMPLES_PER_CLASS = 50

def generate_ndvi_patch(status="Healthy"):
    """
    Generates a synthetic 64x64 patch representing NDVI.
    Healthy: Higher values (brighter), Uniform.
    Stressed: Lower values (darker), Patchy.
    """
    if status == "Healthy":
        # high NDVI (0.6 - 0.9), scaled to 0-255 -> 150-230
        base = np.random.normal(190, 20, (IMG_SIZE, IMG_SIZE))
    else:
        # low NDVI (0.2 - 0.5), scaled to 0-255 -> 50-130
        base = np.random.normal(90, 30, (IMG_SIZE, IMG_SIZE))
        
        # Add "stress spots" (dark patches)
        for _ in range(np.random.randint(3, 8)):
            x, y = np.random.randint(0, IMG_SIZE, 2)
            r = np.random.randint(5, 15)
            cv2.circle(base, (x, y), r, (50), -1)

    # Clip and convert to uint8
    base = np.clip(base, 0, 255).astype(np.uint8)
    
    # Create a pseudo-color image for visualization (Red-Yellow-Green colormap)
    # But for ML, we usually use the raw channel. We'll save as grayscale PNG for now.
    return base

def main():
    print("[INFO] Generating synthetic Sentinel-2 NDVI patches...")
    
    for cls in CLASSES:
        cls_dir = os.path.join(DATASET_DIR, cls)
        os.makedirs(cls_dir, exist_ok=True)
        
        print(f"  - Generating {SAMPLES_PER_CLASS} samples for class '{cls}'...")
        for i in range(SAMPLES_PER_CLASS):
            img_data = generate_ndvi_patch(cls)
            img = Image.fromarray(img_data)
            img.save(os.path.join(cls_dir, f"{cls.lower()}_{i}.png"))
            
    print(f"[SUCCESS] Dataset created at {DATASET_DIR}")

if __name__ == "__main__":
    main()
