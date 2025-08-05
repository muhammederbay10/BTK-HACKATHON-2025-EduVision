import cv2
from facenet_pytorch import MTCNN
import matplotlib.pyplot as plt
import numpy as np

# Initialize MTCNN for face detection (FaceNet)
mtcnn = MTCNN(keep_all=True)

# Load an image (provide the path to your image)
image_path = 'test-data/test_frame.png'  # Replace with the correct image path
image = cv2.imread(image_path)

# Check if the image was loaded successfully
if image is None:
    print("Error: Could not load the image.")
    exit()

# Convert the image from BGR (OpenCV) to RGB (for MTCNN)
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Detect faces
boxes, probs = mtcnn.detect(image_rgb)

# Draw bounding boxes on the image for each detected face
for box in boxes:
    cv2.rectangle(image, 
                  (int(box[0]), int(box[1])), 
                  (int(box[2]), int(box[3])), 
                  (0, 255, 0), 2)  # Green rectangle

# Save the processed image with detected faces
output_path = 'output_facetnet_image.png'
cv2.imwrite(output_path, image)

print(f"Image with detected faces saved as {output_path}")

# Optionally, display the image using matplotlib (for easier viewing in notebooks)
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.axis('off')  # Hide axes
plt.show()
