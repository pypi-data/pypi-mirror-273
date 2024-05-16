from __future__ import annotations

from .bcftmw import BCFTMW
from .bclif import BCLIF

import pandas as pd
import os


class BCExperiment:
    
    def __init__(self,num : int, path : str= '.'):
        self._mil = num//1000000
        self._th = num//1000
        self.num = num
        self.path = path
        self._sep = ';'
        
        if os.path.exists(os.path.join(path,'version.csv')):
            self.path = path
        else: #maybe this is a savePath
            testpath = os.path.join(path,f'experiments/{self._mil}/{self._th}/{self.num}')
            if os.path.exists(os.path.join(testpath,'version.csv')):
                self.path = testpath
        
        #read separator character from version file
        with open(os.path.join(self.path,'version.csv'),'r') as v:
            l = v.readline()
            self._sep = l.strip()
        self.version = pd.read_csv(os.path.join(self.path,'version.csv'),sep=self._sep,header=1)
        
        self.header = pd.read_csv(os.path.join(self.path,'header.csv'),sep=self._sep,header=0,dtype = {'ObjKey':str,'ArrayKey':str,'ArrayIndex':'Int64','ValueKey':str,'Value':str,'Units':str})
        self.objectives = pd.read_csv(os.path.join(self.path,'objectives.csv'),sep=self._sep,header=0)
        self.log = pd.read_csv(os.path.join(self.path,'log.csv'),sep=self._sep,header=0)
        self.hardware = pd.read_csv(os.path.join(self.path,'hardware.csv'),sep=self._sep,header=0)
        self.clocks = pd.read_csv(os.path.join(self.path,'clocks.csv'),sep=self._sep,header=0)
        
        try:
            self.auxdata = pd.read_csv(os.path.join(self.path,'auxdata.csv'),sep=self._sep,header=0)
        except:
            pass
        
        try:
            self.chirps = pd.read_csv(os.path.join(self.path,'chirps.csv'),sep=self._sep,header=0)
        except:
            pass
        
        if os.path.exists(os.path.join(self.path,'fid')):
            self.ftmw = BCFTMW(self.path,self._sep)
            
        if os.path.exists(os.path.join(self.path,'lif')):
            self.lif = BCLIF(self.path,self._sep)


