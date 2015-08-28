from color_histogram.datasets.google_image import dataFile

# -*- coding: utf-8 -*-
## @package color_histogram.results.hist_3d
#
#  color_histogram.results.hist_3d utility package.
#  @author      tody
#  @date        2015/08/28

import os
import numpy as np
import matplotlib.pyplot as plt

from color_histogram.io_util.image import loadRGB
from color_histogram.cv.image import rgb, to32F, rgb2Lab, rgb2hsv
from color_histogram.core.hist_3d import Hist3D
from color_histogram.results.results import resultFile
from color_histogram.plot.window import showMaximize


def plotHistogram3D(C_32F, color_space, ax):
    samples = np.array(C_32F)
    if color_space == "Lab":
        samples = rgb2Lab(samples)

    if color_space == "hsv":
        samples = rgb2hsv(samples)

    font_size = 15
    num_bins = 16
    plt.title("%s 3D histogram: %s bins" % (color_space, num_bins), fontsize=font_size)

    hist3D = Hist3D(samples, num_bins=num_bins, color_space=color_space)
    hist3D.plotColorSamples(ax)

def histogram3DResult(image_file):
    image_name = os.path.basename(image_file)
    image_name = os.path.splitext(image_name)[0]

    fig_w = 10
    fig_h = 6
    fig = plt.figure(figsize=(fig_w, fig_h))
    fig.subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.95, wspace=0.02, hspace=0.2)

    font_size = 15
    fig.suptitle("Hisotogram 3D", fontsize=font_size)

    C_8U = loadRGB(image_file)

    h, w = C_8U.shape[:2]
    fig.add_subplot(231)
    plt.title("Original Image: %s" % [w, h], fontsize=font_size)
    plt.imshow(C_8U)
    plt.axis('off')

    rgb_8U = rgb(C_8U)
    C_32F = to32F(rgb_8U)

    color_spaces = ["rgb", "Lab", "hsv"]

    plot_id = 234
    for color_space in color_spaces:
        ax = fig.add_subplot(plot_id, projection='3d')
        plotHistogram3D(C_32F, color_space, ax)
        plot_id += 1

    result_name = image_name + "_hist3D"
    result_file = resultFile(result_name)
    plt.savefig(result_file, transparent=True)

    #showMaximize()


## Performance tests for the data names, IDs.
def histogram3DResults(data_names, data_ids):
    for data_name in data_names:
        print "Performance tests: %s" % data_name
        for data_id in data_ids:
            print "Data ID: %s" % data_id
            image_file = dataFile(data_name, data_id)
            histogram3DResult(image_file)

if __name__ == '__main__':
    data_names = ["flower"]
    data_ids = [0, 1, 2]

    histogram3DResults(data_names, data_ids)