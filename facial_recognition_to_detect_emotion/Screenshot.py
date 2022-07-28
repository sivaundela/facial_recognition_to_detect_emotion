import cv2

def screenshot():
    cam = cv2.VideoCapture(0)
    cv2.namedWindow("test")
    #img_counter = 0
    while True:
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            break
        cv2.imshow("test", frame)
        k = cv2.waitKey(1)
        if k%256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            break
        elif k%256 == 32:
            # SPACE pressed
            img_name = "test.jpg"
            cv2.imwrite(img_name, frame)
            print("Picture Captured!")

    cam.release()
    cv2.destroyAllWindows()
if __name__ == '__main__':
    screenshot()