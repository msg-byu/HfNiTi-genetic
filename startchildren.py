import numpy as np
#length of each child
l=18
#number of children
#n=100
seed_data=np.load("./low_18_labels.npy")
n=1000
children=[]
master1=np.array([1, 2, 1, 0, 1, 2]*3)
master2=np.array([1, 0, 1, 2, 1, 2]*3) 
for i in range(n):
    # the commented out section is in case I want to seed the children with found low-energy patterns
    # if i%100<len(seed_data):
    #     if np.random.rand()>0.5:
    #         children.append(np.concatenate([np.random.randint(3,size=6),seed_data[i%100]]))
    #     else:
    #         children.append(np.concatenate([seed_data[i%100],np.random.randint(3,size=6)]))
    # if i%20==50:
    #     children.append(master1)
    # elif i%10==50:
    #     children.append(master2)
    # layers=[]
    # for j in range(3):
    #     index=np.random.randint(len(seed_data+1))
    #     if index==len(seed_data):
    #         bro=np.random.rand()
    #         if bro<1/3:
    #             layers.append(master1)
    #         elif bro<2/3:
    #             layers.append(master2)
    #         else:
    #             layers.append(np.random.randint(3,size=18))
    #     else:
    #         bro=np.random.rand()
    #         if bro < 0.5:
    #             temp=np.array_split(seed_data[index],int(len(seed_data)/2))
    #             temp.reverse()
    #             layers.append(np.concatenate(temp))
    #         else:
    #             layers.append(seed_data[index])
    # children.append(np.concatenate(layers))

    children.append(np.random.randint(3,size=l))

np.save("master_children_54_2",children)