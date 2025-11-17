import os
import cv2
import numpy as np
import time

DEFAULT_PASSWORD = "2468"

password_buffer = ""
clicked = None
result_message = None

buttons = {
    "1": (150,150,250,230),
    "2": (300,150,400,230),
    "3": (450,150,550,230),

    "4": (150,250,250,330),
    "5": (300,250,400,330),
    "6": (450,250,550,330),

    "7": (150,350,250,430),
    "8": (300,350,400,430),
    "9": (450,350,550,430),

    "C": (150,450,250,530),
    "0": (300,450,400,530),
    "OK":(450,450,550,530)
}

back_button = (20, 20, 150, 70)

def ensure_password_file():
    if not os.path.exists("password.txt"):
        with open("password.txt", "w") as f:
            f.write(DEFAULT_PASSWORD)
        print("[INFO] password.txt created with default password 2468.")

def load_password():
    ensure_password_file()
    with open("password.txt", "r") as f:
        return f.read().strip()

def verify_password(input_pw):
    return input_pw == load_password()

def draw_keypad():
    img = np.zeros((600,800,3), dtype=np.uint8)

    (bx1, by1, bx2, by2) = back_button
    cv2.rectangle(img, (bx1,by1), (bx2,by2), (255,255,255), 2)
    cv2.putText(img, "BACK", (bx1+10, by1+35),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)

    cv2.putText(img, "ENTER PASSWORD", (200, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1.6, (0, 255, 255), 3)

    display = "*" * len(password_buffer)
    cv2.putText(img, display, (330, 100),
                cv2.FONT_HERSHEY_SIMPLEX, 1.6, (0, 255, 0), 3)

    if result_message is not None:
        text = "Correct!" if result_message == "correct" else "Wrong Password"

        PASSWORD_Y = 150
        text_y = PASSWORD_Y - 20

        text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1.2, 3)[0]
        text_x = int((800 - text_size[0]) / 2)

        color = (0, 255, 0) if result_message == "correct" else (0, 0, 255)

        cv2.putText(img, text, (text_x, text_y),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3)

    for text,(x1,y1,x2,y2) in buttons.items():
        cv2.rectangle(img, (x1,y1), (x2,y2), (255,255,255), 3)

        if text == "OK":
            text_x = x1 + 15
            font_scale = 1.6
        else:
            text_x = x1 + 35
            font_scale = 1.8

        cv2.putText(img, text, (text_x, y1 + 65),
                    cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255,255,255), 3)

    return img

def mouse_callback(event, x, y, flags, param):
    global clicked

    if event == cv2.EVENT_LBUTTONDOWN:

        (bx1, by1, bx2, by2) = back_button
        if bx1 <= x <= bx2 and by1 <= y <= by2:
            clicked = "BACK"
            return

        for key,(x1,y1,x2,y2) in buttons.items():
            if x1 <= x <= x2 and y1 <= y <= y2:
                clicked = key
                return

def password_screen():
    global password_buffer, clicked, result_message

    password_buffer = ""
    result_message = None
    clicked = None
    message_start_time = None

    cv2.namedWindow("Password", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Password", 800, 600)
    cv2.setMouseCallback("Password", mouse_callback)

    while True:

        if result_message is not None:
            if time.time() - message_start_time > 1.2:
                result_message = None

        img = draw_keypad()
        cv2.imshow("Password", img)

        if clicked:
            key = clicked
            clicked = None

            if key == "BACK":
                cv2.destroyWindow("Password")
                return

            elif key == "C":
                password_buffer = ""
                result_message = None

            elif key == "OK":
                if verify_password(password_buffer):
                    result_message = "correct"
                else:
                    result_message = "wrong"

                password_buffer = ""

                message_start_time = time.time()

            else:
                password_buffer += key

        if cv2.waitKey(10) & 0xFF == ord('q'):
            cv2.destroyWindow("Password")
            return

if __name__ == "__main__":
    password_screen()

