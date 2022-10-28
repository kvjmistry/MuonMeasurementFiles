import pylab as plt
import numpy as np
import pandas as pd
import scipy
from scipy import interpolate
from scipy.interpolate import InterpolatedUnivariateSpline
try:
    import cPickle as pickle
except ImportError:
    import pickle

from scipy.interpolate import interp2d, NearestNDInterpolator,LinearNDInterpolator


ei = 0
spacing=10

NumToRun=1000
LinInterps={}
NDInterps={}

eps=0.11   # This is a trick to stop divide by zero errors

def GetMuonInfo(startMuon):
    depthMuon   = np.round(depth(*startMuon),2)
    thMuon      = np.round(np.arctan(   (startMuon[0]**2+startMuon[1]**2 +eps)**0.5/(depthMuon+eps)   ),2)
    phiMuon     = np.round(np.arctan2((startMuon[1]+eps),(startMuon[0]+eps)),2)
    return thMuon,phiMuon,depthMuon

#for depth of mountain above the detector
f=open("/n/home05/kvjmistry/packages/PROPOSAL/ExtendedMountain.pkl",'rb')
depth=pickle.load(f)    
f.close()

intexs=[]
inteys=[]
intepercs=[]

for X in range(-550,1500,spacing):
    for Y in range(-2500,750,spacing):
        intexs.append(X)
        inteys.append(Y)


energy = 100

print("Energy: ", energy)

# Load in spline for survival fraction for each energy at a given x, y position. 
f= open('/n/home05/kvjmistry/packages/PROPOSAL/InterpolateScripts/Files/outputs/Proposal_Muons_interpolator'+str(energy)+'GeV.pkl', 'rb')
PercentMuons = pickle.load(f)
f.close()

ei+=1

costhetas=[]
phis=[]
survfrac=[]
intepercs=[] 
thetas=[]

print("Interpolating Muon Survival Fractions...")
for X in range(-550,1500,spacing):        
    for Y in range(-2500,750,spacing):  
        # Get the interpolated survival fraction at a given x, y postion
        intepercs.append(PercentMuons(X,Y)) 

intepercs = np.array(intepercs)      
intepercs=intepercs.reshape(len(np.unique(intexs)), len(np.unique(inteys)))


# Get Muon info for each event
print("Getting Muon Info...")
for i in range(0,len(intexs)):
    x=np.array(intexs).flatten()[i]
    y=np.array(inteys).flatten()[i]
    c=np.array(intepercs).flatten()[i]
    
    startMuon = (x,y)
    
    thMuon,phiMuon,depthMuon=GetMuonInfo(startMuon)
    
    if(np.cos(thMuon)>0.4):
        survfrac.append(c)
        costhetas.append(np.cos(thMuon))
        phis.append(phiMuon)
        thetas.append(thMuon)

#Add shifted phis to satisfy periodic boundary condition
#costhetas=np.concatenate([costhetas,costhetas,costhetas,2-np.array(costhetas)])
#phis=np.concatenate([phis,np.array(phis)-2*np.pi,np.array(phis)+2*np.pi,phis])
#survfrac=np.concatenate([survfrac, survfrac, survfrac,survfrac])
maxcol=max(np.array(survfrac).flatten())

print(costhetas)

print("Interpolating...")
intereff_lin=LinearNDInterpolator(np.array([thetas,phis]).transpose(),np.array(survfrac).flatten(),rescale=True)

LinInterps=intereff_lin


f=open('/n/home05/kvjmistry/packages/PROPOSAL/InterpolateScripts/Files/LinInterps'+str(energy)+'.pkl','wb')
pickle.dump(LinInterps,f)
f.close()


# Add shifted phis to satisfy periodic boundary condition
costhetas=np.concatenate([costhetas,costhetas,costhetas,2-np.array(costhetas)])
phis=np.concatenate([phis,np.array(phis)-2*np.pi,np.array(phis)+2*np.pi,phis])
survfrac=np.concatenate([survfrac, survfrac, survfrac,survfrac])
maxcol=max(np.array(survfrac).flatten())

print("Interpolating...")
intereff_lin=LinearNDInterpolator(np.array([costhetas,phis]).transpose(),np.array(survfrac).flatten(),rescale=True)

LinInterps=intereff_lin

f=open('/n/home05/kvjmistry/packages/PROPOSAL/InterpolateScripts/Files/LinInterpsCosTheta'+str(energy)+'.pkl','wb')
pickle.dump(LinInterps,f)
f.close()






