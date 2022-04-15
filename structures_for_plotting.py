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


dict={0:'Hf',1:'Ni',2:'Ti'}
cfgs_6=mlippy.ase_loadcfgs("specials_6/special.cfg")
cfgs_12=mlippy.ase_loadcfgs("specials_12/special.cfg")
cfgs_18=mlippy.ase_loadcfgs("specials_18/special.cfg")
good_cfgs=[cfgs_6[2-1],cfgs_6[3-1],cfgs_12[76-1],cfgs_12[22-1],cfgs_18[0],cfgs_18[1]]
mlippy.ase_savecfgs("to_plot.cfg",good_cfgs)
