import cv2
import numpy as np
import os
import time

PASSWORD_FILE = "password.txt"
DEFAULT_PASSWORD = "2468"

pw_buffer = ""
pw_first = None
clicked = None
result_message = None
message_start_time = 0

buttons = {
    "1": (240,120,320,184),
    "2": (360,120,440,184),
    "3": (480,120,560,184),

    "4": (240,200,320,264),
    "5": (360,200,440,264),
    "6": (480,200,560,264),

    "7": (240,280,320,344),
    "8": (360,280,440,344),
    "9": (480,280,560,344),

    "C": (240,360,320,424),
    "0": (360,360,440,424),
    "OK":(480,360,560,424)
}

back_button = (16,16,120,56)

def ensure_password_file():
    if not os.path.exists(PASSWORD_FILE):
        with open(PASSWORD_FILE, "w") as f:
            f.write(DEFAULT_PASSWORD)

def save_new_password(pw):
    with open(PASSWORD_FILE, "w") as f:
        f.write(pw)

def draw_change_pw():
    img = np.zeros((480,800,3), dtype=np.uint8)

    (bx1,by1,bx2,by2) = back_button
    cv2.rectangle(img, (bx1,by1), (bx2,by2), (255,255,255), 2)
    cv2.putText(img, "BACK", (bx1+10, by1+35),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)

    cv2.putText(img, "CHANGE PASSWORD", (180, 48),
                cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0,255,255), 3)

    if pw_first is None:
        stage_text = "Enter New Password"
    else:
        stage_text = "Re-enter Password"

    cv2.putText(img, stage_text, (260, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,255), 2)

    display = "*" * len(pw_buffer)
    cv2.putText(img, display, (330, 112),
                cv2.FONT_HERSHEY_SIMPLEX, 1.6, (0,255,0), 3)

    if result_message is not None:
        text = result_message

        size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1.2, 3)[0]
        text_x = 260
        text_y = 104
        color = (0,255,0) if text == "Password Updated" else (0,0,255)

        cv2.putText(img, text, (text_x, text_y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 3)

    for t,(x1,y1,x2,y2) in buttons.items():
        cv2.rectangle(img, (x1,y1), (x2,y2), (255,255,255), 3)

        if t == "OK":
            tx = x1 + 10
            ty = y1 + 50
            scale = 1.6
        else:
            tx = x1 + 30
            ty = y1 + 50
            scale = 1.8

        cv2.putText(img, t, (tx, ty),
                    cv2.FONT_HERSHEY_SIMPLEX, scale, (255, 255, 255), 3)

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

def change_password_screen():
    global pw_buffer, pw_first, clicked, result_message, message_start_time

    ensure_password_file()
    pw_buffer = ""
    pw_first = None
    clicked = None
    result_message = None

    cv2.namedWindow("Change Password", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Change Password", 800, 480)
    cv2.setMouseCallback("Change Password", mouse_callback)

    while True:

        if result_message is not None:
            if time.time() - message_start_time > 1.2:
                if result_message == "Password Updated":
                    cv2.destroyWindow("Change Password")
                    return "OK"
                result_message = None

        img = draw_change_pw()
        cv2.imshow("Change Password", img)

        if clicked:
            key = clicked
            clicked = None

            if key == "BACK":
                cv2.destroyWindow("Change Password")
                return "BACK"

            elif key == "C":
                pw_buffer = ""

            elif key == "OK":
                if pw_first is None:
                    pw_first = pw_buffer
                    pw_buffer = ""
                else:
                    if pw_buffer == pw_first:
                        save_new_password(pw_buffer)
                        result_message = "Password Updated"
                        message_start_time = time.time()
                    else:
                        result_message = "Mismatch, Try Again"
                        message_start_time = time.time()
                    pw_buffer = ""
                    pw_first = None

            else:
                pw_buffer += key

        if cv2.waitKey(10) & 0xFF == ord('q'):
            cv2.destroyWindow("Change Password")
            return "BACK"


if __name__ == "__main__":
    change_password_screen()
