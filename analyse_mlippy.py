# This finds low-energy configurations and wites them to a .cfg file
# view_mlippy.py takes the outputted file and makes pictures out of
# the configurations
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '/fslhome/lc453/mlip-2/lib')))
import mlippy
from mpi4py import MPI
from ase.db import connect
from ase.optimize import BFGS
from ase.db import connect  # api for connecting to the atoms database
import pymatgen.analysis.phase_diagram as PD
import numpy as np
comm = MPI.COMM_WORLD
mlippy.initialize(comm)
mlip=mlippy.mtp()
mlip.load_potential('HfNiTi.mtp')

mlip.add_atomic_type(72)
mlip.add_atomic_type(28)
mlip.add_atomic_type(22)

configs=mlippy.ase_loadcfgs("relaxed8.cfg")
energies=np.load("chull_dists8.npy")
entries=[]
for struct in configs:
	formula=str(struct.symbols)
	formula=formula.replace("He", "Ti")
	formula=formula.replace("H", "Ni")
	formula=formula.replace("X", "Hf")
	struct.symbols=formula
#pd = PD.PhaseDiagram(entries)
count=0
small_indices=[]
for energy in energies:
	if energy<0.01:
		print(energy)
		small_indices.append(count)
	count+=1
#for thing in pd.all_entries:
#	energy=pd.get_e_above_hull(thing)
#	if energy!=0:
#		#print(energy)
#		if energy<0.05:
#			small_indices.append(count)
#	count+=1
low_energies=[]
for i in small_indices:
	low_energies.append(configs[i])
mlippy.ase_savecfgs("small_indices.cfg",low_energies)

