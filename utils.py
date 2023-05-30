import matplotlib.pyplot as plt
from scipy.signal import butter,lfilter
import numpy as np
import scipy.stats as stats
from dtw import dtw,accelerated_dtw
import math
import pandas as pd

dict_match = {'LLx': 'LowerLip_x', 'LLy': 'LowerLip_y', 'LLz': 'LowerLip_z',
              'ULx': 'UpperLip_x', 'ULy': 'UpperLip_y', 'ULz': 'UpperLip_z',
              'LeLx': 'LeftLip_x', 'LeLy': 'LeftLip_y', 'LeLz': 'LeftLip_z',
              'RLx': 'RightLip_x', 'RLy': 'RightLip_y', 'RLz': 'RightLip_z',
              'JLx': 'JawLeft_x', 'JLy': 'JawLeft_y', 'JLz': 'JawLeft_z',
              'JRx': 'JawRight_x', 'JRy': 'JawRight_y', 'JRz': 'JawRight_z',
              }

def crosscorr(datax, datay, lag=0, wrap=False):
    """ Lag-N cross correlation.
    Shifted data filled with NaNs

    Parameters
    ----------
    lag : int, default 0
    datax, datay : pandas.Series objects of equal length
    Returns
    ----------
    crosscorr : float
    """
    if wrap:
        shiftedy = datay.shift(lag)
        shiftedy.iloc[:lag] = datay.iloc[-lag:].values
        return datax.corr(shiftedy)
    else:
        return datax.corr(datay.shift(lag))

def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a
def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y

def optimal_lowpass(facemeshdata, cortexdata, method='RMSE'):
    best_measure = np.inf
    best_cutoff = 0
    for i in range(0,100):
        test_data = butter_lowpass_filter(facemeshdata, 4.5+i*0.1, 30, order=5)
        length = min(len(cortexdata),len(facemeshdata))
        if method == 'Pearson':
            measure = -stats.pearsonr(test_data[1:length], cortexdata[1:length])[0] # possible nans in the first element
        elif method == 'RMSE':
            MSE = np.square(np.subtract(test_data[1:length], cortexdata[1:length])).mean()
            measure = math.sqrt(MSE)
        if measure < best_measure:
            best_cutoff = 4.5+i*0.1
            best_measure = measure
    print("best cutoff = ", best_cutoff, "Hz")
    return butter_lowpass_filter(facemeshdata, best_cutoff, 30, order=5)

# Coherence
def Cohere(data1, data2, fps=30):
    plt.figure()
    plt.cohere(data1, data2,Fs=fps)
    plt.title("Coherence of FaceMesh with infrared cameras")
    plt.show()

# Dynamic Time Warping
def DTW(data1, data2):
    d, cost_matrix, acc_cost_matrix, path = accelerated_dtw(np.array(data1[200:len(data2)]), np.array(data2[200:]), dist='euclidean')
    plt.imshow(acc_cost_matrix.T, origin='lower', cmap='gray', interpolation='nearest')
    plt.plot(path[0], path[1], 'w')
    plt.xlabel('stickers')
    plt.ylabel('FaceMesh')
    plt.title(f'DTW Minimum Path with minimum distance: {np.round(d,2)}')
    plt.show()

def find_most_common_element(lst):
    counts = {}
    for item in lst:
        if item in counts:
            counts[item] += 1
        else:
            counts[item] = 1

    most_common_element = None
    max_count = 0
    for item, count in counts.items():
        if count > max_count:
            most_common_element = item
            max_count = count

    return most_common_element
def leader_offset(data_facemesh,data_cortex):
    offsets = []
    llx, lly, llz = [], [], []
    ulx, uly, ulz = [], [], []
    lelx, lely, lelz = [], [], []
    rlx, rly, rlz = [], [], []
    jlx, jly, jlz = [], [], []
    jrx, jry, jrz = [], [], []
    save_dict = {'LLx': llx, 'LLy': lly, 'LLz': llz,
            'ULx': ulx, 'ULy': uly, 'ULz': ulz,
            'LeLx': lelx, 'LeLy': lely, 'LeLz': lelz,
            'RLx': rlx, 'RLy': rly, 'RLz': rlz,
            'JLx': jlx, 'JLy': jly, 'JLz': jlz,
            'JRx': jrx, 'JRy': jry, 'JRz': jrz,
            }
    for landmark in dict_match.keys():
        # create list
        for i in range(len(data_facemesh[landmark])):
            save_dict[landmark].append(-data_facemesh[landmark][i])
        # cortex value
        landmark_cortex = dict_match[landmark]
        data_cortex_list = []
        for i in range(len(data_cortex[landmark_cortex])):
            if i % 2 == 0:
                data_cortex_list.append(data_cortex[landmark_cortex][i])
        # rescale
        _, offset_local = rescale(data_cortex_list, save_dict[landmark])
        offsets.append(offset_local)
    return find_most_common_element(offsets)

def rescale(target_data, unscaled_data, is_offset=True, leader_offset=False, set_offset=0):
    # automatic rescaling
    # width: no need since same frames
    # vertical: match means and std
    unscaled_data = np.array(unscaled_data)
    target_data = np.array(target_data)
    arr_mean = np.nanmean(unscaled_data)
    arr_std = np.nanstd(unscaled_data)
    ref_mean = np.nanmean(target_data)
    ref_std = np.nanstd(target_data)
    unscaled_data = (unscaled_data - arr_mean) * ref_std / arr_std + ref_mean
    unscaled_data = unscaled_data.tolist()

    # horizontal
    # trickier: use Time Lagged Cross Correlation
    # first, find the offset
    length = min(len(target_data), len(unscaled_data))
    d1 = pd.Series(target_data[:length])
    d2 = pd.Series(unscaled_data[:length])
    seconds = 5
    fps = 30
    rs = [crosscorr(d1, d2, lag) for lag in range(-int(seconds * fps), int(seconds * fps + 1))]
    offset = int(np.floor(len(rs) / 2) - np.argmax(rs))
    print("offset = ", offset, " frames")
    if leader_offset:
        offset = set_offset
    if not is_offset:
        offset = 0
    # then, offset accordingly
    if offset > 0:
        unscaled_data = unscaled_data[offset:]
    else:
        for i in range(abs(offset)):
            unscaled_data.insert(0, np.mean(unscaled_data))
    scaled_data = unscaled_data
    return scaled_data, offset

def RMSE(facemeshdata, cortexdata):
    MSE = np.square(np.subtract(facemeshdata[1:], cortexdata[1:len(facemeshdata)])).mean()
    RMSE = math.sqrt(MSE)
    print("Root Mean Square Error: ", RMSE)
    r_window_size = 100
    rolling_RMSE = []
    for i in range(len(facemeshdata[1:]) - r_window_size):
        rolling_RMSE.append(math.sqrt(np.square(np.subtract(facemeshdata[1+i:1+i+r_window_size], cortexdata[1+i:1+i+r_window_size])).mean()))
    my_mean = np.min(facemeshdata[1:]) - 5
    plt.figure()
    plt.plot([rolling_RMSE[i]/abs(facemeshdata[1 + i] - my_mean) for i in range(len(rolling_RMSE))], label="percentage")
    plt.xlabel('frames')
    plt.ylabel('RMSE in %')
    plt.title("% of RMSE of FaceMesh vs stickers")
    plt.show()

def Pearson(facemeshdata, cortexdata):
    overall_pearson_r = stats.pearsonr(cortexdata[:len(facemeshdata)],facemeshdata)
    r_window_size = 100
    rolling_pearson = []
    for i in range(len(facemeshdata[1:]) - r_window_size):
        rolling_pearson.append(stats.pearsonr(cortexdata[1+i:1+i+r_window_size],facemeshdata[1+i:1+i+r_window_size])[0])
    print("overall Pearson correlation: ", overall_pearson_r[0])

    plt.figure()
    plt.plot([overall_pearson_r[0]]*len(cortexdata[1:]), label='overall pearson')
    plt.plot(rolling_pearson, label='rolling pearson')
    plt.xlabel('frames')
    plt.ylabel('correlation')
    plt.title("Pearson correlation of FaceMesh vs stickers")
    plt.show()