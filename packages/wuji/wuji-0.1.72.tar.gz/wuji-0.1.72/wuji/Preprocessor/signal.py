#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   signal 
@Time        :   2023/11/21 14:06
@Author      :   Xuesong Chen
@Description :   
"""
import matplotlib.pyplot as plt
import numpy as np
from hrvanalysis import get_nn_intervals
import neurokit2 as nk
from scipy.signal import filtfilt


def interp_heartbeat(positions, values, fs, target_fs, n_samples):
    '''
    Interpolate RRI or JJI to target sampling frequency
    Parameters
    ----------
    positions: positions of RRI or JJI
    values: values of RRI or JJI
    fs: sampling frequency of RRI or JJI
    target_fs: target sampling frequency
    n_samples: number of samples of the raw signal

    Returns
    -------
    interp_value: interpolated RRI or JJI at target sampling frequency, in ms
    '''
    rri_in_ms = values / fs * 1000
    filtered_rri_in_ms = get_nn_intervals(rri_in_ms, verbose=False, ectopic_beats_removal_method='karlsson')
    interp_value = np.interp(
        np.arange(0, n_samples, fs / target_fs), positions,
        filtered_rri_in_ms).astype(np.float32)
    return interp_value


def filter_spo2(spo2, fs, min_allowed_spo2=50, max_allowed_spo2=105):
    if fs != 1:
        signal = nk.signal_resample(signal, sampling_rate=sfreq, desired_sampling_rate=1)
    plt.plot(spo2, label='raw')
    # 如果下降速率大于5，或者上升速率大于10，则认为是异常值
    max_drop_rate = -5
    max_recover_rate = 10
    mask = np.logical_or(np.diff(spo2) < max_drop_rate, np.diff(spo2) > max_recover_rate)
    spo2[1:][mask] = np.nan
    mask = np.logical_or(spo2 < min_allowed_spo2, spo2 > max_allowed_spo2)
    spo2[mask] = np.nan
    return spo2
