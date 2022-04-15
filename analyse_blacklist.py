# This program looks at the various configurations which were added to the blacklist
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '/fslhome/lc453/mlip-2/lib')))
import mlippy
import filecmp
#import mpi4py
from mpi4py import MPI
import generate_unit_cell2 as uc
import random
from ase.optimize import BFGS
from ase.db import connect  # api for connecting to the atoms database
from ase.io import write
import pymatgen.analysis.phase_diagram as PD
import numpy as np
import glob

#defining useful functions
def check(test,array):
    return any(np.array_equal(x, test) for x in array)

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
nprocs = comm.Get_size()

#mlippy.initialize(comm)
mlippy.initialize(comm)
mlip=mlippy.mtp()
mlip.load_potential('../HfNiTi.mtp')

#config=mlippy.ase_loadcfgs('train.cfg')

opts = {"select":"FALSE",
"mtp-filename":"HfNiTi.mtp"}
relax_opts = {"iteration-limit":"990",
"min-dist":"1.5",
"force-tolerance":"1e-3",
"stress-tolerance":"1e-2",
"max-step":"0.03"}

mlip.add_atomic_type(72)
mlip.add_atomic_type(28)
mlip.add_atomic_type(22)

blacklist=[]
# You'll have 
in_dir=".."
for file in glob.glob(in_dir+"/*blacklist*.npy"):
	temp=np.ndarray.tolist(np.load(file))
	for label in temp:
		blacklist.append(label)



print(blacklist)

config=uc.get_crystals(blacklist)

results = mlippy.ase_relax(mlip,config,opts,relax_opts)

relaxed = []
unrelaxed = []

index=0
n_unrelaxed=0
relaxed_labels=[]
unrelaxed_labels=[]
for cfg in results:
	if (cfg.energy!=None):
		relaxed.append(cfg)
		relaxed_labels.append(blacklist[index])
		index+=1
	else:
		unrelaxed.append(cfg)
		unrelaxed_labels.append(blacklist[index+n_unrelaxed])
		n_unrelaxed+=1
		

# calculating the convex hull``
unrelaxed_hull_points=mlippy.ase_loadcfgs('../convex_hull.cfg')
hull_points = mlippy.ase_relax(mlip,unrelaxed_hull_points,opts,relax_opts)
#print(hull_points[0])
#pd = PD.PhaseDiagram([PD.PDEntry(struct.symbols, struct.energy, attribute=struct.id) for struct in hull_points])
entries=[]
entries_cfg=[]
formula=""
for struct in hull_points:
	formula=str(struct.symbols)
	formula=formula.replace("He", "Ti")
	formula=formula.replace("H", "Ni")
	formula=formula.replace("X", "Hf")
	entries.append(PD.PDEntry(formula, struct.energy, attribute=(len(entries)+1)))
	entries_cfg.append(struct)
	num_hull_entries=len(hull_points)
num_children=len(relaxed)
print(entries)
print(len(relaxed))

chull_candidates=[]
# adding all the children to the hull so we can see where they all are ### OLD CODE
# comparing all the children to the hull so we can compare them
for struct in relaxed:
	#print(struct)

	formula=str(struct.symbols)
	formula=formula.replace("He", "Ti")
	formula=formula.replace("H", "Ni")
	formula=formula.replace("X", "Hf")
	chull_candidates.append(PD.PDEntry(formula, struct.energy, attribute=(len(entries)+1)))

pd = PD.PhaseDiagram(entries)
#print("nah bruh	")
low_energy_cfgs=[]
dists=[]
for i in range(num_children):
	try:
		val=pd.get_e_above_hull(chull_candidates[i])
	except:
		# If it doesn't work we want the structures to be seen as extremely unfavorable
		val=10
	dists.append(val)
	if val <= 0.05:
		print(relaxed_labels[i])
		print(val)
		low_energy_cfgs.append(relaxed[i])
mlippy.ase_savecfgs("low_energy.cfg",low_energy_cfgs)
os.system("rm -r blacklist_images; mkdir blacklist_images")
count = 1
for cfg in low_energy_cfgs:
    write("blacklist_images/cfg_"+str(count)+".png",cfg)
    count+=1


status=os.EX_OK
sys.exit(status)