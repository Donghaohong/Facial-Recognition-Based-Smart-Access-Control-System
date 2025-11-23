import os
import cv2
import numpy as np
import time

DEFAULT_ADMIN_PASSWORD = "9999"

admin_pw_buffer = ""
clicked = None
result_message = None
message_start_time = 0

buttons = {
    "1": (150,120,250,184),
    "2": (300,120,400,184),
    "3": (450,120,550,184),

    "4": (150,200,250,264),
    "5": (300,200,400,264),
    "6": (450,200,550,264),

    "7": (150,280,250,344),
    "8": (300,280,400,344),
    "9": (450,280,550,344),

    "C": (150,360,250,424),
    "0": (300,360,400,424),
    "OK":(450,360,550,424)
}

back_button = (20, 16, 150, 56)

def ensure_admin_pw_file():
    if not os.path.exists("admin_password.txt"):
        with open("admin_password.txt", "w") as f:
            f.write(DEFAULT_ADMIN_PASSWORD)
        print("[INFO] admin_password.txt created with default password 9999.")

def load_admin_password():
    ensure_admin_pw_file()
    with open("admin_password.txt", "r") as f:
        return f.read().strip()

def verify_admin_password(input_pw):
    return input_pw == load_admin_password()

def draw_admin_keypad():
    img = np.zeros((480,800,3), dtype=np.uint8)

    (bx1, by1, bx2, by2) = back_button
    cv2.rectangle(img, (bx1,by1), (bx2,by2), (255,255,255), 2)
    cv2.putText(img, "BACK", (bx1+10, by1+35),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)

    cv2.putText(img, "ADMIN LOGIN", (230, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1.6, (0, 255, 255), 3)

    display = "*" * len(admin_pw_buffer)
    cv2.putText(img, display, (330, 100),
                cv2.FONT_HERSHEY_SIMPLEX, 1.6, (0, 255, 0), 3)

    if result_message is not None:
        text = "Access Granted" if result_message == "correct" else "Wrong Password"

        text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1.2, 3)[0]
        text_x = int((800 - text_size[0]) / 2)
        text_y = 100

        color = (0,255,0) if result_message == "correct" else (0,0,255)

        cv2.putText(img, text, (text_x, text_y),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3)

    for text,(x1,y1,x2,y2) in buttons.items():
        cv2.rectangle(img, (x1,y1), (x2,y2), (255,255,255), 3)

        if text == "OK":
            text_x = x1 + 15
            scale = 1.6
        else:
            text_x = x1 + 35
            scale = 1.8

        cv2.putText(img, text, (text_x, y1 + 55),
                    cv2.FONT_HERSHEY_SIMPLEX, scale, (255,255,255), 3)

    return img

def mouse_callback(event, x, y, flags, param):
    global clicked

    if event == cv2.EVENT_LBUTTONDOWN:

        (bx1,by1,bx2,by2) = back_button
        if bx1 <= x <= bx2 and by1 <= y <= by2:
            clicked = "BACK"
            return

        for key,(x1,y1,x2,y2) in buttons.items():
            if x1 <= x <= x2 and y1 <= y <= y2:
                clicked = key
                return

def admin_login_screen():
    global admin_pw_buffer, clicked, result_message, message_start_time

    admin_pw_buffer = ""
    clicked = None
    result_message = None

    cv2.namedWindow("Admin Login", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Admin Login", 800, 480)
    cv2.setMouseCallback("Admin Login", mouse_callback)

    while True:
        if result_message is not None:
            if time.time() - message_start_time > 1.2:
                result_message = None

        img = draw_admin_keypad()
        cv2.imshow("Admin Login", img)

        if clicked:
            key = clicked
            clicked = None

            if key == "BACK":
                cv2.destroyWindow("Admin Login")
                return "BACK"

            elif key == "C":
                admin_pw_buffer = ""
                result_message = None

            elif key == "OK":
                if verify_admin_password(admin_pw_buffer):
                    result_message = "correct"
                    message_start_time = time.time()
                    admin_pw_buffer = ""

                    time.sleep(1)
                    cv2.destroyWindow("Admin Login")
                    return "OK"
                else:
                    result_message = "wrong"
                    message_start_time = time.time()
                    admin_pw_buffer = ""

            else:
                admin_pw_buffer += key

        if cv2.waitKey(10) & 0xFF == ord('q'):
            cv2.destroyWindow("Admin Login")
            return "BACK"

if __name__ == "__main__":
    admin_login_screen()
