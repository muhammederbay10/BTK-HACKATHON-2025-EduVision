import cv2
import easyocr
import numpy as np

def extract_name_easyocr(image_path, show_debug=False):
    # Load image
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Could not load image: {image_path}")
    
    h, w = image.shape[:2]

    # Resize image for better OCR (4x scale)
    scale = 4
    image_up = cv2.resize(image, (w * scale, h * scale), interpolation=cv2.INTER_CUBIC)

    # Expanded crop region to handle slight position changes
    h_up, w_up = image_up.shape[:2]
    crop_top = int(h_up * 0.60)   # Start from 60% of height instead of 75%
    crop_left = 0                 # Start from far left
    crop_bottom = h_up            # Bottom edge
    crop_right = int(w_up * 0.80) # Cover 80% width instead of 60%

    cropped = image_up[crop_top:crop_bottom, crop_left:crop_right]

    # Create EasyOCR reader
    reader = easyocr.Reader(['en'], gpu=False)

    # Run OCR
    results = reader.readtext(cropped)

    # Optional debug
    if show_debug:
        for (bbox, text, confidence) in results:
            print(f"[{confidence:.2f}] {text}")
        cv2.imwrite("debug_output.jpg", cropped)
        print("Saved debug image as debug_output.jpg")

    # Extract name (sorted left-to-right)
    if results:
        results.sort(key=lambda r: r[0][0][0])
        return " ".join([r[1] for r in results])
    else:
        return "Name not found"

if __name__ == "__main__":
    path = "test-data/bf169fce.jpg"
    name = extract_name_easyocr(path, show_debug=True)
    print("Extracted Name:", name)
