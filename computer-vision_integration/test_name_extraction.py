import cv2
import pytesseract
import pandas as pd

# Load image
image = cv2.imread("test-data/bf169fce.jpg")

# Optional: Resize if too small
# image = cv2.resize(image, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Optional preprocessing
# gray = cv2.GaussianBlur(gray, (3, 3), 0)
# gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

# Get OCR data
data = pytesseract.image_to_data(gray, output_type=pytesseract.Output.DATAFRAME)
data = data.dropna(subset=["text"])
data = data[data.conf > 30]  # Confidence threshold

# Group words by block, paragraph, and line
grouped = data.groupby(['block_num', 'par_num', 'line_num'])

# Iterate over lines
for _, group in grouped:
    text = " ".join(group['text'].tolist())
    x = group['left'].min()
    y = group['top'].min()
    x2 = group['left'].max() + group['width'][group['left'].idxmax()]
    y2 = group['top'].max() + group['height'][group['top'].idxmax()]

    # Draw bounding box
    cv2.rectangle(image, (x, y), (x2, y2), (0, 255, 0), 2)
    cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

# Display the result
cv2.imshow("Names Detected", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
