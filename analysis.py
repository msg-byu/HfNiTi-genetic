# This program collects the average, min, and standard deviations of convex hull distances
# from the iterations of the genetic algorithm
import numpy as np
import os
in_dir=".."
prefix=""
suffix="12"
avgdists=[]
mindists=[]
stdevs=[]
i=0
while(os.path.exists(in_dir+"/it"+str(i+1)+"/"+prefix+"chull_dists"+suffix+".npy")):
    data=np.load(in_dir+"/it"+str(i+1)+"/"+prefix+"chull_dists"+suffix+".npy")
    avgdists.append(np.average(data))
    mindists.append(min(data))
    stdevs.append(np.std(data))
    i+=1
print(avgdists)
print(mindists)
print(stdevs)
