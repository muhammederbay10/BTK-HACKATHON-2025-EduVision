import cv2

# Load the pre-trained Haar Cascade face detector from OpenCV
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Load an image from file (provide the path to your image)
image_path = 'test-data/test_frame.png'  # Replace with the correct image path
image = cv2.imread(image_path)

# Check if the image was loaded successfully
if image is None:
    print("Error: Could not load the image.")
    exit()

# Convert the image to grayscale (Haar Cascade works on grayscale images)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Detect faces in the image
faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

# Draw rectangles around detected faces
for (x, y, w, h) in faces:
    cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)

# Save the resulting image with detected faces
output_path = 'output_image.png'  # Path where the output image will be saved
cv2.imwrite(output_path, image)

print(f"Image with detected faces saved as {output_path}")
