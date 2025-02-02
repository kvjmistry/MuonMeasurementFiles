import numpy as np
import pandas as pd
try:
    import cPickle as pickle
except ImportError:
    import pickle
import scipy
from scipy import interpolate
from scipy.interpolate import InterpolatedUnivariateSpline

NumToRun=1000

#pull in the combined proposal outputs
musDatamtn=pd.read_hdf('/lcrc/project/NEXT/data/Muon-Rate-Measurement/Proposal/Outputs2022/CombinedProposalInterpOutputs.h5','MuonsProp')  


#get interpolatations for proposal output for all X,Y for each energy


energies=musDatamtn.Energy.unique()
#print(energies)
energies.sort()


for LOC in range(0,len(energies)):
    r=0


    NRG=energies[LOC]
    #print(NRG)
    MUSinterp=musDatamtn[musDatamtn.Energy==NRG]
    



    kX=MUSinterp.X.unique()
    kX.sort()
    lY=MUSinterp.Y.unique()
    lY.sort()


    Xs=[]
    Ys=[]
    Percs=[]
    for X in kX:
        for Y in lY:
            percsum=0
            multi=0
            

            if len(MUSinterp[(MUSinterp.X==X)&(MUSinterp.Y==Y)])==0:
                Xs.append(X)
                print("missing",X,Y)
                Percs.append(0) #need to rerun anything missing
                Ys.append(Y)
                continue
            perc=MUSinterp[(MUSinterp.X==X)&(MUSinterp.Y==Y)].SurvivalPercent.values[0]
            
            Xs.append(X)
            Percs.append(perc)
            Ys.append(Y)
    #print(X,Y,perc)

    df=pd.DataFrame(Xs, columns = ['X'])
    df['Y']=Ys
    df['perc']=Percs

    percsarray=np.array(df.perc)
    percsarray = percsarray.reshape(len(df.X.unique()), len(df.Y.unique()))
    
    #print (np.unique(df.X),np.unique(df.Y),percsarray)
    PercentMuons=scipy.interpolate.RectBivariateSpline(np.unique(df.X),np.unique(df.Y),percsarray,s=0,kx=3, ky=3)
    

    with open('/lcrc/project/NEXT/data/Muon-Rate-Measurement/Proposal/Proposal_Muons_interpolator'+str(int(NRG*10**-3))+'GeV.pkl', 'wb') as f:
        pickle.dump(PercentMuons, f)                            
