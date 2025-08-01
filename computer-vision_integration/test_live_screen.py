import mss
import numpy as np
import cv2

def main():
    sct = mss.mss()
    monitor = sct.monitors[1]  # [1] is the primary monitor

    print("Displaying live screen capture. Press 'q' to exit.")

    SCALE = 0.5  # Scale factor (0.5 = 50% of original size)

    while True:
        img = sct.grab(monitor)
        frame = np.array(img)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

        # Resize for display
        frame_resized = cv2.resize(frame, (0, 0), fx=SCALE, fy=SCALE)

        cv2.imshow("Screen Capture (press q to quit)", frame_resized)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()