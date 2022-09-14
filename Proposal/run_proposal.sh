#!/bin/bash
#SBATCH -J PROPOSAL # A single job name for the array
#SBATCH -c 8 # Number of cores
#SBATCH -p shared # Partition
#SBATCH --mem 1000 # Memory request (6Gb)
#SBATCH -t 0-12:00 # Maximum execution time (D-HH:MM)
#SBATCH -o PROPOSAL_%A_%a.out # Standard output
#SBATCH -e PROPOSAL_%A_%a.err # Standard error

start=`date +%s`

# Set the configurable variables
JOBNAME="PROPOSAL"
FILES_PER_JOB=1
Energy=100
SCRIPT=RunProposalOverXY.py
SLURM_ARRAY_TASK_ID=1

# Create the directory
cd $SCRATCH/guenette_lab/Users/$USER/
mkdir -p $JOBNAME/$Energy
cd $JOBNAME/$Energy

mkdir Outputs

# Copy the files that we need for the jobover
cp ~/packages/PROPOSAL/${SCRIPT} .
cp ~/packages/PROPOSAL/CombiningOutputsInterp.py .
cp ~/packages/PROPOSAL/rocklength_to_detector.pkl .
cp ~/packages/PROPOSAL/ExtendedMountain.pkl .
cp ~/packages/PROPOSAL/config.json .

# Setup nexus and run
echo "Initialising PROPOSAL environment" 2>&1 | tee -a log_nexus_"${SLURM_ARRAY_TASK_ID}".txt
source ~/packages/PROPOSAL/env/bin/activate

for i in $(eval echo "{1..${FILES_PER_JOB}}"); do

	# Replace the energy to run in the file	
	echo "The energy is: ${Energy}" 2>&1 | tee -a log_nexus_"${SLURM_ARRAY_TASK_ID}".txt
	sed -i "s#.*energies=.*#energies=[${Energy}]#" ${SCRIPT}
	python ${SCRIPT} | tee -a log_nexus_"${SLURM_ARRAY_TASK_ID}".txt
	python CombiningOutputsInterp.py |  tee -a log_nexus_"${SLURM_ARRAY_TASK_ID}".txt
	
	echo; echo; echo;
done

rm -rv Outputs | tee -a log_nexus_"${SLURM_ARRAY_TASK_ID}".txt

echo "FINISHED....EXITING" 2>&1 | tee -a log_nexus_"${SLURM_ARRAY_TASK_ID}".txt
end=`date +%s`
runtime=$((end-start))
echo "$runtime s" 2>&1 | tee -a log_nexus_"${SLURM_ARRAY_TASK_ID}".txt
