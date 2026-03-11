from PIL import Image
import os

def generate_rom_data(image_path, output_file):
    try:
        # 1. Load the image
        img = Image.open(image_path)
        
        # 2. Handle transparent backgrounds
        # If the image has an alpha channel (RGBA), paste it onto a pure white background first
        if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
            white_bg = Image.new("RGB", img.size, (255, 255, 255))
            white_bg.paste(img, mask=img.convert('RGBA').split()[3])
            img = white_bg # Replace the original image with the processed white-background version
            
        # 3. Now it is safe to convert to grayscale
        img = img.convert('L')
        
    except Exception as e:
        print(f"Image not found or could not be opened: {e}")
        return 

    width, height = img.size
    
    with open(output_file, "w") as f:
        f.write(f"// --- Processing: {os.path.basename(image_path)} ({width}x{height}) ---\n")

        if height != 32:
            f.write("// ERROR: Image height must be exactly 32 pixels.\n")
            print("Error: Image height is not 32 pixels.")
            return

        if width == 32:
            f.write("// --- 32x32 Image Data ---\n")
            extract_pixels(img, 0, 32, 32, f)
            print(f"Conversion successful! Open {output_file} to view the result.")
            
        elif width == 64:
            f.write("// --- 64x32 Image Data (Left Half) ---\n")
            extract_pixels(img, 0, 32, 32, f)
            
            f.write("\n// --- 64x32 Image Data (Right Half) ---\n")
            extract_pixels(img, 32, 64, 32, f)
            print(f"Conversion successful! Open {output_file} to view the result.")
            
        else:
            f.write("// ERROR: Image width must be 32 or 64 pixels.\n")
            print("Error: Image width is not 32 or 64 pixels.")

def extract_pixels(img, start_x, end_x, height, file_handle):
    for y in range(height):
        row_binary = ""
        for x in range(start_x, end_x):
            pixel_value = img.getpixel((x, y))
            # Threshold: values below 128 are treated as black pixels (1),
            # and values of 128 or above are treated as white background (0)
            if pixel_value < 128:
                row_binary += "1" 
            else:
                row_binary += "0"
        
        file_handle.write(f"32'b{row_binary},\n")

# --- Execution block ---
if __name__ == "__main__":
    # Replace these with your actual file names. You can also change the output path to your desktop.
    image_file = r"C:\Users\Wind_Hsu\Desktop\EE2026\EE2026_project_pictures\Wire.png" 
    output_text = r"C:\Users\Wind_Hsu\Desktop\EE2026\EE2026_project_pictures\Wire.txt"
    
    if os.path.exists(image_file):
        generate_rom_data(image_file, output_text)
    else:
        print(f"Could not find '{image_file}'. Please make sure the image and this Python file are in the same folder.")
    
    input("\nExecution finished. Press Enter to exit...")
