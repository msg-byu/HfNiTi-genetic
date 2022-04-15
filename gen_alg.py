# getting everything set up
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '/fslhome/lc453/mlip-2/lib')))
import mlippy
import filecmp
#import mpi4py
from mpi4py import MPI
import generate_unit_cell as uc
import random
from ase.db import connect
from ase.optimize import BFGS
from ase.db import connect  # api for connecting to the atoms database
import pymatgen.analysis.phase_diagram as PD
import numpy as np
import time

#defining useful functions
def check(test,array):
    return any(np.array_equal(x, test) for x in array)

# these won't be really useful without multiprocessing
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
nprocs = comm.Get_size()

mlippy.initialize(comm)
mlip=mlippy.mtp()
mlip.load_potential('HfNiTi.mtp')

# opts is what goes in the mlip.ini file normally
# relax_opts are options that you want to use when relaxing
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

# setting the directories we want to read from/write to
in_dir=""
out_dir=""
iteration=0
prefix=""
suffix="_54"
# setting up the blacklist for the lock-out strategy
if not os.path.exists(prefix+"blacklist"+suffix+".npy"):
	blacklisted=np.array([])
else:
	blacklisted=np.load(prefix+"blacklist"+suffix+".npy")
# If a single configuration make up a proportion of the relaxed configurations
# greater than the threshold, that configuration gets added to the blacklist
threshold=1/2
# adding the possibility of "mutation"
chance_mutation=0.0
# loop through until we get something on the convex hull
mindist=1
# where the loop starts: we'll want to keep iterating until we find something on the convex hull
# while mindist > 0:
while True:
	# either carry on from the last iteration or start with a children file in the current directory
	if not os.path.exists(prefix+"init"+suffix+".npy"):
		iteration=1
	else:
		iteration=np.load(prefix+"init"+suffix+".npy")

	if iteration==1:
		in_dir="./"
		out_dir="it"+str(iteration)+"/"
	else:
		in_dir="it"+str(iteration-1)+"/"
		out_dir="it"+str(iteration)+"/"

	
	os.system("mkdir "+out_dir)
	# this gets the arrays of lists containing 0,1,2 which represents the unit cell
	children=np.load(in_dir+prefix+"children"+suffix+".npy")
	# changing each list of 0,1,2 into a cfg format
	config=uc.get_crystals(children)


	# relaxing the children configurations
	# and setting up their labels so we can ignore the labels for the configurations that failed relaxation
	# also timing the relaxation
	time_1=time.time()

	results = mlippy.ase_relax(mlip,config,opts,relax_opts)

	time_2=time.time()
	print(time_2-time_1)

	# dividing the results into relaxed and unrelaxed (sometimes relaxation fails)
	relaxed = []
	unrelaxed = []

	index=0
	n_unrelaxed=0
	relaxed_labels=[]
	unrelaxed_labels=[]
	for cfg in results:
		if (cfg.energy!=None):
			relaxed.append(cfg)
			relaxed_labels.append(children[index])
			index+=1
		else:
			unrelaxed.append(cfg)
			unrelaxed_labels.append(children[index+n_unrelaxed])
			n_unrelaxed+=1
			

	# calculating the convex hull. The hull will be made from the known hull points, as well as any new points
	# from previous iterations that have been found to be on the convex hull
	if os.path.exists(in_dir+prefix+'convex_hull'+suffix+'.cfg'):
		unrelaxed_hull_points=mlippy.ase_loadcfgs(in_dir+prefix+'convex_hull'+suffix+'.cfg')
	else:
		unrelaxed_hull_points=mlippy.ase_loadcfgs('convex_hull.cfg')
	hull_points = mlippy.ase_relax(mlip,unrelaxed_hull_points,opts,relax_opts)
	#print(hull_points[0])


	# We are converting all of the known hull points into a format that can be read by the phase diagram package
	entries=[]
	entries_cfg=[]
	formula=""
	for struct in hull_points:
		formula=str(struct.symbols)
		# 0,1,2 get read as 'X','H','He', so we're changing that to 'Hf','Ni','Ti'
		formula=formula.replace("He", "Ti")
		formula=formula.replace("H", "Ni")
		formula=formula.replace("X", "Hf")
		entries.append(PD.PDEntry(formula, struct.energy, attribute=(len(entries)+1)))
		entries_cfg.append(struct)
		num_hull_entries=len(hull_points)
	num_children=len(relaxed)
	print(entries)
	print(len(relaxed))

	# We are converting all of the relaxed structures into a format that can be read by the phase diagram package
	chull_candidates=[]
	for struct in relaxed:
		#print(struct)
	
		formula=str(struct.symbols)
		formula=formula.replace("He", "Ti")
		formula=formula.replace("H", "Ni")
		formula=formula.replace("X", "Hf")
		chull_candidates.append(PD.PDEntry(formula, struct.energy, attribute=(len(entries)+1)))

	# making the convex hull out of the known hull points we don't add the relaxed configurations to the
	# convex hull directly. Instead we compare the points to the convex hull made by the known hull points.
	pd = PD.PhaseDiagram(entries)
	
	# comparing the relaxed configurations to the convex hull
	dists=[]
	for i in range(num_children):
		try:
			val=pd.get_e_above_hull(chull_candidates[i])
		except:
			# If it doesn't work we want the structures to be seen as extremely unfavorable
			val=10
		dists.append(val)
		if val<=0.0:
			hull_points.append(relaxed[i])
	mindist=min(dists)
	print("The number of distances is:"+ str(len(dists)))
	print("The number of labels is:"+str(len(relaxed_labels	)))

	# checking if one of the configurations is already on the blacklist
	for label in relaxed_labels:
		match=0
		not_match=0
		if check(label,blacklisted):
			continue
		else:

			for otherlabel in relaxed_labels:
				# I think I have [otherlabel,[0,1,2,1,1,2,0]] here because
				# of how my check function was defined. It works better 
				# if we do this
				if check(label,[otherlabel,[0,1,2,1,1,2,0]]):
					match+=1
				else:
					not_match+=1

			if match/not_match >= threshold:
				temp=np.ndarray.tolist(blacklisted)
				temp.append(np.ndarray.tolist(label))
				blacklisted=np.array(temp)
				print(label," has been added to the blacklist")


	newchildren=[]
	ncontestants=10\
	# add a new child to the set by using a tournament style genetic algorithm
	shuffle=np.random.permutation(len(relaxed_labels))
	# adding random indices to the shuffle because some of the original children were lost due to not being able to relax
	for i in range(len(relaxed_labels),len(children)):
		shuffle=np.append(shuffle,random.randint(0,len(relaxed_labels)-1))
	for i in range(int(ncontestants)):
		for j in range(int(len(children)/(ncontestants*2))):
			indp1=indp2=0
			dist1=10
			dist2=10
			for h in range(2*j*ncontestants,(2*j+1)*ncontestants):
				if dists[shuffle[h]]<dist1:
					dist1=dists[shuffle[h]]
					indp1=shuffle[h]
			for h in range((2*j+1)*ncontestants,(2*j+2)*ncontestants):
				#print(h, " lol")
				if dists[shuffle[h]]<dist2:
					dist2=dists[shuffle[h]]
					indp2=shuffle[h]
			print(indp1)
			print(indp2)
			parent1=relaxed_labels[indp1]
			parent2=relaxed_labels[indp2]

			# make sure that the child isn't on the blacklist
			splitind=random.randint(0,min(len(parent1),len(parent2)))
			newchild1=np.concatenate([parent1[0:splitind],parent2[splitind:]])
			newchild2=np.concatenate([parent2[0:splitind],parent1[splitind:]])
			counter=0
			# Check both children against the blacklist
			if check(newchild1,blacklisted) or check(newchild2,blacklisted):
				while check(newchild1,blacklisted) or check(newchild2,blacklisted):
					print(counter)
					counter+=1
					splitind=random.randint(0,min(len(parent1),len(parent2)))
					newchild1=np.concatenate([parent1[0:splitind],parent2[splitind:]])
					newchild2=np.concatenate([parent2[0:splitind],parent1[splitind:]])
					# If we've gone 10 times, it won't be possible to get a configuration that's
					# not on the blacklist, so we'll add the parents or a completely random
					# configuration
					if counter==10:
						newchild1=parent1
						newchild2=parent2
					if counter>=11:
						newchild1=np.random.randint(3, size=len(parent1))
						newchild2=np.random.randint(3, size=len(parent2))
			print(newchild1)

			for l in range(len(newchild1)):
				if(random.random()<=chance_mutation):
					newchild1[l]=(newchild1[l]+random.randint(1,2))%3
			for l in range(len(newchild2)):
				if(random.random()<=chance_mutation):
					newchild2[l]=(newchild2[l]+random.randint(1,2))%3
			newchildren.append(newchild1)
			newchildren.append(newchild2)
	# saving our data to the assigned directory for this iteratnion
	# saving the relaxed children, their labels, and their distances from the convex hull in formats that are easy to read as well
	# as binaries that python can read
	dict={0:'Hf',1:'Ni',2:'Ti'}
	mlippy.ase_savecfgs(out_dir+prefix+'relaxed'+suffix+'.cfg',relaxed)
	mlippy.ase_savecfgs(out_dir+prefix+'unrelaxed'+suffix+'.cfg',unrelaxed)
	mlippy.ase_savecfgs(out_dir+prefix+'convex_hull'+suffix+'.cfg',hull_points)
	np.save(out_dir+prefix+"parents_used"+suffix,relaxed_labels)
	symbolic=[]
	for line in relaxed_labels:
		symb_lab=[]
		for char in line:
			symb_lab.append(dict[char])
		symbolic.append(symb_lab)
	#print(symbolic)
	np.savetxt(out_dir+prefix+"parents_used"+suffix+".txt",symbolic,newline=']\n[',
	header='Labels for the relaxed parents\n[###############################################################################',
	footer='###############################################################################]',fmt="%s")
	np.save(out_dir+prefix+"parents_failed"+suffix,unrelaxed_labels)
	symbolic=[]
	for line in unrelaxed_labels:
		symb_lab=[]
		for char in line:
			symb_lab.append(dict[char])
		symbolic.append(symb_lab)
	np.savetxt(out_dir+prefix+"parents_failed"+suffix+".txt",symbolic,newline=']\n[',
	header='Labels for the unrelaxed parents\n[###############################################################################',
	footer='###############################################################################]',fmt="%s")
	np.save(out_dir+prefix+"chull_dists"+suffix,dists)
	np.savetxt(out_dir+prefix+"chull_dists"+suffix+".txt",dists,header='Distances above the convex hull\n')
	# saving the new children so they can be used by the next iteration
	np.save(out_dir+prefix+"children"+suffix,newchildren)
	symbolic=[]
	for line in newchildren:
		symb_lab=[]
		for char in line:
			symb_lab.append(dict[char])
		symbolic.append(symb_lab)
	np.savetxt(out_dir+prefix+"children"+suffix+".txt",symbolic,newline=']\n[',
	header='Labels for the children generated this generation\n[###############################################################################',
	footer='###############################################################################]',fmt="%s")
	np.save(prefix+'init'+suffix,(iteration+1))
	np.save(prefix+"blacklist"+suffix,blacklisted)
status=os.EX_OK
sys.exit(status)
