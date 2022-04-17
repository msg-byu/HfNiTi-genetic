#!/bin/bash
#SBATCH --job-name=train_mtp
#SBATCH --ntasks=1
#SBATCH --qos=msg
#SBATCH --cpus-per-task=1
#SBATCH --time=40:00:00
#SBATCH --mem-per-cpu=10G
module load intel-compilers/2017 libfabric/1.8 intel-mpi/2017 mlp/0.2-zbl
mlp train HfNiTi.mtp train.cfg
