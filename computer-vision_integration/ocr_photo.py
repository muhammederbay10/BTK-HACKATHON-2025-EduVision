# ocr_photo.py
import os
import json
import cv2
import easyocr

def ensure_photo_dir_exists(photo_dir="photo_id"):
    if not os.path.exists(photo_dir):
        os.makedirs(photo_dir)
    return photo_dir

def crop_face_with_padding(frame, face_landmarks, frame_w, frame_h, 
                          pad_left_ratio=0.2, pad_right_ratio=0.2,
                          pad_top_ratio=0.3, pad_bottom_ratio=0.4):
    points = [(int(lm.x * frame_w), int(lm.y * frame_h)) for lm in face_landmarks.landmark]
    x_vals, y_vals = zip(*points)
    min_x, max_x = min(x_vals), max(x_vals)
    min_y, max_y = min(y_vals), max(y_vals)
    box_w = max_x - min_x
    box_h = max_y - min_y
    pad_left = int(box_w * pad_left_ratio)
    pad_right = int(box_w * pad_right_ratio)
    pad_top = int(box_h * pad_top_ratio)
    pad_bottom = int(box_h * pad_bottom_ratio)
    x1 = max(min_x - pad_left, 0)
    y1 = max(min_y - pad_top, 0)
    x2 = min(max_x + pad_right, frame_w-1)
    y2 = min(max_y + pad_bottom, frame_h-1)
    return frame[y1:y2, x1:x2]

def extract_name_easyocr_from_array(img_array, show_debug=False):
    reader = easyocr.Reader(['en'], gpu=False)
    h, w = img_array.shape[:2]
    scale = 4
    image_up = cv2.resize(img_array, (w * scale, h * scale), interpolation=cv2.INTER_CUBIC)
    h_up, w_up = image_up.shape[:2]
    crop_top = int(h_up * 0.60)
    crop_left = 0
    crop_bottom = h_up
    crop_right = int(w_up * 0.80)
    cropped = image_up[crop_top:crop_bottom, crop_left:crop_right]
    results = reader.readtext(cropped)
    if show_debug:
        for (bbox, text, confidence) in results:
            print(f"[{confidence:.2f}] {text}")
        cv2.imwrite("debug_output.jpg", cropped)
        print("Saved debug image as debug_output.jpg")
    if results:
        results.sort(key=lambda r: r[0][0][0])
        return " ".join([r[1] for r in results])
    else:
        return "Name not found"

def save_face_photo(frame, face_landmarks, frame_w, frame_h, student_id, photo_dir="photo_id"):
    points = [(int(lm.x * frame_w), int(lm.y * frame_h)) for lm in face_landmarks.landmark]
    x_vals, y_vals = zip(*points)
    min_x, max_x = min(x_vals), max(x_vals)
    min_y, max_y = min(y_vals), max(y_vals)
    box_w = max_x - min_x
    box_h = max_y - min_y
    pad_left_ratio = 1.3
    pad_right_ratio = 0.2
    pad_top_ratio = 0.3
    pad_bottom_ratio = 0.4
    pad_left = int(box_w * pad_left_ratio)
    pad_right = int(box_w * pad_right_ratio)
    pad_top = int(box_h * pad_top_ratio)
    pad_bottom = int(box_h * pad_bottom_ratio)
    x1 = max(min_x - pad_left, 0)
    y1 = max(min_y - pad_top, 0)
    x2 = min(max_x + pad_right, frame_w-1)
    y2 = min(max_y + pad_bottom, frame_h-1)
    face_img = frame[y1:y2, x1:x2]
    out_path = os.path.join(photo_dir, f"{student_id}.jpg")
    cv2.imwrite(out_path, face_img)

def handle_new_student(frame, face_landmarks, frame_w, frame_h, student_id, mapping_json_path, photo_dir="photo_id"):
    wide_img = crop_face_with_padding(
        frame, face_landmarks, frame_w, frame_h,
        pad_left_ratio=1.3, pad_right_ratio=0.2,
        pad_top_ratio=0.3, pad_bottom_ratio=0.4
    )
    name = extract_name_easyocr_from_array(wide_img, show_debug=False)
    print(f"OCR got name: {name}")

    if os.path.exists(mapping_json_path):
        with open(mapping_json_path, 'r') as f:
            mapping = json.load(f)
    else:
        mapping = {}
    mapping[student_id] = name
    os.makedirs(os.path.dirname(mapping_json_path), exist_ok=True)
    with open(mapping_json_path, 'w') as f:
        json.dump(mapping, f, indent=2)

    normal_img = crop_face_with_padding(
        frame, face_landmarks, frame_w, frame_h,
        pad_left_ratio=0.30, pad_right_ratio=0.30,
        pad_top_ratio=0.50, pad_bottom_ratio=0.50
    )
    os.makedirs(photo_dir, exist_ok=True)
    normal_img_path = os.path.join(photo_dir, f"{student_id}.jpg")
    cv2.imwrite(normal_img_path, normal_img)
