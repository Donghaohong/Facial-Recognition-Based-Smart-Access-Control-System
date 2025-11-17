import cv2
import numpy as np
from password_enter import password_screen

clicked_button = None

buttons = {
    "password": (100, 120, 700, 200),
    "face":     (100, 230, 700, 310),
    "admin":    (100, 340, 700, 420),
}

def draw_menu():
    img = np.zeros((480, 800, 3), dtype=np.uint8)

    cv2.putText(img, "SMART DOOR LOCK", (200, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0,255,255), 3)

    cv2.rectangle(img, (100,120), (700,200), (255,255,255), 3)
    cv2.putText(img, "Password Unlock", (180, 175),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)

    cv2.rectangle(img, (100,230), (700,310), (255,255,255), 3)
    cv2.putText(img, "Face Recognition", (180, 285),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)

    cv2.rectangle(img, (100,340), (700,420), (255,255,255), 3)
    cv2.putText(img, "Admin Login", (180, 395),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)

    return img

def mouse_callback(event, x, y, flags, param):
    global clicked_button
    if event == cv2.EVENT_LBUTTONDOWN:
        for name, (x1, y1, x2, y2) in buttons.items():
            if x1 <= x <= x2 and y1 <= y <= y2:
                clicked_button = name

def main():
    global clicked_button

    while True:
        clicked_button = None

        cv2.namedWindow("Menu", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Menu", 800, 480)
        cv2.setMouseCallback("Menu", mouse_callback)

        while True:
            img = draw_menu()
            cv2.imshow("Menu", img)

            if clicked_button:
                break

            if cv2.waitKey(10) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                return  # 完全退出程序

        cv2.destroyWindow("Menu")  # 先关闭菜单界面

        if clicked_button == "password":
            password_screen()

if __name__ == "__main__":
    main()


