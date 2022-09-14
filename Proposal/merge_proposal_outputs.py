import pandas as pd
import glob
import os


file_dir = os.path.expandvars("/n/holyscratch01/guenette_lab/Users/kvjmistry/PROPOSAL/*/")
files = glob.glob(os.path.join(file_dir, "Combined*.h5"))
print(files)

dfs = pd.DataFrame()

for f in files:
    df = pd.read_hdf(f)
    dfs = dfs.append(df)

# Write out the dataframe
dfs = dfs.sort_values(by=['Energy'])
dfs.to_hdf("ProposalMuonsCombined.h5",'MuonsProp')
