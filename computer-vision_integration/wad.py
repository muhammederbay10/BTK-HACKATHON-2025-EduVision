import cv2
import dlib

# Load the dlib face detector
detector = dlib.get_frontal_face_detector()

# Load the image
image_path = 'test-data/test_frame.png'  # Replace with your image
image = cv2.imread(image_path)

# Check if the image was loaded successfully
if image is None:
    print("Error: Could not load the image.")
    exit()

# Convert image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Detect faces using dlib's face detector
faces = detector(gray)

# Draw rectangles around detected faces
for face in faces:
    x, y, w, h = (face.left(), face.top(), face.width(), face.height())
    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

# Save the resulting image with faces detected
output_path = 'output_dlib_image.png'
cv2.imwrite(output_path, image)

print(f"Image with detected faces using dlib saved as {output_path}")
