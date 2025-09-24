import cv2
import numpy as np


# 1. SIMPLEST: Create and show a colored window
def colored_window():
    # Create a 400x400 blue image
    blue_img = np.zeros((400, 400, 3), dtype=np.uint8)
    blue_img[:] = (255, 0, 0)  # BGR format: Blue

    cv2.imshow('Blue Window', blue_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# 2. SIMPLE: Draw on a blank canvas
def simple_drawing():
    # Black canvas
    canvas = np.zeros((300, 500, 3), dtype=np.uint8)

    # Draw a smiley face
    cv2.circle(canvas, (250, 150), 80, (0, 255, 255), 3)  # Yellow circle (face)
    cv2.circle(canvas, (220, 120), 10, (0, 255, 255), -1)  # Left eye
    cv2.circle(canvas, (280, 120), 10, (0, 255, 255), -1)  # Right eye
    cv2.ellipse(canvas, (250, 170), (30, 15), 0, 0, 180, (0, 255, 255), 2)  # Smile

    cv2.imshow('Smiley', canvas)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# 3. SIMPLE: Basic webcam with effects
def webcam_with_effects():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Apply different effects based on key press
        key = cv2.waitKey(1) & 0xFF

        if key == ord('g'):  # Grayscale
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
        elif key == ord('b'):  # Blur
            frame = cv2.GaussianBlur(frame, (21, 21), 0)
        elif key == ord('e'):  # Edges
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 50, 150)
            frame = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

        cv2.imshow('Webcam - Press g/b/e for effects, q to quit', frame)

        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


# 4. SIMPLE: Mouse drawing
def mouse_drawing():
    drawing = False

    def draw_circle(event, x, y, flags, param):
        nonlocal drawing

        if event == cv2.EVENT_LBUTTONDOWN:
            drawing = True
        elif event == cv2.EVENT_MOUSEMOVE and drawing:
            cv2.circle(img, (x, y), 5, (0, 255, 0), -1)
        elif event == cv2.EVENT_LBUTTONUP:
            drawing = False

    # Create black image
    img = np.zeros((512, 512, 3), dtype=np.uint8)
    cv2.namedWindow('Draw with Mouse')
    cv2.setMouseCallback('Draw with Mouse', draw_circle)

    while True:
        cv2.imshow('Draw with Mouse', img)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('c'):  # Clear canvas
            img[:] = 0

    cv2.destroyAllWindows()


# 5. SIMPLE: Color picker from webcam
def color_picker():
    def pick_color(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            # Get the color at clicked position
            b, g, r = frame[y, x]
            print(f"Color at ({x}, {y}): B={b}, G={g}, R={r}")

            # Show the color in a separate window
            color_sample = np.full((100, 100, 3), (b, g, r), dtype=np.uint8)
            cv2.imshow('Picked Color', color_sample)

    cap = cv2.VideoCapture(0)
    cv2.namedWindow('Color Picker - Click to pick color')
    cv2.setMouseCallback('Color Picker - Click to pick color', pick_color)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow('Color Picker - Click to pick color', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


# 6. SIMPLE: Motion detection
def simple_motion_detection():
    cap = cv2.VideoCapture(0)

    # Read first frame
    ret, frame1 = cap.read()
    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    gray1 = cv2.GaussianBlur(gray1, (21, 21), 0)

    while True:
        ret, frame2 = cap.read()
        if not ret:
            break

        gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.GaussianBlur(gray2, (21, 21), 0)

        # Find difference between frames
        diff = cv2.absdiff(gray1, gray2)
        thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1]

        # Find contours of moving objects
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            if cv2.contourArea(contour) > 1000:  # Only large movements
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(frame2, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame2, 'MOTION', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        cv2.imshow('Motion Detection', frame2)
        cv2.imshow('Difference', thresh)

        # Update background
        gray1 = gray2.copy()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


# Run one of these functions
if __name__ == "__main__":
    print("Choose an implementation:")
    print("1 - Colored window")
    print("2 - Simple drawing")
    print("3 - Webcam with effects")
    print("4 - Mouse drawing")
    print("5 - Color picker")
    print("6 - Motion detection")

    choice = input("Enter number (1-6): ")

    if choice == '1':
        colored_window()
    elif choice == '2':
        simple_drawing()
    elif choice == '3':
        webcam_with_effects()
    elif choice == '4':
        mouse_drawing()
    elif choice == '5':
        color_picker()
    elif choice == '6':
        simple_motion_detection()
    else:
        print("Invalid choice!")