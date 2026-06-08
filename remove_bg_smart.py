import os
import sys
import argparse
import numpy as np
from PIL import Image
import scipy.ndimage as ndimage

def remove_bg_solid(image_path, output_path, tolerance=40, low_tolerance=15):
    print(f"Loading image: {image_path}")
    img = Image.open(image_path).convert("RGBA")
    arr = np.array(img)
    h, w, _ = arr.shape
    
    # Detect background color from corners
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
    
    # Copy the original alpha channel
    alpha = arr[:, :, 3].copy()
    
    # Calculate soft alpha for anti-aliasing
    with np.errstate(divide='ignore', invalid='ignore'):
        alpha_factor = (dist - low_tolerance) / (tolerance - low_tolerance)
        alpha_factor = np.clip(alpha_factor, 0.0, 1.0)
        
    # For background mask pixels, apply the soft alpha_factor
    alpha[background_mask] = (alpha[background_mask] * alpha_factor[background_mask]).astype(np.uint8)
    
    # Update the alpha channel
    arr[:, :, 3] = alpha
    
    # Save the output image
    out_img = Image.fromarray(arr)
    out_img.save(output_path, "PNG")
    print(f"Saved transparent image (Solid Mode) to: {output_path}")


def remove_bg_ai(image_path, output_path, model_name="isnet-general"):
    try:
        from rembg import remove, new_session
    except ImportError:
        print("\n[!] Error: The 'rembg' library is required for AI mode.")
        print("Please install it using: pip install rembg")
        print("Note: To run with GPU support, install: pip install rembg[gpu]\n")
        sys.exit(1)
        
    print(f"Loading image for AI processing: {image_path}")
    img = Image.open(image_path)
    
    print(f"Initializing AI model '{model_name}' (this may take a few seconds on first run)...")
    try:
        session = new_session(model_name)
        print("Processing background removal using AI...")
        out_img = remove(img, session=session)
        out_img.save(output_path, "PNG")
        print(f"Saved transparent image (AI Mode) to: {output_path}")
    except Exception as e:
        print(f"[!] AI Processing failed: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Smart Background Remover: Supports precise solid color keying and advanced AI-based segmentation."
    )
    parser.add_argument("input", help="Path to input image file")
    parser.add_argument("output", help="Path to output transparent PNG file")
    parser.add_argument(
        "--mode", 
        choices=["solid", "ai"], 
        default="solid", 
        help="Processing mode: 'solid' for solid/logo backgrounds (flood-fill), 'ai' for complex/scenic backgrounds"
    )
    parser.add_argument(
        "--model", 
        default="isnet-general", 
        help="AI model to use (only for --mode ai). Examples: isnet-general (best for anime/illustrations), birefnet-general (best for general images), u2net"
    )
    parser.add_argument(
        "--tolerance", 
        type=int, 
        default=40, 
        help="Tolerance threshold for solid background detection (only for --mode solid)"
    )
    parser.add_argument(
        "--low-tolerance", 
        type=int, 
        default=15, 
        help="Lower tolerance limit for soft edge blending (only for --mode solid)"
    )
    
    args = parser.parse_args()
    
    if args.mode == "solid":
        remove_bg_solid(args.input, args.output, args.tolerance, args.low_tolerance)
    elif args.mode == "ai":
        remove_bg_ai(args.input, args.output, args.model)


if __name__ == "__main__":
    main()
