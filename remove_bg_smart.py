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


def remove_bg_ai(image_path, output_path, model_name="isnet-general", alpha_matting=False, post_process_mask=False):
    try:
        from rembg import remove, new_session
    except ImportError:
        print("\n[!] Error: The 'rembg' library is required for AI/Hybrid mode.")
        print("Please install it using: pip install rembg")
        print("Note: To run with GPU support, install: pip install rembg[gpu]\n")
        sys.exit(1)
        
    print(f"Loading image for AI processing: {image_path}")
    img = Image.open(image_path)
    
    print(f"Initializing AI model '{model_name}' (this may take a few seconds on first run)...")
    try:
        session = new_session(model_name)
        print(f"Processing background removal (alpha_matting={alpha_matting}, post_process_mask={post_process_mask})...")
        out_img = remove(
            img, 
            session=session,
            alpha_matting=alpha_matting,
            post_process_mask=post_process_mask
        )
        out_img.save(output_path, "PNG")
        print(f"Saved transparent image (AI Mode) to: {output_path}")
    except Exception as e:
        print(f"[!] AI Processing failed: {e}")
        sys.exit(1)


def remove_bg_hybrid(image_path, output_path, model_name="isnet-anime", tolerance=75, low_tolerance=35, erosion_iterations=15):
    try:
        from rembg import remove, new_session
    except ImportError:
        print("\n[!] Error: The 'rembg' library is required for Hybrid mode.")
        print("Please install it using: pip install rembg")
        sys.exit(1)
        
    print(f"Loading image for Hybrid processing: {image_path}")
    img = Image.open(image_path).convert("RGBA")
    arr = np.array(img)
    
    # 1. Run AI to get the initial alpha mask
    print(f"Running AI segmentation using '{model_name}' to find character boundaries...")
    try:
        session = new_session(model_name)
        ai_out = remove(img, session=session)
        ai_arr = np.array(ai_out)
        ai_alpha = ai_arr[:, :, 3].astype(np.float32)
    except Exception as e:
        print(f"[!] AI phase failed: {e}")
        sys.exit(1)
        
    # 2. Detect the background color dynamically from AI-confirmed background pixels (alpha == 0)
    bg_pixels = arr[ai_alpha == 0, :3]
    if len(bg_pixels) == 0:
        # Fallback to corner pixels if AI mask covers the entire image
        h, w, _ = arr.shape
        corners = [arr[0, 0, :3], arr[0, w-1, :3], arr[h-1, 0, :3], arr[h-1, w-1, :3]]
        bg_color = np.mean(corners, axis=0).astype(np.int32)
    else:
        bg_color = np.mean(bg_pixels, axis=0).astype(np.int32)
    print(f"Detected background color from AI-background region: {bg_color}")
    
    # 3. Calculate distance to background color for each pixel
    diff = arr[:, :, :3].astype(np.int32) - bg_color
    dist = np.sqrt(np.sum(diff ** 2, axis=-1))
    
    # 4. Create a Core Protection Mask by eroding the character mask
    # This prevents details inside the character's body (like blue eyes or highlights) from turning transparent
    character_mask = ai_alpha > 127
    core_mask = ndimage.binary_erosion(character_mask, iterations=erosion_iterations)
    
    # 5. Color-based transparency multiplier
    with np.errstate(divide='ignore', invalid='ignore'):
        color_factor = (dist - low_tolerance) / (tolerance - low_tolerance)
        color_factor = np.clip(color_factor, 0.0, 1.0)
        
    # Apply core protection: pixels in core_mask must remain fully opaque/unmodified by color distance
    color_factor[core_mask] = 1.0
    
    # Multiply the AI alpha by the color factor
    new_alpha = (ai_alpha * color_factor).astype(np.uint8)
    
    # Update alpha channel and save
    arr[:, :, 3] = new_alpha
    out_img = Image.fromarray(arr)
    out_img.save(output_path, "PNG")
    print(f"Saved transparent image (Hybrid Mode) to: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Smart Background Remover: Supports precise solid color keying, standard AI segmentation, and hybrid matting."
    )
    parser.add_argument("input", help="Path to input image file")
    parser.add_argument("output", help="Path to output transparent PNG file")
    parser.add_argument(
        "--mode", 
        choices=["solid", "ai", "hybrid"], 
        default="solid", 
        help="Processing mode: 'solid' for logos/solid backgrounds, 'ai' for general photos, 'hybrid' for complex anime/illustration hair details"
    )
    parser.add_argument(
        "--model", 
        default="isnet-anime", 
        help="AI model to use (for 'ai' and 'hybrid' modes). Examples: isnet-anime (anime), birefnet-general (general), u2net"
    )
    parser.add_argument(
        "--tolerance", 
        type=int, 
        default=40, 
        help="Tolerance threshold for background color detection (default: 40 for solid, 75 for hybrid)"
    )
    parser.add_argument(
        "--low-tolerance", 
        type=int, 
        default=15, 
        help="Lower tolerance limit for soft edge blending (default: 15 for solid, 35 for hybrid)"
    )
    parser.add_argument(
        "--alpha-matting",
        action="store_true",
        help="Use rembg built-in alpha matting for edge/hair refinement (only for --mode ai)"
    )
    parser.add_argument(
        "--post-process-mask",
        action="store_true",
        help="Post process the mask to clean up small artifacts (only for --mode ai)"
    )
    parser.add_argument(
        "--erosion-iterations",
        type=int,
        default=15,
        help="Number of erosion iterations to protect the core body of the character (only for --mode hybrid)"
    )
    
    args = parser.parse_args()
    
    # Apply context-aware defaults for tolerance if they were not explicitly changed
    if args.mode == "hybrid":
        # Check if they are still at default values, if so, upgrade to hybrid defaults
        if args.tolerance == 40:
            args.tolerance = 75
        if args.low_tolerance == 15:
            args.low_tolerance = 35
            
    if args.mode == "solid":
        remove_bg_solid(args.input, args.output, args.tolerance, args.low_tolerance)
    elif args.mode == "ai":
        remove_bg_ai(args.input, args.output, args.model, args.alpha_matting, args.post_process_mask)
    elif args.mode == "hybrid":
        remove_bg_hybrid(args.input, args.output, args.model, args.tolerance, args.low_tolerance, args.erosion_iterations)


if __name__ == "__main__":
    main()
