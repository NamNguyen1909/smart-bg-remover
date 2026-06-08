import os
import sys
import numpy as np
from PIL import Image
import scipy.ndimage as ndimage

def remove_background(image_path, output_path, tolerance=40, low_tolerance=15):
    print(f"Loading image: {image_path}")
    img = Image.open(image_path).convert("RGBA")
    arr = np.array(img)
    h, w, _ = arr.shape
    
    # We assume the background color is white or matching the corners.
    corners = [
        arr[0, 0, :3],
        arr[0, w-1, :3],
        arr[h-1, 0, :3],
        arr[h-1, w-1, :3]
    ]
    bg_color = np.mean(corners, axis=0).astype(np.int32)
    print(f"Detected background color: {bg_color}")
    
    # Calculate color distance to background color for each pixel
    diff = arr[:, :, :3].astype(np.int32) - bg_color
    dist = np.sqrt(np.sum(diff ** 2, axis=-1))
    
    # Binary mask of similar pixels (using tolerance)
    similar = dist < tolerance
    
    # Label connected components of background-like pixels
    labels, num_features = ndimage.label(similar)
    print(f"Found {num_features} connected components.")
    
    # Identify which components touch the borders
    border_labels = set()
    border_labels.update(labels[0, :])          # Top edge
    border_labels.update(labels[-1, :])         # Bottom edge
    border_labels.update(labels[:, 0])          # Left edge
    border_labels.update(labels[:, -1])         # Right edge
    
    # 0 is the foreground (non-similar pixels), remove it from border labels
    if 0 in border_labels:
        border_labels.remove(0)
        
    print(f"Border-touching component labels: {border_labels}")
    
    # Create mask of background
    background_mask = np.isin(labels, list(border_labels))
    
    # We copy the original alpha channel (which is 255 everywhere initially)
    alpha = arr[:, :, 3].copy()
    
    # Calculate soft alpha for anti-aliasing
    with np.errstate(divide='ignore', invalid='ignore'):
        alpha_factor = (dist - low_tolerance) / (tolerance - low_tolerance)
        alpha_factor = np.clip(alpha_factor, 0.0, 1.0)
        
    # For background mask pixels, apply the soft alpha_factor
    alpha[background_mask] = (alpha[background_mask] * alpha_factor[background_mask]).astype(np.uint8)
    
    # Update the alpha channel in the array
    arr[:, :, 3] = alpha
    
    # Save the output image
    out_img = Image.fromarray(arr)
    out_img.save(output_path, "PNG")
    print(f"Saved transparent image to: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python remove_bg_smart.py <input_path> <output_path> [tolerance] [low_tolerance]")
        sys.exit(1)
        
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    tol = int(sys.argv[3]) if len(sys.argv) > 3 else 40
    low_tol = int(sys.argv[4]) if len(sys.argv) > 4 else 15
    
    remove_background(input_path, output_path, tol, low_tol)
