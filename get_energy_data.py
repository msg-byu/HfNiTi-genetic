import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '/fslhome/lc453/mlip-2/lib')))
from mpi4py import MPI
from ase.db import connect
from ase.optimize import BFGS
from ase.db import connect  # api for connecting to the atoms database
import numpy as np


in_dir=".."
prefix=""
suffix="6"
cutoff=0.01
i=0
min_dists=[]
curr_min=10
while(os.path.exists(in_dir+"/it"+str(i+1)+"/"+prefix+"chull_dists"+suffix+".npy")):
    data=np.load(in_dir+"/it"+str(i+1)+"/"+prefix+"chull_dists"+suffix+".npy")
    print(min(data))
    if min(data)<curr_min:
        curr_min=   min(data)
    min_dists.append(curr_min)
    i+=1


print(min_dists)
i=0
