#!/bin/bash

# Declare an array of string with type, these are the Energy values to run
#declare -a Energies=("100" "300" "400" "450" "500" "550" "600" "650" "700" "650" "800" "900" "1000" "2000" "4000" "6000")
declare -a Energies=("1000" "2000" "4000" "6000")

# Iterate the string array using for loop
for E in ${Energies[@]}; do
   echo "Making jobscripts for Energy value: $E"
   mkdir -p Energy_$E
   cd  Energy_$E
   cp ../run_proposal.sh .
   sed -i "s#.*SBATCH -J.*#\#SBATCH -J ${E}MeV \# A single job name for the array#" run_proposal.sh
   sed -i "s#.*SBATCH -o.*#\#SBATCH -o ${E}MeV_%A_%a.out \# Standard output#" run_proposal.sh
   sed -i "s#.*SBATCH -e.*#\#SBATCH -e ${E}MeV_%A_%a.err \# Standard error#" run_proposal.sh
   sed -i "s#.*Energy=.*#Energy=${E}#" run_proposal.sh
   sbatch run_proposal.sh
   cd ..
done
