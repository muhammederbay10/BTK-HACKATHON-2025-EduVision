# attention_tracker.py
import argparse
import sys
import traceback
import cv2
from frame_processor import initialize_tracking, process_frame

def main():
    parser = argparse.ArgumentParser(description='Attention Tracker (short main)')
    parser.add_argument('--video_path', type=str, default='test-data/test_video.mp4')
    parser.add_argument('--output_csv', type=str, default='student_attention_log.csv')
    args = parser.parse_args()

    cap, face_mesh, mapping_json_path, id_name_mapping, csv_file_path, frame_idx, photo_dir = initialize_tracking(
        args.video_path, args.output_csv
    )

    if not cap.isOpened():
        sys.exit("Error: Could not open video source")

    try:
        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                break

            if not args.video_path:  # webcam flip
                frame = cv2.flip(frame, 1)

            frame, frame_idx, id_name_mapping = process_frame(
                frame, face_mesh, mapping_json_path, id_name_mapping, csv_file_path, frame_idx
            )

            if not args.video_path:
                cv2.imshow('Multi-Person Attention Tracker', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

    except Exception as e:
        print("Runtime error:", e)
        traceback.print_exc()
    finally:
        cap.release()
        cv2.destroyAllWindows()
        print(f"Done. Results saved to: {csv_file_path}")

if __name__ == "__main__":
    main()