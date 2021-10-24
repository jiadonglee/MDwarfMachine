#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: Bo ZHANG (bozhang at bnu.edu.cn)
Please cite https://ui.adsabs.harvard.edu/abs/2021ApJS..256...14Z/abstract
"""

#%%%%  path to your spectra
import glob
fps = glob.glob("data/*.fits.gz")
print("number of spectra: ", len(fps))

#%%
print("load RVM ...")
import joblib
from laspec.wavelength import air2vac, vac2air
rvm = joblib.load("models/R1800_rvm_Ca8500.dump") # 3. the path of the rvm file
rvm.wave_mod = vac2air(rvm.wave_mod)


#%%
import numpy as np
from laspec.mrs import MrsSpec
from laspec.normalization import normalize_spectrum_spline
from astropy.io import fits


def measure_rv(rvm, fp):
    try:
        ms = MrsSpec.from_lrs(fp, norm_type=None)
        # cut spectrum  
        indcut = (ms.wave>8000)&(ms.wave<8950)
        wave_obs = ms.wave[indcut]
        flux_obs = ms.flux[indcut]
        flux_err = ms.flux_err[indcut]
        mask_obs = ms.mask[indcut]
        
        # normalize spectrum
        flux_norm, flux_cont = normalize_spectrum_spline(wave_obs, flux_obs, niter=3)
        flux_norm_err = flux_err / flux_cont
        # measure rv
        rvr = rvm.measure(wave_obs, flux_norm, flux_norm_err, nmc=100)
        print(rvr)
        rvr["snr50"] = np.median(flux_obs/flux_err)
        rvr["fp"] = fp
        rvr["obsid"] = fits.getheader(fp)["OBSID"]
        rvr["rvteff"] = rvr["pmod"][0]
        rvr["rv16"],rvr["rv50"],rvr["rv84"] = rvr["rv_pct"]
        rvr["rv_unc"] = (rvr["rv84"]-rvr["rv16"])/2
        rvr["npix_obs"] = len(flux_obs)
        rvr["npix_bad"] = np.sum(mask_obs>0)
        return rvr
    except Exception:
        return None

#%%
print("measure rv ...")
rvr_list = joblib.Parallel(n_jobs=-1, verbose=20)(joblib.delayed(measure_rv)(rvm, fp) for fp in fps)
rvr_list_valid = []
for i in range(len(rvr_list)):
    if rvr_list[i] is not None:
        rvr_list_valid.append(rvr_list[i])


from astropy.table import Table
trvr = Table(rvr_list_valid)
trvr.write("data/trvr.fits", overwrite=True) # 4. save to the file
