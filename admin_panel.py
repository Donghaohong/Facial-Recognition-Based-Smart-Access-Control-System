import cv2
import numpy as np

clicked_button = None

buttons = {
    "change_pw":   (100,  96, 700, 160),
    "add_face":    (100, 184, 700, 248),
    "delete_face": (100, 272, 700, 336),
    "back":        (100, 360, 700, 424),
}

def draw_admin_panel():
    img = np.zeros((480,800,3), dtype=np.uint8)

    cv2.putText(img, "ADMIN PANEL", (250, 56),
                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,255,255), 3)

    # Change PW
    cv2.rectangle(img, (100, 96), (700, 160), (255,255,255), 3)
    cv2.putText(img, "Change Password", (180, 140),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)

    # Add face
    cv2.rectangle(img, (100, 184), (700, 248), (255,255,255), 3)
    cv2.putText(img, "Add New Face", (230, 228),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)

    # Delete face
    cv2.rectangle(img, (100, 272), (700, 336), (255,255,255), 3)
    cv2.putText(img, "Delete Face Data", (200, 316),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)

    # Back
    cv2.rectangle(img, (100, 360), (700, 424), (255,255,255), 3)
    cv2.putText(img, "BACK", (350, 404),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)

    return img

def mouse_callback(event, x, y, flags, param):
    global clicked_button

    if event == cv2.EVENT_LBUTTONDOWN:
        for name, (x1,y1,x2,y2) in buttons.items():
            if x1 <= x <= x2 and y1 <= y <= y2:
                clicked_button = name


def admin_panel_screen():
    global clicked_button
    clicked_button = None

    cv2.namedWindow("Admin Panel", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Admin Panel", 800, 480)
    cv2.setMouseCallback("Admin Panel", mouse_callback)

    while True:
        img = draw_admin_panel()
        cv2.imshow("Admin Panel", img)

        if clicked_button:
            action = clicked_button
            clicked_button = None
            cv2.destroyWindow("Admin Panel")
            return action

        if cv2.waitKey(10) & 0xFF == ord('q'):
            cv2.destroyWindow("Admin Panel")
            return "back"

if __name__ == "__main__":
    result = admin_panel_screen()
    print("Admin panel action:", result)
