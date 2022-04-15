module load intel-compilers/2017 libfabric/1.8 intel-mpi/2017 mlp/0.2
for outcar in OUTCAR*
do
        mlp convert-cfg --input-format=vasp-outcar --append $outcar train.cfg
done


