#!/usr/bin/python
# -*- coding: UTF-8 -*-
import numpy as np
import pandas as pd
from scipy import stats, interpolate
from scipy.optimize import curve_fit
from tqdm import tqdm
import pymc3 as pm
import theano.tensor as tt


def get_mcmc_stats(X, num_error=1):
    
    x = np.median(X)
    x_err_left = np.percentile(X, 84) - np.percentile(X, 50)
    x_err_right = np.percentile(X, 50) - np.percentile(X, 16)
    
    if num_error==1:
        x_err = np.max([x_err_left, x_err_right])
    elif num_error==2:
        x_err = (x_err_left, x_err_right)
        
    return x, x_err


def error_mc(arg, arg_err, N=10, model=None):
    """
    
    Parameters:
    -----------
    arg: list or array
        observed stellar parameters
        
    arg_err:list or array
        observed stellar parameters uncertainties
        
    N: int
        number of Monte Carlo
    
    model: Xgboost instance
        
    
    Return:
    -----------
    out: array
        estimated stellar parameter
    out_err: array
        estimated stellar parameter uncertianties
    """
    out, out_err =np.nan*np.ones(len(arg)), np.nan*np.ones(len(arg))
    if len(arg.shape) == 1:
        ndim = 1
        for i in tqdm(range(len(arg))):
            X_test = np.random.normal(
                arg[i], np.abs(arg_err[i]),size=N
            )
            y_pred_rand = model(X_test)
            out[i], out_err[i] = get_mcmc_stats(y_pred_rand)
            
    elif len(arg.shape)>=2:
        ndim = arg.shape[1]
        for i in tqdm(range(len(arg))):
            X_test = np.random.normal(
                arg[i,:], np.abs(arg_err[i,:]),size=(N, ndim)
            )
            y_pred_rand = model(X_test)
            out[i], out_err[i] = get_mcmc_stats(y_pred_rand)
    else:
        raise ValueError('input data dimension error!')
        
    return out, out_err


def error_rf_mc(arg, arg_err, N=10, model=None):

    out, out_err =np.nan*np.ones(len(arg)), np.nan*np.ones(len(arg))
    if len(arg.shape) == 1:
        ndim = 1
        for i in tqdm(range(len(arg))):
            X_test = np.random.normal(
                arg[i], np.abs(arg_err[i]),size=N
            )
            y_pred_rand = model.predict(X_test)
            out[i], out_err[i] = get_mcmc_stats(y_pred_rand)
            
    elif len(arg.shape)>=2:
        ndim = arg.shape[1]
        for i in tqdm(range(len(arg))):
            X_test = np.random.normal(
                arg[i,:], np.abs(arg_err[i,:]),size=(N, ndim)
            )
            y_pred_rand = model.predict(X_test)
            out[i], out_err[i] = get_mcmc_stats(y_pred_rand)
    else:
        raise ValueError('input data dimension error!')
        
    return out, out_err
  
def bay_pwlaw(nu, mass, ZZ, mass_err, SAMPLE_SIZE=3000, TUNE_SIZE=3000, TAR_ACCP=0.95):
    """
    single power-law

    """
    lg_nu_err = np.array([0.5 for i in range(len(nu))])
    with pm.Model() as model:
        lgmtot = tt.log10(mass)
        mtot = tt.as_tensor_variable(mass)
        lgnu = tt.log10(nu)
        ZZ = tt.as_tensor_variable(ZZ)
        lg_nu_err = tt.as_tensor_variable(lg_nu_err)
        m_tot_err = tt.as_tensor_variable(mass_err)

        """Prior"""
        alpha = pm.Uniform("alpha", lower=0.1, upper=4.)
        C =  pm.Uniform("C", lower=3., upper=7.)
        lghz = pm.Uniform("lghz", lower=2., upper=2.9)
#         lghz = pm.Normal("lghz", 2.7, 0.3)

        """likelihood"""
        lg_nu_obs = pm.Normal(
            "lg_nu_obs", 
            mu=C - ZZ/(tt.pow(10,lghz)*tt.log(10)) - lghz - alpha*lgmtot,
            sigma=tt.sqrt(lg_nu_err**2+m_tot_err**2/mtot**2), 
            observed=lgnu
        )

        trace = pm.sample(
            SAMPLE_SIZE, tune=TUNE_SIZE, 
            discard_tuned_samples=True, target_accept=TAR_ACCP,
            return_inferencedata=False
        )
        return trace, model
