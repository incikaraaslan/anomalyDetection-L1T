#!/bin/sh
#SBATCH --time=1-06:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=64

module load python3
export DATE=12252023
python3 matchDatafast.py > run_$DATE.log
