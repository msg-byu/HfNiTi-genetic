# HfNiTi-genetic
A genetic algorithm to find the stable configuration of HfNiTi

To use this code, you'll first need to get access to the mlip-2 repository by filling out the form at https://mlip.skoltech.ru/register/
Once you have access, you can chock out the MLIPPY branch. Follow the instructions on the readme file.

You will need the pymatgen package. The most recent version for me didn't work with my environment, so if you run into that problem, you can get an older version that works with this command: python -m pip install pymatgen==v2021.3.3 --force-reinstall

If you're running this on  MaryLou, than I found I needed to load these modules:

module load intel-compilers libfabric intel-mkl intel-mpi

and add these directories to the python path:

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/apps/intel_parallel_studio_xe/2017_update8/compilers_and_libraries_2017.8.262/linux/mpi/intel64/lib:/apps/libfabric/1.8.0/lib:/apps/intel_parallel_studio_xe/2017_update8/compilers_and_libraries_2017.8.262/linux/compiler/lib/intel64:/apps/intel_parallel_studio_xe/2017_update8/compilers_and_libraries_2017.8.262/linux/mkl/lib/intel64/

when I compiled MLIPPY and each time I wanted to use it.
