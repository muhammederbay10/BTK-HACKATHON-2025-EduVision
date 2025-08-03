import cv2
import pytesseract
import numpy as np
import re

def extract_name_from_zoom_image(image_path, show_debug=False):
    # Load and check image
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Could not load image: {image_path}")
    
    h, w = image.shape[:2]

    # Step 1: Resize up (4x)
    upscale_factor = 4
    image_up = cv2.resize(image, (w * upscale_factor, h * upscale_factor), interpolation=cv2.INTER_CUBIC)
    h_up, w_up = image_up.shape[:2]

    # Step 2: Crop bottom left quarter (names typically here)
    crop = image_up[int(h_up * 0.75):h_up, int(w_up * 0.02):int(w_up * 0.6)]

    # Step 3: Grayscale
    gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)

    # Step 4: Sharpen
    sharpen_kernel = np.array([[-1, -1, -1],
                                [-1,  9, -1],
                                [-1, -1, -1]])
    sharp = cv2.filter2D(gray, -1, sharpen_kernel)

    # Step 5: Binary threshold
    _, binary = cv2.threshold(sharp, 150, 255, cv2.THRESH_BINARY)

    # Step 6: OCR
    config = "--oem 3 --psm 7"
    raw_text = pytesseract.image_to_string(binary, config=config)

    # Optional: Visual debug
    if show_debug:
        cv2.imshow("Cropped Region", crop)
        cv2.imshow("OCR Input", binary)
        print("[DEBUG] Raw OCR Text:", repr(raw_text))
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    # Step 7: Clean result — keep only lines with letters
    lines = [line.strip() for line in raw_text.split('\n') if re.search(r'[A-Za-z]', line)]
    name = lines[0] if lines else "Name not found"
    return name

if __name__ == "__main__":
    image_path = "test-data/6cc5ce3c.jpg"
    name = extract_name_from_zoom_image(image_path, show_debug=True)
    print("Extracted Name:", name)
