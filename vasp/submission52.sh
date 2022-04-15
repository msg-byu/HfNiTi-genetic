#!/bin/bash
#SBATCH --job-name=52_get_outcars
#SBATCH --ntasks=1
#SBATCH --array=0-112
#SBATCH --qos=msg
#SBATCH --cpus-per-task=1
#SBATCH --time=20:00:00
#SBATCH --mem-per-cpu=100G
ulimit -s unlimited
export PATH=$PATH:/fslhome/lc453/.local/bin/
i=$SLURM_ARRAY_TASK_ID
mkdir 52.$i
cd 52.$i
cp ../INCAR .
cp ../POTCAR ./_POTCAR
cp ../KPGEN .
cp ../POSCAR52_$i ./_POSCAR
../__mlip_pre.pl
cp ../kpoints.x .
./kpoints.x
srun vasp_std
module load intel-compilers/2017 libfabric/1.8 intel-mpi/2017 mlp/0.2
mlp convert-cfg --input-format=vasp-outcar OUTCAR outcar.cfg
perl ../__mlip_post.pl
cd ..
