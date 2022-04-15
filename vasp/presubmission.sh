export PATH=$PATH:/fslhome/lc453/.local/bin/
module load intel-compilers/2017 libfabric/1.8 intel-mpi/2017 mlp/0.2
mlp convert-cfg --output-format=vasp-poscar convex_hull52.cfg POSCAR52_
