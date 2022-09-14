import pandas as pd
import re
import glob

r=0

for files in glob.glob('Outputs/ProposalMuons*.h5'):
    print (files)
    
    run=re.search('Muons(.*)_', files)
    X=str(run.group(1))
    run=re.search('0_(.*).h5', files)
    Y=str(run.group(1))
    if r==0:
        musDatamtn=pd.read_hdf(files)
        musDatamtn['X']=    X
        musDatamtn['Y']=    Y        
        print(musDatamtn)
        r+=1
    else:
        df=pd.read_hdf(files)
        df['X']=    X
        df['Y']=    Y  
        musDatamtn=musDatamtn.append(df, ignore_index=True)


musDatamtn['X'] = musDatamtn['X'].astype(float)        
musDatamtn['Y'] = musDatamtn['Y'].astype(float)          


data_out1 = f'CombinedProposalInterpOutputs.h5'

musDatamtn.to_hdf(data_out1,'Muons')

