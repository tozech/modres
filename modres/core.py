#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 27 19:46:24 2018

@author: tzech
"""
from collections import OrderedDict

import pandas as pd



def upsample_det_model(data, det_model):
    """resample data according to deterministic model

    Parameters
    ----------
    data : pandas.Series
        time series with regular input freq
    det_model : pandas.Series
        time series of deterministic model in regular target freq

    Returns
    -------
    pandas.DataFrame
        'upsampled'
        time series of data upsampled to target freq according to deterministic model
        'corr_factor'
        time series of correction factors in target freq

    Conventions
    -----------
    time stamps label the end of the period to which the value belongs
    closed='right'
    label='right'

    'corr_factor'
    det_model / downsample(det_model, 'input_freq').mean()
    """
    name = data.name

    def _assert_freqs():
        target_freq = pd.Timedelta(det_model.index.freq)
        input_freq = pd.Timedelta(data.index.freq)
        zero_delta = pd.Timedelta(0)
        msg = 'target_freq {0} must be a divider of input_freq {1}'.format(target_freq, input_freq)
        assert input_freq % target_freq == zero_delta, msg
        freq_quoi = int(input_freq / target_freq)
        len_det_mod = len(det_model)
        len_data = len(data)
        msg = ('len of data ({0}) / len det_model ({1}) must be equal to '
               'target_freq ({2})/ input_freq ({3})').format(len_data,
                                                             len_det_mod,
                                                             target_freq,
                                                             input_freq)
        assert len_det_mod == freq_quoi * len_data, msg
        return input_freq, target_freq, freq_quoi

    input_freq, target_freq, freq_quoi = _assert_freqs()

    def _duplicate_target_times(x):
        d_target_freq = x.resample(target_freq)
        d_target_freq = d_target_freq.fillna(method='bfill', limit=freq_quoi)
        return d_target_freq
    # duplicate values which apply for the entire period
    data_target_freq = _duplicate_target_times(data)
    # Downsample deterministic modell to target freq and duplicate values
    det_model_input_freq = det_model.resample(input_freq, closed='right', label='right')
    det_model_input_freq = _duplicate_target_times(det_model_input_freq)
    # Correction factors for upsampling according to model
    corr_factors = det_model / det_model_input_freq
    # Apply factors to input data
    upsampled = corr_factors * data_target_freq
    return pd.DataFrame(OrderedDict([(name, upsampled),
                                     ('corr_factor', corr_factors)]))