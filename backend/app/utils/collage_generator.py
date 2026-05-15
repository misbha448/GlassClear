from PIL import Image
import os

def create_smart_collage(image_paths, layout="Grid", bg_color="#08080e"):
    images = [Image.open(path) for path in image_paths if os.path.exists(path)]
    if not images:
        return None

    # Standardize sizes
    width, height = 800, 600
    images = [img.resize((width, height), Image.Resampling.LANCZOS) for img in images]

    if layout == "Comparison" and len(images) >= 2:
        canvas = Image.new('RGB', (width * 2 + 10, height), bg_color)
        canvas.paste(images[0], (0, 0))
        canvas.paste(images[1], (width + 10, 0))
    
    elif layout == "Grid":
        # Simple 2x2 Grid
        canvas = Image.new('RGB', (width * 2 + 10, height * 2 + 10), bg_color)
        for i, img in enumerate(images[:4]):
            x = (i % 2) * (width + 10)
            y = (i // 2) * (height + 10)
            canvas.paste(img, (x, y))
    
    else:
        # Fallback: Vertical Stack (Story)
        total_height = sum(img.height for img in images[:3])
        canvas = Image.new('RGB', (width, total_height), bg_color)
        y_offset = 0
        for img in images[:3]:
            canvas.paste(img, (0, y_offset))
            y_offset += img.height

    output_path = "uploads/collages/latest_collage.jpg"
    os.makedirs("uploads/collages", exist_ok=True)
    canvas.save(output_path, "JPEG", quality=95)
    return output_path
