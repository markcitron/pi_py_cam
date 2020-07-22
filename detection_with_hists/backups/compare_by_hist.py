#!/usr/bin/python3

import numpy as np
import cv2
import logging
import logging.handlers as handlers

logname = "hist_deltas.log"
logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
logHandler = handlers.RotatingFileHandler(logname, maxBytes=10000000, backupCount=5)
logHandler.setLevel(logging.INFO)
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)

hists = []

def get_weights(size):
    weights = []
    for r in range(size):
        weights.append(int(r/10)+1)
    return weights


def compare_hists(current_hist):
    hist_deltas = []
    for each_hist in hists:
        hist_deltas.append(abs(cv2.compareHist(current_hist, each_hist, cv2.HISTCMP_CORREL)))
    hd = np.array(hist_deltas)
    calc_weights = get_weights(len(hists))
    # return np.average(hd)
    return np.average(hd, weights = calc_weights)

def add_to_hists(new_hist):
    if len(hists) > 300:
        hists.pop(0)
    hists.append(new_hist)
    return True

def main():
    cap = cv2.VideoCapture(2)

    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Display the resulting frame
        # cv2.imshow('frame',frame)

        # determine current delta for histgram and add to hists array
        current_hist = cv2.calcHist(frame, [0], None, [256], [0,256])
        add_to_hists(current_hist)

        # determine offset from average hists in last (up to) 50 hists
        delta = compare_hists(current_hist)
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
