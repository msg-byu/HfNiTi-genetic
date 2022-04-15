# This program finds all of the lowest energy configruations from a particular run of the genetic algorithm
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
rank = comm.Get_rank()
nprocs = comm.Get_size()

#mlippy.initialize(comm)
mlippy.initialize(comm)
mlip=mlippy.mtp()
mlip.load_potential('HfNiTi.mtp')

in_dir=".."
prefix=""
suffix="6"
cutoff=0.02
i=0
dists=[]
labels=[]
symbolic=[]
low_e_cfgs=[]
num_each=[]
dict={0:'Hf',1:'Ni',2:'Ti'}
# It reads in data from the chull_dists file from the genetic algorithm
while(os.path.exists(in_dir+"/it"+str(i+1)+"/"+prefix+"chull_dists"+suffix+".npy")):
    data=np.load(in_dir+"/it"+str(i+1)+"/"+prefix+"chull_dists"+suffix+".npy")
    data2=np.load(in_dir+"/it"+str(i+1)+"/"+prefix+"parents_used"+suffix+".npy")
    count=0
    #print(in_dir+"/it"+str(i+1)+"/"+prefix+"relaxed"+suffix+".cfg")
    try:
        cfgs=mlippy.ase_loadcfgs(in_dir+"/it"+str(i+1)+"/"+prefix+"relaxed"+suffix+".cfg")
    except:
        print("failure")
        i+=1
        continue
    for level in data:
        if level<=cutoff and not (level in dists):
            dists.append(level)
            #print(level)
            low_e_cfgs.append(cfgs[count])
            labels.append(data2[count])
        count+=1
    i+=1
i=0
for line in labels:
    symb_lab=[]
    nums=[0,0,0]
    for char in line:
        nums[char]+=1
        symb_lab.append(dict[char])
    #nums.append(dists[i])
    symbolic.append(symb_lab)
    num_each.append(nums)
    i+=1
np.savetxt("special_dists.txt",dists)
np.savetxt("special_labels.txt",symbolic,fmt="%s")
np.savetxt("special_stoichiometry.txt",num_each,fmt='%s')
np.save("special_dists",dists)
np.save("special_stoichiometry",num_each)
np.save("special_labels",labels)
mlippy.ase_savecfgs("special.cfg",low_e_cfgs)
