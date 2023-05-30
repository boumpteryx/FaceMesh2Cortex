import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from one_euro_filter import OneEuroFilter
import math
import scipy.stats as stats
from utils import crosscorr, butter_lowpass_filter, optimal_lowpass, Cohere, DTW, rescale, RMSE, Pearson

fps = 60

# Cortex data
url_cortex = "Videos/Jaws/CSV/TMS10_Speech_BBP.csv"
data_cortex = pd.read_csv(url_cortex)
# FaceMesh data
url_FaceMesh = "tracking/Jaws/TMS10_Speech_BBP1-Decklink Video Capture.csv"
data_facemesh = pd.read_csv(url_FaceMesh)
video_name = "Jaws/TMS10_Speech_BBP1-Decklink Video Capture"

"""llx, lly, llz = [], [], []
ulx, uly, ulz = [], [], []
lelx, lely, lelz = [], [], []
rlx, rly, rlz = [], [], []
jlx, jly, jlz = [], [], []
jrx, jry, jrz = [], [], []
bex, bey, bez = [], [], []
dict = {'LLx': llx, 'LLy': lly, 'LLz': llz,
              'ULx': ulx, 'ULy': uly, 'ULz': ulz,
              'LeLx': lelx, 'LeLy': lely, 'LeLz': lelz,
              'RLx': rlx, 'RLy': rly, 'RLz': rlz,
              'JLx': jlx, 'JLy': jly, 'JLz': jlz,
              'JRx': jrx, 'JRy': jry, 'JRz': jrz,
              }
dict_match = {'LLx': 'LowerLip_x', 'LLy': 'LowerLip_y', 'LLz': 'LowerLip_z',
              'ULx': 'UpperLip_x', 'ULy': 'UpperLip_y', 'ULz': 'UpperLip_z',
              'LeLx': 'LeftLip_x', 'LeLy': 'LeftLip_y', 'LeLz': 'LeftLip_z',
              'RLx': 'RightLip_x', 'RLy': 'RightLip_y', 'RLz': 'RightLip_z',
              'JLx': 'JawLeft_x', 'JLy': 'JawLeft_y', 'JLz': 'JawLeft_z',
              'JRx': 'JawRight_x', 'JRy': 'JawRight_y', 'JRz': 'JawRight_z',
              }"""
"""for landmark in dict.keys():
    print(landmark)
    # create list
    for i in range(len(data_facemesh[landmark])):
        dict[landmark].append(-data_facemesh[landmark][i])
    # cortex value
    landmark_cortex = dict_match[landmark]
    data_cortex_list = []
    for i in range(len(data_cortex[landmark_cortex])):
        if i % 2 == 0:
            data_cortex_list.append(data_cortex[landmark_cortex][i])
    # rescale
    dict[landmark] = rescale(data_cortex_list, dict[landmark])
    # filter
    dict[landmark] = butter_lowpass_filter(dict[landmark], 12, fps, order=5)

# save
df = pd.DataFrame(dict)
df.to_csv("tracking/overall/" + video_name + ".csv")"""

llx, lly, llz = [], [], []
ulx, uly, ulz = [], [], []
lelx, lely, lelz = [], [], []
rlx, rly, rlz = [], [], []
jlx, jly, jlz = [], [], []
jrx, jry, jrz = [], [], []
bex, bey, bez = [], [], []
jcx, jcy, jcz = [], [], []
jlcx, jlcy, jlcz = [], [], []
jrcx, jrcy, jrcz = [], [], []
jlclx, jlcly, jlclz = [], [], []
jrcrx, jrcry, jrcrz = [], [], []
jlux, jluy, jluz = [], [], []
jrux, jruy, jruz = [], [], []
dict = {
              'JLx': jlx, 'JLy': jly, 'JLz': jlz,
              'JRx': jrx, 'JRy': jry, 'JRz': jrz,
              'JCx': jcx, 'JCy': jcy, 'JCz': jcz,
              'JLCx': jlcx, 'JLCy': jlcy, 'JLCz': jlcz,
              'JRCx': jrcx, 'JRCy': jrcy, 'JRCz': jrcz,
              'JLCLx': jlclx, 'JLCLy': jlcly, 'JLCLz': jlclz,
              'JRCRx': jrcrx, 'JRCRy': jrcry, 'JRCRz': jrcrz,
              'JLUx': jlux, 'JLUy': jluy, 'JLUz': jluz,
              'JRUx': jrux, 'JRUy': jruy, 'JRUz': jruz,
              }
dict_match = {
              'JLx': 'iJLx', 'JLy': 'iJLy', 'JLz': 'iJLz',
              'JRx': 'iJRx', 'JRy': 'iJRy', 'JRz': 'iJRz',
              'JCx': 'iJCx', 'JCy': 'iJCy', 'JCz': 'iJCz',
              'JLCx': 'iJLx', 'JLCy': 'iJLy', 'JLCz': 'iJLz',
              'JRCx': 'iJRx', 'JRCy': 'iJRy', 'JRCz': 'iJRz',
              'JLCLx': 'iJLx', 'JLCLy': 'iJLy', 'JLCLz': 'iJLz',
              'JRCRx': 'iJRx', 'JRCRy': 'iJRy', 'JRCRz': 'iJRz',
              'JLUx': 'iJLx', 'JLUy': 'iJLy', 'JLUz': 'iJLz',
              'JRUx': 'iJRx', 'JRUy': 'iJRy', 'JRUz': 'iJRz',
              }

for landmark in dict.keys():
    print(landmark)
    # create list
    for i in range(len(data_facemesh[landmark])):
        dict[landmark].append(-data_facemesh[landmark][i])
    # cortex value
    landmark_cortex = dict_match[landmark]
    data_cortex_list = []
    for i in range(len(data_cortex[landmark_cortex])):
        if i % 2 == 0:
            data_cortex_list.append(data_cortex[landmark_cortex][i])
    # rescale
    dict[landmark] = rescale(data_cortex_list, dict[landmark])
    # filter
    dict[landmark] = butter_lowpass_filter(dict[landmark], 12, fps, order=5)

# save
df = pd.DataFrame(dict)
df.to_csv("tracking/overall/" + video_name + ".csv")

# point and dimension to study
landmark = "JCx"
landmark_cortex = "iJCx"

"""right_eye = []
for i in range(len(data_facemesh['RREx'])):
    right_eye.append(np.sqrt((data_facemesh['RREx'][i] - data_facemesh['LREx'][i])**2 + (data_facemesh['RREy'][i] - data_facemesh['LREy'][i])**2 + (data_facemesh['RREz'][i] - data_facemesh['LREz'][i])**2))
plt.plot(right_eye)"""

# get one out of x frames to match fps
data_facemesh_list = []
for i in range(len(data_facemesh[landmark])):
    data_facemesh_list.append(-data_facemesh[landmark][i])

data_cortex_list = []
for i in range(len(data_cortex[landmark_cortex])):
    if i % 2 == 0:
        data_cortex_list.append(data_cortex[landmark_cortex][i])

# rescale
data_facemesh_list = rescale(data_cortex_list, data_facemesh_list)

# low-pass filter
data_facemesh_list_butter = butter_lowpass_filter(data_facemesh_list, 12, fps, order=5)

def signal_plot():
    plt.figure(figsize=(17, 5))
    plt.plot(data_cortex_list[15:], label="Cortex")
    plt.plot(data_facemesh_list_butter[15:], label="FaceMesh")
    plt.xlabel('frames')
    plt.ylabel(landmark)
    plt.legend()
    plt.show()

# RMSE()

# Pearson()

# print("correlation: ", np.correlate(data_cortex_list, data_facemesh_list_butter, mode='full'))

# Cohere(data_facemesh_list_butter, data_cortex_list)

signal_plot()

# DTW(data_cortex_list, data_facemesh_list_butter)
