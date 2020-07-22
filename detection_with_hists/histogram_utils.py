#!/usr/bin/python3

import numpy as np
import cv2

class Histograms():
    def __init__(self, max_hists):
        self.hists = []
        self.max_hists = max_hists

    def get_weights(self):
        """ build weights array based on total length of histogram array and weight the
            newest ones heavier """
        current_hists_length = len(self.hists)
        weights = []
        if current_hists_length > 0:
            for r in range(current_hists_length):
                weights.append(int(r/10)+1)
        return weights

    def compare_hists(self, current_hist):
        """ Compare current histogram against previous historgrams by determining the delta
            between the current on and all of the others and then using np to determine a 
            weighted average."""
        hist_deltas = []
        for each_hist in self.hists:
            hist_deltas.append(abs(cv2.compareHist(current_hist, each_hist, cv2.HISTCMP_CORREL)))
        hd = np.array(hist_deltas)
        calc_weights = self.get_weights()
        return np.average(hd, weights = calc_weights)

    def add_to_hists(self, new_hist): 
        if len(self.hists) > self.max_hists: 
            self.hists.pop(0)
        self.hists.append(new_hist)
        return True
