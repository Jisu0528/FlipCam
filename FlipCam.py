import cv2 as cv
from datetime import datetime

def main():
    cap = cv.VideoCapture(0)  # Get camera video

    # Set camera video properties
    width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
    fps = 30
    fourcc = cv.VideoWriter_fourcc(*'XVID')
    out = None
    is_recording = False
    mode = 'normal' # Initial mode: normal

    while True:
        valid, img = cap.read()
        if not valid:
            break
        
        # Change image mode
        if mode == 'flip_horizontal':
            img = cv.flip(img, 1)  # Horizontal flip
        elif mode == 'invert_colors':
            img = cv.bitwise_not(img)  # Invert colors

        # Add current time to filename
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"FlipCam_{current_time}.avi"

        # Add circle to frame when recording
        if is_recording:
            cv.circle(img, (20, 20), radius=5, color=(0, 0, 255), thickness=-1)

        cv.imshow('FlipCam', img) # Display video on screen

        # Save video if in recording mode
        if is_recording:
            if out is None:
                out = cv.VideoWriter(filename, fourcc, fps, (width, height))
            out.write(img)

        # Key input handling
        key = cv.waitKey(1)
        if key == 27:   # Press ESC key to exit
            break
        elif key == 32:  # Press Space key to toggle recording mode
            is_recording = not is_recording
            if not is_recording:
                out.release()
                out = None
        elif key == ord('a'):  # Press 'a' key to change image mode to horizontal flip
            mode = 'flip_horizontal'
        elif key == ord('s'):  # Press 's' key to change image mode to invert colors
            mode = 'invert_colors'
        elif key == ord('d'):  # Press 'd' key to change image mode to normal
            mode = 'normal'

    # Release resources on exit
    cap.release()
    if out is not None:
        out.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()

