module load intel-compilers/2017 libfabric/1.8 intel-mpi/2017 mlp/0.2
for i in {0..19}
do
	cd $i
        mlp convert-cfg --input-format=vasp-outcar OUTCAR train.cfg
	cd ..
done

