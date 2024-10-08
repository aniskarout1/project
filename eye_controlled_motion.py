#pip install opencv                         #Run the code in terminal which are comment out
#pip install mediapipe
#pip install pyautogui
import cv2
import mediapipe as mp
import pyautogui
import pyttsx3

cam = cv2.VideoCapture(0)
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
screen_w, screen_h = pyautogui.size()

def zoom_in():
    pyautogui.hotkey('ctrl', '+')

def zoom_out():
    pyautogui.hotkey('ctrl', '-')

def process_eye_zoom(eye_x, eye_y):
    # Top-right corner for zoom in
    if eye_x > screen_w * 0.75 and eye_y < screen_h * 0.25:
        zoom_in()
    # Bottom-left corner for zoom out
    elif eye_x < screen_w * 0.25 and eye_y > screen_h * 0.75:
        zoom_out()

def eye():
    while True:
        _, frame = cam.read()
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        output = face_mesh.process(rgb_frame)
        landmark_points = output.multi_face_landmarks
        frame_h, frame_w, _ = frame.shape
        if landmark_points:
            landmarks = landmark_points[0].landmark
            for id, landmark in enumerate(landmarks[474:478]):
                x = int(landmark.x * frame_w)
                y = int(landmark.y * frame_h)
                cv2.circle(frame, (x, y), 3, (0, 255, 0))
                if id == 1:
                    screen_x = screen_w * landmark.x
                    screen_y = screen_h * landmark.y
                    pyautogui.moveTo(screen_x, screen_y)

                    # Call zoom function based on eye position
                    process_eye_zoom(screen_x, screen_y)
                    
            left = [landmarks[145], landmarks[159]]
            for landmark in left:
                x = int(landmark.x * frame_w)
                y = int(landmark.y * frame_h)
                cv2.circle(frame, (x, y), 3, (0, 255, 255))
            if (left[0].y - left[1].y) < 0.008:
                pyautogui.doubleClick()
                pyautogui.sleep(1)
            right = [landmarks[374], landmarks[386]]
            for landmarks in right:
                x = int(landmarks.x * frame_w)
                y = int(landmarks.y * frame_h)
                cv2.circle(frame, (x,y), 3, (0, 0, 255))
            if(left[0].y - left[1].y < 0.006):
                pyautogui.rightClick()
                pyautogui.sleep(1)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cv2.imshow('Eye Controlled Mouse', frame)
        cv2.waitKey(1)

eye()