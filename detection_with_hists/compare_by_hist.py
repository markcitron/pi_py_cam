#!/usr/bin/python3

import cv2
import logging
import logging.handlers as handlers
import histogram_utils

logname = "hist_deltas.log"
logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
logHandler = handlers.RotatingFileHandler(logname, maxBytes=10000000, backupCount=5)
logHandler.setLevel(logging.INFO)
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)

def main():
    cap = cv2.VideoCapture(2)
    Image_Histograms = histogram_utils.Histograms(30)

    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()

        # determine current delta for histgram and add to hists array
        current_hist = cv2.calcHist(frame, [0], None, [256], [0,256])
        Image_Histograms.add_to_hists(current_hist)

        # determine offset from average hists in last (up to) 50 hists
        delta = Image_Histograms.compare_hists(current_hist)
        logger.info("Delta: {0}".format(delta))
        if delta < 0.8:
            logger.warn("Something changed!!!")

        # end if ready
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
