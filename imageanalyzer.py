# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 14:01:51 2016

@author: Konrad

This script displays and analyses image(s) from the current sequence.
"""
from analyzer import Analyzer, save_plot

import numpy as np
import matplotlib.pyplot as plt

def analyze(figure, file):
    try:
        image_array = np.load(file.filename[:-4] + 'npy')
        ax = figure.add_subplot(111)
        ax.imshow(image_array)
        
        return 1,1
    except Exception as e:
        print(e)
        
def plot(fig, data):
    pass

a = Analyzer(analyze)
a.run()