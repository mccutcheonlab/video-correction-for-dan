# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 13:25:47 2020

@author: admin
"""

## Need to ensure tdt and opencv are installed for this to function.

# pip install tdt
# conda install -c conda-forge opencv
# pip install opencv-contrib-python

# Import necessary functions
import numpy as np
import matplotlib.pyplot as plt
import tdt
import cv2 as cv

# Set folder for tank, location of .avi file, and output file

folder = 'C:\\Users\\jmc010\\Dropbox\\Shared and resource folders\\Dan Covey\\'
tank = folder+'SD6\\'
videofile = tank+'DAN_RR-190827-090229_SD6_Cam1.avi'
outputfile = 'output.avi'

# Read in epoc information from TDT tank
epocs = tdt.read_block(tank, evtype=['epocs']).epocs

ticks = epocs['Tick']['onset']
cam = epocs['Cam1']['onset']

print('There are {} ticks and {} camera timestamps/frames'.format(len(ticks), len(cam)))

# Calculate inter-tick and inter-framne intervals and plot.
# If frames are taken at irregular times then figure on left will show
# a distribution of inter-frame intervals rather than a 'spike'

itis = np.diff(ticks)
ifis = np.diff(cam)

f, ax = plt.subplots(ncols=2)
ax[0].hist(itis)
ax[1].hist(ifis, bins=100)

# Print some stats on interframe rate
print('The fastest instantaneous frame rate is {} Hz'.format(1/min(ifis)))
print('The slowest instantaneous frame rate is {} Hz'.format(1/max(ifis)))
print('The mean frame rate is {} Hz'.format(1/np.mean(ifis)))

# Calculate bounds for min and max frame in video
Fs_cam = 10
interval = 1/Fs_cam

minframe = round(min(cam), 1)
maxframe = round(max(cam), 1)

frames_out = np.arange(minframe, maxframe, interval)

# Make frame_index which determines while frames of original .avi to sample
# to make a video of appropriate length and frame rate

frame_index=[0]
for frame in frames_out:
    frame_index.append([i for i, f in enumerate(cam) if f > frame][0])

# Open original video file
cap = cv.VideoCapture(videofile)

# Define the codec and create VideoWriter object
fourcc = cv.VideoWriter_fourcc(*'XVID')
out = cv.VideoWriter('output.avi', fourcc, 10.0, (800,  600))

# Loop through frame_index, selecting appropriate frames from original video
# and writing to a new file
for frame in frame_index:
    cap.set(cv.CAP_PROP_POS_FRAMES, frame)
    ret, frame = cap.read()
    if ret:
        out.write(frame)

cap.release()
out.release()
cv.destroyAllWindows()

