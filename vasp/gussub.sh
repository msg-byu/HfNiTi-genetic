#!/bin/bash
#SBATCH --nodes=1 --ntasks=24
#SBATCH --mem=64G
#SBATCH --time=6-00:00:00
#SBATCH -C 'avx2'
#SBATCH --job-name=vasp54

export OMP_NUM_THREADS=1
module purge
module load libfabric
module load intel-compilers/2017
module load intel-mpi/2017
export PATH=$PATH:/fslhome/lc453/.local/bin/
srun vasp_std

