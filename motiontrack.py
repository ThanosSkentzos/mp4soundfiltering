import cv2
import numpy as np

cap = cv2.VideoCapture(0)

# Read first frame and convert to grayscale
ret, frame = cap.read()
if not ret:
    print("Error: Couldn't access webcam.")
    cap.release()
    cv2.destroyAllWindows()
    exit()

old_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

lk_params = dict(winSize=(15, 15),
                 maxLevel=2,
                 criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

def select_point(event, x, y, flags, param):
    global point_selected, point, old_points
    if event == cv2.EVENT_LBUTTONDOWN:
        point = (x, y)
        point_selected = True
        old_points = np.array([[x, y]], dtype=np.float32)

cv2.namedWindow("Motion Tracker")
cv2.setMouseCallback("Motion Tracker", select_point)

point_selected = False
point = (0, 0)
old_points = np.array([[]])
mask = np.zeros_like(frame) #develop a empty image to track motion trail

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    if point_selected:
        cv2.circle(frame, point, 5, (0, 0, 255), 2)

        new_points, status, error = cv2.calcOpticalFlowPyrLK(old_gray, gray_frame, old_points, None, **lk_params)

        if new_points is not None and len(new_points) > 0:
            x, y = new_points.ravel()
            new_point = (int(x), int(y))

            mask = cv2.line(mask, point, new_point, (0, 255, 0), 2)
            frame = cv2.circle(frame, new_point, 5, (0, 255, 0), -1)

            # Update old points and frame and Update tracked point
            old_gray = gray_frame.copy()
            old_points = new_points.reshape(-1, 1, 2)
            point = new_point

        # Merge frame with mask to show motion trails
        frame = cv2.add(frame, mask)

    cv2.imshow("Motion Tracker", frame)

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()