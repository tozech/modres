#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 27 19:47:24 2018

@author: tzech
"""
import pytest

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


import modres.core

@pytest.mark.filterwarnings("ignore::FutureWarning")
def test_upsample_det_model():
    # Input data inspired by solar_irradiance = clear_sky * cloud_coverage
    # However, clear_sky is simplified to be a sin-function and cloud_coverage
    # assumed to be uniformly distributed.
    times = pd.date_range('2063-04-04 06:15', '2063-04-04 18:00', freq='15min')
    num_el = len(times)
    sin = [np.sin(x) for x in np.linspace(0, np.pi, num_el)]
    np.random.seed(42)
    noise_strong = np.random.rand(int(num_el / 2))
    noise_weak = 1 - 0.1*np.random.rand(int(num_el / 2))
    noise = np.concatenate((noise_strong, noise_weak))
    data_15min = pd.DataFrame({'sin': sin, 'noise': noise}, index=times)
    data_15min['noisy_sin'] = data_15min['sin'] * data_15min['noise']
    data_15min['noisy_sin'].plot()

    #Upsample to 1min
    times_1min = pd.date_range('2063-04-04 06:01', '2063-04-04 18:00', freq='1min')
    sin_1min = [np.sin(x) for x in np.linspace(0, np.pi, len(times_1min))]
    sin_1min = pd.Series(sin_1min, index=times_1min)
    upsampled_1min = modres.core.upsample_det_model(data_15min['noisy_sin'],
                                                    sin_1min)
    ts_1min = upsampled_1min['noisy_sin']
    corr_fac_1min = upsampled_1min['corr_factor']

    ts_1min.plot()
    plt.legend(['15min', '1min'], loc='upper left')
    corr_fac_1min.plot(secondary_y=True)
    plt.legend(['corr_factor'], loc='upper right')
    # Test succesful upsampling
    assert ts_1min.index.freq == pd.tseries.offsets.Minute()
    ts_downsampled_15min = ts_1min.resample('15min', closed='right', label='right').mean()
    # Test consistency to input data when downsampling
    pd.testing.assert_series_equal(ts_downsampled_15min, data_15min['noisy_sin'])


if __name__ == '__main__':
    # Input data inspired by solar_irradiance = clear_sky * cloud_coverage
    # However, clear_sky is simplified to be a sin-function and cloud_coverage
    # assumed to be uniformly distributed.
    times = pd.date_range('2063-04-04 06:15', '2063-04-04 18:00', freq='15min')
    num_el = len(times)
    sin = [np.sin(x) for x in np.linspace(0, np.pi, num_el)]
    np.random.seed(42)
    noise_strong = np.random.rand(int(num_el / 2))
    noise_weak = 1 - 0.1*np.random.rand(int(num_el / 2))
    noise = np.concatenate((noise_strong, noise_weak))
    data_15min = pd.DataFrame({'sin': sin, 'noise': noise}, index=times)
    data_15min['noisy_sin'] = data_15min['sin'] * data_15min['noise']
    data_15min['noisy_sin'].plot()

    #Upsample to 1min
    times_1min = pd.date_range('2063-04-04 06:01', '2063-04-04 18:00', freq='1min')
    sin_1min = [np.sin(x) for x in np.linspace(0, np.pi, len(times_1min))]
    sin_1min = pd.Series(sin_1min, index=times_1min)
    upsampled_1min = modres.core.upsample_det_model(data_15min['noisy_sin'],
                                                    sin_1min)
    ts_1min = upsampled_1min['noisy_sin']
    corr_fac_1min = upsampled_1min['corr_factor']

    ts_1min.plot()
    plt.legend(['15min', '1min'], loc='upper left')
    corr_fac_1min.plot(secondary_y=True)
    plt.legend(['corr_factor'], loc='upper right')
    # Test succesful upsampling
    assert ts_1min.index.freq == pd.tseries.offsets.Minute()
    ts_downsampled_15min = ts_1min.resample('15min', closed='right', label='right').mean()
    # Test consistency to input data when downsampling
    pd.testing.assert_series_equal(ts_downsampled_15min, data_15min['noisy_sin'])








    data_1h = data_15min.resample('1h', closed='right', label='right').mean()

    #%%
    fig, ax = plt.subplots()
    sin_1min.plot(ax=ax)
    sin_1min_smooth = pd.rolling_window(sin_1min, window=20,
                                        win_type='cosine',
                                        center=True, min_periods=1)
    sin_1min_smooth.plot(ax=ax, linestyle='--')
    a = sin_1min.iloc[60:-61]
    b = sin_1min_smooth.iloc[60:-61]
    r = b - a
    ar = r / a
    rmse = np.sqrt(np.mean(r**2))
    rel_rmse = rmse / a.mean()
    rel_bias = r.mean() / a.mean()
    rel_mae = r.abs().mean() / a.mean()
    print("BIAS:{0:%} RMSE: {1:%} MAE: {2:%}".format(rel_bias,
                                                     rel_rmse,
                                                     rel_mae))
    #pd.testing.assert_series_equal(a, b)
