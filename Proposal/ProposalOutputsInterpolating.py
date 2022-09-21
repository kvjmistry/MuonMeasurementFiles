import pylab as plt
import numpy as np
import pandas as pd
import scipy
from scipy import interpolate
from scipy.interpolate import InterpolatedUnivariateSpline

import re
import sys

import matplotlib.pyplot as plt
import random
try:
    import cPickle as pickle
except ImportError:
    import pickle
from scipy.interpolate import interp2d, NearestNDInterpolator,LinearNDInterpolator


ei=0
spacing=10

NumToRun=1000
LinInterps={}
NDInterps={}

eps=0.11   # This is a trick to stop divide by zero errors

energies=[100,300,400,450,500,550,600,650,700,800,900,1000,2000,4000,6000]



def GetMuonInfo(startMuon):
    depthMuon   = np.round(depth(*startMuon),2)
    distMuon    = np.round(rocklength(*startMuon),2)
    thMuon      = np.round(np.arctan((startMuon[0]**2+startMuon[1]**2 +eps)**0.5/(depthMuon+eps)),2)
    phiMuon     = np.round(np.arctan2((startMuon[1]+eps),(startMuon[0]+eps)),2)
    return thMuon,phiMuon,depthMuon,distMuon

#to open rocklength from edge of mountain to detector                                                        
f=open("/lcrc/project/NEXT/data/Muon-Rate-Measurement/SmallerNotebooksChecked/rocklength_to_detector.pkl",'rb')                                      
rocklength=pickle.load(f)                                                                                    
f.close() 

#for depth of mountain above the detector
f=open("/lcrc/project/NEXT/data/Muon-Rate-Measurement/SmallerNotebooksChecked/ExtendedMountain.pkl",'rb')                      
depth=pickle.load(f)    
f.close()  

#Xmin=-600-spacing  
#Xmax=600+spacing/2                                                                                                      
#Ymin=-600-spacing
#Ymax=600+spacing/2                                                                                                                                      

intexs=[]
inteys=[]
intepercs=[]

for X in range(-550,1500,spacing):          
    for Y in range(-2500,750,spacing):            
          intexs.append(X)                               
          inteys.append(Y)      
          




for energy in energies:
    f= open('../Proposal/PROPOSALInterpFunctions/Proposal_Muons_interpolator'+str(energy)+'GeV.pkl', 'rb')
    PercentMuons = pickle.load(f)
    f.close()

    ei+=1
    
    costhetas=[]
    phis=[]
    survfrac=[]


    intepercs=[] 

    for X in range(-550,1500,spacing):        
        for Y in range(-2500,750,spacing):  
            intepercs.append(PercentMuons(X,Y)) 

    intepercs = np.array(intepercs)      
    intepercs=intepercs.reshape(len(np.unique(intexs)), len(np.unique(inteys)))

                                                                                                  
    for i in range(0,len(intexs)):
        x=np.array(intexs).flatten()[i]
        y=np.array(inteys).flatten()[i]
        c=np.array(intepercs).flatten()[i]
        startMuon = (x,y)
        thMuon,phiMuon,depthMuon,distMuon=GetMuonInfo(startMuon)
        if(np.cos(thMuon)>0.4):
            survfrac.append(c)
            costhetas.append(np.cos(thMuon))
            phis.append(phiMuon)

    #Add shifted phis to satisfy periodic boundary condition
    costhetas=np.concatenate([costhetas,costhetas,costhetas,2-np.array(costhetas)])
    phis=np.concatenate([phis,np.array(phis)-2*np.pi,np.array(phis)+2*np.pi,phis])
    survfrac=np.concatenate([survfrac, survfrac, survfrac,survfrac])
    maxcol=max(np.array(survfrac).flatten())

    intereff_lin=LinearNDInterpolator(np.array([costhetas,phis]).transpose(),np.array(survfrac).flatten(),rescale=True)

    LinInterps[energy]=intereff_lin
    
f=open("../Proposal/LinInterps.pkl",'wb')
pickle.dump(LinInterps,f)
f.close()
