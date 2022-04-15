#!/bin/bash
#SBATCH --job-name=get_outcars0
#SBATCH --ntasks=2
#SBATCH --qos=msg
#SBATCH --cpus-per-task=1
#SBATCH --time=20:00:00
#SBATCH --mem-per-cpu=10G
ulimit -s unlimited
export PATH=$PATH:/fslhome/lc453/.local/bin/
i=(0)
mkdir $i
cd $i
cp ../INCAR .
cp ../POTCAR ./_POTCAR
cp ../KPGEN .
cp ../POSCAR$i ./_POSCAR
../__mlip_pre.pl
cp ../kpoints.x .
./kpoints.x
srun vasp_std
module load intel-compilers/2017 libfabric/1.8 intel-mpi/2017 mlp/0.2
mlp convert-cfg --input-format=vasp-outcar OUTCAR outcar.cfg
perl ../__mlip_post.pl
cd ..

