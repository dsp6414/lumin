import numpy as np
import pandas as pd
from typing import Tuple
from fastprogress import progress_bar


def calc_ams(s:float, b:float, br:float=0, unc_b:float=0) -> float:
    if b == 0: return -1
    if not unc_b:
        radicand = 2*((s+b+br)*np.log(1.0+s/(b+br))-s)
    else:
        sigma_b_2 = np.square(unc_b*b)
        radicand = 2*(((s+b)*np.log((s+b)*(b+sigma_b_2)/((b**2)+((s+b)*sigma_b_2))))-(((b**2)/sigma_b_2)*np.log(1+((sigma_b_2*s)/(b*(b+sigma_b_2))))))
    return np.sqrt(radicand) if radicand > 0 else -1


def ams_scan_quick(in_data:pd.DataFrame, w_factor:float=1, br:float=0, syst_unc_b:float=0,
                   pred_name:str='pred', targ_name:str='gen_target', weight_name:str='gen_weight') -> Tuple[float,float]:
    '''Determine optimum calc_ams and cut,
    w_factor used rescale weights to get comparable calc_amss
    sufferes from float precison - not recommended for final evaluation'''
    max_ams = 0
    threshold = 0.0
    in_data = in_data.sort_values(by=[pred_name])
    s = np.sum(in_data.loc[(in_data[targ_name] == 1), weight_name])
    b = np.sum(in_data.loc[(in_data[targ_name] == 0), weight_name])

    for i, cut in enumerate(in_data[pred_name]):
        ams = calc_ams(max(0, s*w_factor), max(0, b*w_factor), br, syst_unc_b)
        if ams > max_ams:
            max_ams = ams
            threshold = cut
        if in_data[targ_name].values[i]: s -= in_data[weight_name].values[i]
        else:                            b -= in_data[weight_name].values[i]        
    return max_ams, threshold


def ams_scan_slow(in_data:pd.DataFrame, w_factor:float=1, br:float=0, syst_unc_b:float=0, 
                  use_stat_unc:bool=False, start_cut:float=0.9, min_events:int=10,
                  pred_name:str='pred', targ_name:str='gen_target', weight_name:str='gen_weight', show_prog:bool=True) -> Tuple[float,float]:
    '''Determine optimum calc_ams and cut,
    w_factor used rescale weights to get comparable calc_amss
    slower than ams_scan_quick, but doesn't suffer from float precision'''
    max_ams = 0
    threshold = 0.0
    signal = in_data[in_data[targ_name] == 1]
    bkg    = in_data[in_data[targ_name] == 0]
    syst_unc_b2 = np.square(syst_unc_b)

    for i, cut in enumerate(progress_bar(in_data.loc[in_data[pred_name] >= start_cut, pred_name].values, display=show_prog, leave=show_prog)):
        bkg_pass = bkg.loc[(bkg[pred_name] >= cut), 'gen_weight']
        n_bkg = len(bkg_pass)
        if n_bkg < min_events: continue

        s = np.sum(signal.loc[(signal[pred_name] >= cut), 'gen_weight'])
        b = np.sum(bkg_pass)
        if use_stat_unc: unc_b = np.sqrt(syst_unc_b2+(1/n_bkg))
        else:            unc_b = syst_unc_b

        ams = calc_ams(s*w_factor, b*w_factor, br, unc_b)
        if ams > max_ams:
            max_ams = ams
            threshold = cut      
    return max_ams, threshold


