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

# Pull in the combined proposal outputs
musDatamtn=pd.read_hdf('Files/ProposalMuonsCombined_morebins2.h5','MuonsProp')  

# Get interpolatations for proposal output for all X,Y for each energy
energies=musDatamtn.Energy.unique()
print(energies/1000)
energies.sort()

# Loop over the energies
for LOC in range(0,len(energies)):
    r=0

    NRG=energies[LOC]
    print(NRG)
    MUSinterp=musDatamtn[musDatamtn.Energy==NRG]
    
    kX=MUSinterp.X.unique()
    kX.sort()
    lY=MUSinterp.Y.unique()
    lY.sort()

    Xs=[]
    Ys=[]
    Percs=[]

    # Loop over the x and y positions and get the survival fraciton
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
            
            perc = MUSinterp[(MUSinterp.X==X)&(MUSinterp.Y==Y)].SurvivalPercent.values[0]
            
            Xs.append(X)
            Percs.append(perc)
            Ys.append(Y)
    #print(X,Y,perc)

    # Create dataframe for each energy
    df=pd.DataFrame(Xs, columns = ['X'])
    df['Y']=Ys
    df['perc']=Percs

    # Conver the survival fraction df to an array
    percsarray=np.array(df.perc)

    # Reshape to x x y sized
    percsarray = percsarray.reshape(len(df.X.unique()), len(df.Y.unique()))
    
    #print (np.unique(df.X),np.unique(df.Y),percsarray)
    PercentMuons=scipy.interpolate.RectBivariateSpline(np.unique(df.X),np.unique(df.Y),percsarray,s=0,kx=3, ky=3)
    

    with open('Files/outputs/Proposal_Muons_interpolator'+str(int(NRG*10**-3))+'GeV.pkl', 'wb') as f:
        pickle.dump(PercentMuons, f)                            
