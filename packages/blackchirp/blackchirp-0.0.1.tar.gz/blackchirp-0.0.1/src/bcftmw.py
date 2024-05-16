from __future__ import annotations

from .bcfid import BCFid

import numpy as np
import pandas as pd
import os
import warnings

class BCFTMW:
    def __init__(self,path : str, sep : str):
        self.path = path
        self._sep = sep
        self.fidparams = pd.read_csv(os.path.join(self.path,'fid/fidparams.csv'),sep=self._sep,header=0,index_col=0)
        pdf = pd.read_csv(os.path.join(self.path,'fid/processing.csv'),sep=self._sep,header=0,index_col=0)
        self.proc = {}
        for r in pdf.itertuples():
            self.proc[r[0]] = r[1]
        self._numfids = len(self.fidparams)
        
    def get_fids(self,num=0):
        return BCFid.create(num,self.path,self.fidparams,self._sep,self.proc)
    
    def process_sideband(self,
                         which : str="both",
                         avg : str="geometric",
                         min_ft_offset : float=None,
                         max_ft_offset : float=None,
                         frame : int=0,
                         verbose : bool=False,
                         **proc_kwargs) -> (np.array,np.array):
        
        #figure out range of data and create the global x array.
        min_probe = np.min(self.fidparams.probefreq.to_numpy())
        max_probe = np.max(self.fidparams.probefreq.to_numpy())
        fid = BCFid.create(0,self.path,self.fidparams,self._sep,self.proc)
        x,ft = fid.ft(frame=frame,**proc_kwargs)
        bw = np.abs(np.max(x)-np.min(x))
        ftsp = bw/(len(x)-1)
        
        si = 0
        ei = 0
        if min_ft_offset is not None:
            if min_ft_offset <= 0.0:
                raise ValueError("min_ft_offset must be positive")
            
            si = int(np.ceil(min_ft_offset/ftsp))
            
        if max_ft_offset is not None:
            if max_ft_offset <= 0.0:
                raise ValueError("max_ft_offset must be positive")
            
            ei = int(np.floor(max_ft_offset/ftsp))
        
        if which == "lower":
            xx = np.arange(min_probe-max_ft_offset,max_probe-min_ft_offset,ftsp)
        elif which == "upper":
            xx = np.arange(min_probe+min_ft_offset,max_probe+max_ft_offset,ftsp)
        elif which == "both":
            xx = np.arange(min_probe-max_ft_offset,max_probe+max_ft_offset,ftsp)
        else:
            raise ValueError("Which must be 'lower', 'upper', or 'both'")
            
        shots_array = np.zeros_like(xx)
        y_out = np.zeros_like(xx)
        
        if avg == "harmonic":
            avg_f = BC_harm_mean
        elif avg == "geometric":
            avg_f = BC_geo_mean
        else:
            raise ValueError("Avg must be 'geometric' or 'harmonic'")
        
        for i in range(self._numfids):
            if verbose:
                print(f"Processing {i+1}/{self._numfids}")
            fid = BCFid.create(i,self.path,self.fidparams,self._sep,self.proc)
            if (len(fid) == 0) or (fid.shots == 0):
                continue
                
            x,ft = fid.ft(frame=frame,**proc_kwargs)
            x = x[si:ei]
            ftu = ft.flatten()[si:ei]
            ftl = ftu[::-1]
            
            if fid.fidparams['sideband'] == 1:
                xl = x[::-1]
                xu = (fid.fidparams.probefreq - x) + fid.fidparams.probefreq
            else:            
                t = (fid.fidparams.probefreq - x) + fid.fidparams.probefreq
                xl = t[::-1]
                xu = x            
            
            if (which == "lower") or (which == "both"):
                yint = np.interp(xx,xl,ftl,left=0.,right=0.)
                yshots = np.where(yint>0.0,fid.shots,0.0)
                
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    y_out = avg_f(y_out,yint,shots_array,yshots)
                shots_array += yshots
                
            if (which == "upper") or (which == "both"):
                yint = np.interp(xx,xu,ftu,left=0.,right=0.)
                yshots = np.where(yint>0.0,fid.shots,0.0)
                
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    y_out = avg_f(y_out,yint,shots_array,yshots)
                shots_array += yshots
                
        return xx,y_out
                

def BC_harm_mean(y1 : np.array, y2 : np.array, s1 : np.array, s2 : np.array) -> np.array: 
    return np.where(s1==0,y2,np.where(s2==0,y1,(s1+s2)/(s1/y1 + s2/y2)))

def BC_geo_mean(y1 : np.array, y2 : np.array, s1 : np.array, s2 : np.array) -> np.array: 
    return np.where(s1==0,y2,np.where(s2==0,y1,np.exp( (s1*np.log(y1) + s2*np.log(y2))/(s1+s2) )))

