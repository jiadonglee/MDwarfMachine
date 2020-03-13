#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import numpy as np
from astropy.io import fits
from scipy.interpolate import interp1d

def readFits(filename):
    """
    read Lamost DR5 fits
    """
    hdulist = fits.open(filename)
    head = hdulist[0].header
    scidata = hdulist[0].data
    # obsid = head['OBSID']
    flux = scidata[0,]
    invar = scidata[1,]

    wavelength = scidata[2,]
    hdulist.close()

    return (wavelength, flux, invar)

def resample(wave, flux, err, wave_resamp):

    f1 = interp1d(wave, flux, kind='cubic')
    f2 = interp1d(wave, err)
    re_flux = f1(wave_resamp)
    re_err = f2(wave_resamp)
        
    return np.array(re_flux), np.array(re_err)

class LAMOST():

    def __init__(self, root_dir, wave_resamp):
        self.root_dir = root_dir
        self.wave_resamp = wave_resamp
        self.spec_names = os.listdir(root_dir)
        # remove hidden file of MacOS
        self.spec_names = [f for f in os.listdir(root_dir) if not f.startswith('.')]
        self.spec_names.sort()
        
    def __len__(self):
        length = len(self.spec_names)
        return length

    def __getitem__(self, idx):
        spec_name = os.path.join(self.root_dir, self.spec_names[idx])
        self.wave, self.flux, self.invar = readFits(spec_name)
        self.re_flux, self.re_invar = resample(self.wave, self.flux, self.invar, self.wave_resamp)

        return {'wave':self.wave, 'flux':self.flux, 'invar':self.invar, \
                'flux_resamp':self.re_flux, 'invar_resamp':self.re_invar}

if __name__ == "__main__":
    pass