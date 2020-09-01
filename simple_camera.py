#!/usr/bin/python3

import cv2

def main():
    cam = cv2.VideoCapture(0)
    cv2.namedWindow("Simple Camera")

    img_counter = 0

    while True:
        ret, frame = cam.read()
        if not ret:
            print("Failed to grab frame")
            break
        cv2.imshow("Simple Camera", frame)

            k = cv2.waitKey(1)
            if k%256 == 27:
                print("Escape hit, see you later.")
                break
            if k%256 == 32:
                img.name = "frame_capture_{}.png".format(img_counter)
                cv2.imwrite(img_name, frame)
                print("{} written".format(img_name))
                img_counter += 1
    
    cv2.detroyAllWindows()
    cam.release()

if __name__ == "__main__":
    main()