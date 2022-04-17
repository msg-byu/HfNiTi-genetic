#!/bin/bash
#SBATCH --job-name=Master_Genetic_Algorithm54
#SBATCH --ntasks=1
#SBATCH --qos=msg
#SBATCH --cpus-per-task=1
#SBATCH --time=48:00:00
#SBATCH --mem-per-cpu=512M
#export OMP_NUM_THREADS=$SLURM_NTASKS

#mpirun -np $SLURM_NTASKS python gen_alg.py
python gen_alg_master.py
