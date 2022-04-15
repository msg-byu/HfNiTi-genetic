import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '/fslhome/lc453/mlip-2/lib')))
import mlippy
from mpi4py import MPI
from ase.db import connect
from ase.optimize import BFGS
from ase.db import connect  # api for connecting to the atoms database
from ase.visualize import view
from ase.io import write
import pymatgen.analysis.phase_diagram as PD
import numpy as np
comm = MPI.COMM_WORLD
mlippy.initialize(comm)
mlip=mlippy.mtp()
mlip.load_potential('HfNiTi.mtp')

mlip.add_atomic_type(72)
mlip.add_atomic_type(28)
mlip.add_atomic_type(22)


configs=mlippy.ase_loadcfgs("special.cfg")
print(configs)
# for struct in configs:
# 	formula=str(struct.symbols)
# 	formula=formula.replace("He", "Ti")
# 	formula=formula.replace("H", "Ni")
# 	formula=formula.replace("X", "Hf")
# 	struct.symbols=formula

#os.system("rm -r images; mkdir images")
os.system("rm -r special_images; mkdir special_images")
count = 1
for cfg in configs:
	print("sup")
	write("special_images/cfg_"+str(count)+".png",cfg)
	count+=1
