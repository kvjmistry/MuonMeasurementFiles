# Running Proposal

This set of scripts is for running on the harvard machines

Requirements:
You should have a virtual env setup with proposal and the relavent dependencies

Overview of files:
- The `setup_proposal.sh` script will setup the environment for you so you can run
proposal.
- The jobs are launched using the `launch_proposal_jobs.sh` script. In here you 
configure the energies you want to run. A separate job will be launched for 
each energy.
- The `run_proposal.sh` is the script that gets run on each job cluster. It copies
over the necessary files to run the proposal code. 
- Each job produces a set of files for each X,Y position. The `CombiningOutputsInterp.py`
script will merge these into one file.
- For each energy, we need to merge the files to get one single output. You can
do that with the `merge_proposal_outputs.py` file. 
- The `RunProposalOverXY.py` script is the main job script that runs the proposal commands.
- Files folder contains various configuration files and other necessary files you need to run

# Configuration of scripts
A set of paths in each file have been hardcoded, so here is what you need to change
in each of your scripts to get it to run.

-----

`setup_proposal.sh`
```
# Here change to the path of your environment to activate
conda activate /n/home05/kvjmistry/miniconda/envs/proposal
```
-----

`Files/config.json`
```
# Change the following lines to a folder called tables, you should create an empty 
# folder in your main repo area where you can set the path to
"path_to_tables" : "/n/home05/kvjmistry/packages/PROPOSAL/resources/tables",
"path_to_tables_readonly" : "/n/home05/kvjmistry/packages/PROPOSAL/resources/tables",
```
----

`run_proposal.sh`
```
# Set these paths to the appropriate value
cp ~/packages/PROPOSAL/${SCRIPT} .
cp ~/packages/PROPOSAL/CombiningOutputsInterp.py .
cp ~/packages/PROPOSAL/rocklength_to_detector.pkl .
cp ~/packages/PROPOSAL/ExtendedMountain.pkl .
cp ~/packages/PROPOSAL/config.json .

# Also make sure you update this line
source ~/packages/PROPOSAL/env/bin/activate

```

----

`merge_proposal_outputs.py`
```
#Set this path to the output of your proposal files
file_dir = os.path.expandvars("/n/holyscratch01/guenette_lab/Users/kvjmistry/PROPOSAL/*/")
```

# Order to run
```
# Launch the jobs
source launch_proposal_jobs.sh

# Merge the jobs
source setup_proposal.sh
python merge_proposal_outputs.py
```

You should now end up with a file called:
`ProposalMuonsCombined.h5`