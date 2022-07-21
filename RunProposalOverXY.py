import pylab as plt
import numpy as np
import pandas as pd
import proposal as pp  #installed with pip
import scipy
import pickle
from scipy import interpolate
from scipy.interpolate import griddata
import crflux.models as crf
import re
import sys
import os.path
from os import path


# a handy function to go from surface position to angles, depth, distance
'''def GetMuonInfo(startMuon):
    depthMuon   = np.round(depth(*startMuon)[0],2)
    distMuon    = np.round(rocklength(*startMuon)[0],2)
    thMuon      = np.round(np.arctan((startMuon[0]**2+startMuon[1]**2)**0.5/depthMuon),2)
    phiMuon     = np.round(np.arctan2(startMuon[1],startMuon[0]),2)
    return thMuon,phiMuon,depthMuon,distMuon
'''

#This function does the business of calling PROPOSAL.
# It is configured in config.json to propagate the muon through a giant block of "standard rock"

def PropagateMuons(MuonEnergyToSimulate,DistToDetector,NumberToRun=1000):
    mu_def = pp.particle.MuMinusDef()
    prop = pp.Propagator(
        particle_def=mu_def,
        config_file="/lcrc/project/NEXT/data/Muon-Rate-Measurement/Proposal/PROPOSAL/config.json"   #in the PROPOSAL resources directory
    )

    
    mu = pp.particle.DynamicData(mu_def.particle_type)

    mu.energy = MuonEnergyToSimulate
    mu.direction = pp.Vector3D(0, 0, -1)

    mu_position = []
    mu_energy = []

    for i in range(NumberToRun):
        sec = prop.propagate(mu,DistToDetector)
        slop=100
        if(np.abs(sec.position[-1].magnitude()-DistToDetector)<slop):
            mu_energy.append(sec.energy[-1])
            mu_position.append(sec.position[-1].magnitude()-DistToDetector)
            
    return mu_energy,mu_position

#to read file
#pdmtn=pd.read_hdf('/lcrc/project/NEXT/data/Muon-Rate-Measurement/MCeQ/MountaintforProposal_OuterPerim.h5')

#to open rocklength from edge of mountain to detector                                                        
f=open("/lcrc/project/NEXT/data/Muon-Rate-Measurement/SmallerNotebooksChecked/rocklength_to_detector.pkl",'rb')                                      
rocklength=pickle.load(f)                                                                                    
f.close() 

f=open("/lcrc/project/NEXT/data/Muon-Rate-Measurement/SmallerNotebooksChecked/rocklength_to_detector.pkl",'rb')                      
depth=pickle.load(f)    
f.close()                                                  

StepSize=50
eps=0.1   # This is a trick to stop divide by zero errors

m_to_cm=100
GeV=1000



NumToRun=1000
#energies=np.linspace(100,30000,15,endpoint=True)
energies=[100,300,400,450,500,550,600,650,700,650,800,900,1000,2000,4000,6000] #in MeV
r=0


for x in range(-550,1500,50): 
    for y in range(-2500,750,50): 

        z=depth(x,y)
        distMuon=rocklength(x,y)
        phioffset=0                      # Orientation of detector relative to map
        alpha=np.arctan((x**2+y**2+eps)**.5/(z+eps))           # spherical alpha coordinate (0 = downgoing)
        beta= round(np.arctan2((y+eps),(x+eps)),2)  # spherical beta coordinate

        files= '/lcrc/project/NEXT/data/Muon-Rate-Measurement/Proposal/Outputs/ProposalMuons'+str(x)+'_'+str(y)+'.h5'
        print ('starting on'+ files)
        if path.isfile(files)==True:
            print (files, 'already exists')
            continue
        r+=1
        srtnrg=[]
        srttheta=[]
        srtphi=[]
        srtdep=[]
        srtdist=[]
        #FinalMuons=[]
        #FinalPos=[]
        perc=[]

        # Run a few energies 
        for nrgs in energies:
            E=nrgs*GeV

            FinalMuons0,FinalPos0=np.array(PropagateMuons(E,distMuon*m_to_cm,NumberToRun=1000),dtype=object)
        
            #FinalMuons.append(len(FinalMuons0))
            #FinalPos.append(len(FinalPos0))
            perc.append(len(FinalMuons0)/NumToRun) #percent of muons that survived to the detector
            srtnrg.append( E)
            srttheta.append(alpha)
            srtphi.append(beta)
            srtdep.append(z)
            srtdist.append(distMuon)
        
        data_out4 = files
        pd.DataFrame({'Energy':srtnrg,
                  'Theta':srttheta,
                  'Phi':srtphi,
                  'DepthOfDet':srtdep,
                  'DistToDet':srtdist,
                  'SurvivalPercent':perc}).to_hdf(data_out4,'MuonsProp')
    if r==5:
        break #this is only because if it ran too long everything would fail so I just had it not run many batches...not ideal obviously
