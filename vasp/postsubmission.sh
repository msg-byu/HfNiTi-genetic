#module load intel-compilers/2017 libfabric/1.8 intel-mpi/2017 mlp/0.2
#for outcar in OUTCAR*
#do
#        mlp convert-cfg --input-format=vasp-outcar --append $outcar newtrain.cfg
#done
rm new_train.cfg
touch new_train.cfg
for i in {0..19}
do
	cat $i/_outcar.cfg >> new_train.cfg
done
