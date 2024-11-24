import argparse
from PIL import Image
import os

def png_to_tif(input_path, output_path):
    """
    Convert a PNG image to a TIFF format.
    
    Parameters:
    - input_path: str, path to the PNG image.
    - output_path: str, desired path for the output TIFF file.
    """
    try:
        # Open the PNG image
        with Image.open(input_path) as img:
            # Convert to RGB mode if necessary
            if img.mode in ("RGBA", "P"):  # RGBA for transparency, P for palette-based
                img = img.convert("RGB")
            # Save as TIFF
            img.save(output_path, format="TIFF")
        print(f"Successfully converted {input_path} to {output_path}")
    except Exception as e:
        print(f"Error converting image: {e}")

def main():
    # Argument parser setup
    parser = argparse.ArgumentParser(description="Convert PNG images to TIFF format.")
    parser.add_argument("input", help="Path to the input PNG image.")
    parser.add_argument("output", help="Path to save the output TIFF image.")
    
    # Parse the arguments
    args = parser.parse_args()
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    
    # Convert PNG to TIFF
    png_to_tif(args.input, args.output)

if __name__ == "__main__":
    main()
