from ase import Atom, Atoms

# define a function to write configurations for the unit cell, given an array of numbers: 0="Hf"; 1="Ni"; 2="Ti"
def generate_cells(label):
    # length of the sides of the cube:
    #a=lattice_parameter(label)
    #the paper said that a was approximately equal to this :)
    a=8.87
    positions_type0=[]
    positions_type1=[]
    positions_type2=[]
    # label is a string containing three symbols: 0=Hf, 1=Ni, 2=Ti

    position_dict={}

    if len(label)==6:
        position_dict = {
            0 : [0,0,0],
            1 : [a/6,a/6,a/6],
            2 : [a/3,0,0],
            3 : [a/2,a/6,a/6],
            4 : [a*2/3,0,0],
            5 : [a*5/6,a/6,a/6]
        }

    if len(label)==8:
        position_dict = {
            0 : [0,0,0],
            1 : [a/6,a/6,a/6],
            2 : [a/3,0,0],
            3 : [a/2,a/6,a/6],
            4 : [0,a/3,0],
            5 : [a/6,a/2,a/6],
            6 : [a/3,a/3,0],
            7 : [a/2,a/2,a/6]
        }

    if len(label)==12:
        position_dict = {
            0 : [0,0,0],
            1 : [a/6,a/6,a/6],
            2 : [a/3,0,0],
            3 : [a/2,a/6,a/6],
            4 : [a*2/3,0,0],
            5 : [a*5/6,a/6,a/6],
            6 : [0,a/3,0],
            7 : [a/6,a/2,a/6],
            8 : [a/3,a/3,0],
            9 : [a/2,a/2,a/6],
            10 : [a*2/3,a/3,0],
            11 : [a*5/6,a/2,a/6]
        }

    if len(label)==16:
        position_dict = {
            0 : [0,0,0],
            1 : [a/6,a/6,a/6],
            2 : [a/3,0,0],
            3 : [a/2,a/6,a/6],
            4 : [0,a/3,0],
            5 : [a/6,a/2,a/6],
            6 : [a/3,a/3,0],
            7 : [a/2,a/2,a/6],
            8 : [0,0,a/3],
            9 : [a/6,a/6,a/2],
            10 : [a/3,0,a/3],
            11 : [a/2,a/6,a/2],
            12 : [0,a/3,a/3],
            13 : [a/6,a/2,a/2],
            14 : [a/3,a/3,a/3],
            15 : [a/2,a/2,a/2]
        }

    if len(label)==18:
        # define a dictionary the correlates position in the label matrix to position in the unit generate_cell
        position_dict = {
            0 : [0,0,0],
            1 : [a/6,a/6,a/6],
            2 : [a/3,0,0],
            3 : [a/2,a/6,a/6],
            4 : [a*2/3,0,0],
            5 : [a*5/6,a/6,a/6],
            6 : [0,a/3,0],
            7 : [a/6,a/2,a/6],
            8 : [a/3,a/3,0],
            9 : [a/2,a/2,a/6],
            10 : [a*2/3,a/3,0],
            11 : [a*5/6,a/2,a/6],
            12 : [0,a*2/3,0],
            13 : [a/6,a*5/6,a/6],
            14 : [a/3,a*2/3,0],
            15 : [a/2,a*5/6,a/6],
            16 : [a*2/3,a*2/3,0],
            17 : [a*5/6,a*5/6,a/6]
        }

    if len(label)==24:
        position_dict = {
            0 : [0,0,0],
            1 : [a/6,a/6,a/6],
            2 : [a/3,0,0],
            3 : [a/2,a/6,a/6],
            4 : [a*2/3,0,0],
            5 : [a*5/6,a/6,a/6],
            6 : [0,a/3,0],
            7 : [a/6,a/2,a/6],
            8 : [a/3,a/3,0],
            9 : [a/2,a/2,a/6],
            10 : [a*2/3,a/3,0],
            11 : [a*5/6,a/2,a/6],
            12 : [0,0,a/3],
            13 : [a/6,a/6,a/2],
            14 : [a/3,0,a/3],
            15 : [a/2,a/6,a/2],
            16 : [a*2/3,0,a/3],
            17 : [a*5/6,a/6,a/2],
            18 : [0,a/3,a/3],
            19 : [a/6,a/2,a/2],
            20 : [a/3,a/3,a/3],
            21 : [a/2,a/2,a/2],
            22 : [a*2/3,a/3,a/3],
            23 : [a*5/6,a/2,a/2]
        }

    # for the 54 atom unit cell (27 bcc's stacked on each other)
    if len(label)==54:
        # define a dictionary the correlates position in the label matrix to position in the unit generate_cell
        position_dict = {
        0 : [0,0,0],
        1 : [a/6,a/6,a/6],
        2 : [a/3,0,0],
        3 : [a/2,a/6,a/6],
        4 : [a*2/3,0,0],
        5 : [a*5/6,a/6,a/6],
        6 : [0,a/3,0],
        7 : [a/6,a/2,a/6],
        8 : [a/3,a/3,0],
        9 : [a/2,a/2,a/6],
        10 : [a*2/3,a/3,0],
        11 : [a*5/6,a/2,a/6],
        12 : [0,a*2/3,0],
        13 : [a/6,a*5/6,a/6],
        14 : [a/3,a*2/3,0],
        15 : [a/2,a*5/6,a/6],
        16 : [a*2/3,a*2/3,0],
        17 : [a*5/6,a*5/6,a/6],
        18 : [0,0,a/3],
        19 : [a/6,a/6,a/2],
        20 : [a/3,0,a/3],
        21 : [a/2,a/6,a/2],
        22 : [a*2/3,0,a/3],
        23 : [a*5/6,a/6,a/2],
        24 : [0,a/3,a/3],
        25 : [a/6,a/2,a/2],
        26 : [a/3,a/3,a/3],
        27 : [a/2,a/2,a/2],
        28 : [a*2/3,a/3,a/3],
        29 : [a*5/6,a/2,a/2],
        30 : [0,a*2/3,a/3],
        31 : [a/6,a*5/6,a/2],
        32 : [a/3,a*2/3,a/3],
        33 : [a/2,a*5/6,a/2],
        34 : [a*2/3,a*2/3,a/3],
        35 : [a*5/6,a*5/6,a/2],
        36 : [0,0,a*2/3],
        37 : [a/6,a/6,a*5/6],
        38 : [a/3,0,a*2/3],
        39 : [a/2,a/6,a*5/6],
        40 : [a*2/3,0,a*2/3],
        41 : [a*5/6,a/6,a*5/6],
        42 : [0,a/3,a*2/3],
        43 : [a/6,a/2,a*5/6],
        44 : [a/3,a/3,a*2/3],
        45 : [a/2,a/2,a*5/6],
        46 : [a*2/3,a/3,a*2/3],
        47 : [a*5/6,a/2,a*5/6],
        48 : [0,a*2/3,a*2/3],
        49 : [a/6,a*5/6,a*5/6],
        50 : [a/3,a*2/3,a*2/3],
        51 : [a/2,a*5/6,a*5/6],
        52 : [a*2/3,a*2/3,a*2/3],
        53 : [a*5/6,a*5/6,a*5/6]
        }




    # for the 52 atom unit cell (gamma brass)
    if len(label)==52:
        # defining a few values to make organizing the cell easier. Obtained from aflowlib on Nov 1 2021:
        # aflowlib.org/prototype-encyclopedia/A4B9_cP52_215_ei_3efgi.html
        position_dict = {
        0 : [a/6,a/6,a/6],
        1 : [a/3,0,0],
        2 : [a/2,a/6,a/6],
        3 : [a*2/3,0,0],
        4 : [a*5/6,a/6,a/6],
        5 : [0,a/3,0],
        6 : [a/6,a/2,a/6],
        7 : [a/3,a/3,0],
        8 : [a/2,a/2,a/6],
        9 : [a*2/3,a/3,0],
        10 : [a*5/6,a/2,a/6],
        11 : [0,a*2/3,0],
        12 : [a/6,a*5/6,a/6],
        13 : [a/3,a*2/3,0],
        14 : [a/2,a*5/6,a/6],
        15 : [a*2/3,a*2/3,0],
        16 : [a*5/6,a*5/6,a/6],
        17 : [0,0,a/3],
        18 : [a/6,a/6,a/2],
        19 : [a/3,0,a/3],
        20 : [a/2,a/6,a/2],
        21 : [a*2/3,0,a/3],
        22 : [a*5/6,a/6,a/2],
        23 : [0,a/3,a/3],
        24 : [a/6,a/2,a/2],
        25 : [a/3,a/3,a/3],
        26 : [a*2/3,a/3,a/3],
        27 : [a*5/6,a/2,a/2],
        28 : [0,a*2/3,a/3],
        29 : [a/6,a*5/6,a/2],
        30 : [a/3,a*2/3,a/3],
        31 : [a/2,a*5/6,a/2],
        32 : [a*2/3,a*2/3,a/3],
        33 : [a*5/6,a*5/6,a/2],
        34 : [0,0,a*2/3],
        35 : [a/6,a/6,a*5/6],
        36 : [a/3,0,a*2/3],
        37 : [a/2,a/6,a*5/6],
        38 : [a*2/3,0,a*2/3],
        39 : [a*5/6,a/6,a*5/6],
        40 : [0,a/3,a*2/3],
        41 : [a/6,a/2,a*5/6],
        42 : [a/3,a/3,a*2/3],
        43 : [a/2,a/2,a*5/6],
        44 : [a*2/3,a/3,a*2/3],
        45 : [a*5/6,a/2,a*5/6],
        46 : [0,a*2/3,a*2/3],
        47 : [a/6,a*5/6,a*5/6],
        48 : [a/3,a*2/3,a*2/3],
        49 : [a/2,a*5/6,a*5/6],
        50 : [a*2/3,a*2/3,a*2/3],
        51 : [a*5/6,a*5/6,a*5/6]
        }

    for i in range(len(label)):
        if label[i]==0:
            positions_type0.append(position_dict.get(i))
        elif label[i]==1:
            positions_type1.append(position_dict.get(i))
        else:
            positions_type2.append(position_dict.get(i))

    return positions_type0, positions_type1, positions_type2

# turning the positions into a usable data type
def get_crystals(configurations):
    crystal_set=[]
    features={}
    for label in configurations:
        a0_positions, a1_positions, a2_positions = generate_cells(label)
        #parameter = lattice_parameter(label)
        parameter = 8.87
        if len(label)==6:
            cell_vecs = [parameter,parameter/3,parameter/3]
        elif len(label)==8:
            parameter=parameter*3/2
            cell_vecs = [parameter*2/3,parameter*2/3,parameter*2/3]
        elif len(label)==12:
            cell_vecs = [parameter,parameter*2/3,parameter/3]
        elif len(label)==16:
            cell_vecs = [parameter*2/3,parameter*2/3,parameter*2/3]
        elif len(label)==18:
            cell_vecs=[parameter,parameter,parameter/3]
        elif len(label)==24:
            cell_vecs = [parameter,parameter*2/3,parameter*2/3]
        # if False:
        #     print("frick off")
        else:
            cell_vecs = [[parameter,0.0,0.0],[0.0,parameter,0.0],[0.0,0.0,parameter]]
        atoms = []
        counter = 1
        for position in a0_positions:
            atoms.append(Atom(0,position))
        for position in a1_positions:
            atoms.append(Atom(1,position))
        for position in a2_positions:
            atoms.append(Atom(2,position))
        crystal = Atoms(atoms, pbc=True)
        crystal.set_cell(cell_vecs)
        crystal_set.append(crystal)
    return crystal_set

# define a function to estimate the lattce parameter. Information for volumes was taken from aflowlib on Nov 02 2021
def lattice_parameter(label):
    volume=0.0
    for i in range(len(label)):
        # Hf has a unit cell with two atoms and volume of 44.86 cubic angstroms
        v0=44.86/2
        # Ni has a unit cell with three atoms and volume of 32.36 cubic angstroms
        v1=32.36/3
        # Ti has a unit cell with two atoms and volume of 34.5 cubic angstroms
        v2=34.5/2
        if label[i]==0:
            volume+=v0
        elif label[i]==1:
            volume+=v1
        else:
            volume+=v2
    return volume**(1/3)


# define a function to get the component energy of a label passed in. Information for energy was taken from aflowlib on Nov 02 2021
def component_energy(label):
    energy=0.0
    for i in range(len(label)):
        # Hf has a unit cell energy of -9.954 ev/atom
        e0=-9.953
        # Ni has a unit cell energy of -5.778 ev/atom
        e1=-5.778
        # Ti has a unit cell energy of -7.939
        e2=-7.989
        if label[i]==0:
            energy+=e0
        elif label[i]==1:
            energy+=e1
        else:
            energy+=e2
    return energy
