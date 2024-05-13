import pymatgen
from pymatgen.core import Composition
from pymatgen.core import Structure
from pymatgen.core import Lattice
from pymatgen.transformations.standard_transformations import OrderDisorderedStructureTransformation as ODST
from pymatgen.transformations.standard_transformations import PartialRemoveSpecieTransformation
import pickle
from pymatgen.analysis.ewald import EwaldSummation
# partial_Fe_Li=Composition({"Fe2+":1/3, "Li1+":2/3})
import random
import copy
from pymatgen.io.vasp.outputs import Poscar
import sys
import time
import pickle as pkl
from pymatgen.core import Lattice
# Making Li10Fe8S8O8
from numba import jit
import numpy as np 
from event import Event


@jit
def insert_nitrogen(N_sites, structure_list_S_only): 
    return  [-1 if index in N_sites else element for index,element in enumerate(structure_list_S_only)]


def make_random_structure(N_fraction, reference_structure_file='kmc_supercell_reference_poscar.vasp'): 
    # structure = Poscar.from_file('kmc_supercell_reference_poscar.vasp').structure
    structure = Poscar.from_file(reference_structure_file).structure
    num_of_Li_sites = int(structure.composition.as_dict()['Li'])
    structure_list_S_only = [0 for i in range(num_of_Li_sites)] + [1 for i in range(len(structure) - num_of_Li_sites)]
    index_range_anions = range(num_of_Li_sites, len(structure))
    N_sites = random.sample(index_range_anions, int(N_fraction*len(index_range_anions)))
    structure_list = insert_nitrogen(N_sites, structure_list_S_only)
    return np.array(structure_list)




def generate_events(structure_array, jump_library_file = 'jump_library_with_code_keys.pkl', 
                    keys_both_ways_file ='keys_both_ways.pkl', anions_surr_site_file =  'anions_surrounding_site',
                      b_necks_file = 'bottlenecks.pkl'):
    
    


    with open(keys_both_ways_file, 'rb') as h: 
        keys = pkl.load(h)
        oct_tet_keys, tet_oct_keys, tet_tet_keys = keys[0], keys[1], keys[2]
        keys = oct_tet_keys+tet_oct_keys+tet_tet_keys

    with open(anions_surr_site_file, 'rb') as h: 
        anions_surrounding_site = pkl.load(h)

    with open(b_necks_file, 'rb') as h: 
        b_necks = pkl.load(h)

    with open(jump_library_file , 'rb') as h: 
        jump_library = pkl.load(h)

    events = [None for key in keys]
    for index, key in enumerate(keys): 
        anions_1st_site = anions_surrounding_site[key[0]]
        first_code = np.sum(structure_array[anions_1st_site])
        anions_2nd_site = anions_surrounding_site[key[1]]
        second_code = np.sum(structure_array[anions_2nd_site])
        bneck_anions = b_necks[key]
        if len(bneck_anions)>3:
            raise ValueError("The length of 'bneck_anions' should not exceed 3. This problem arises for 1x1x1 supercells \n make the supercell larger at least (2x2x2) and the issue is solved.)")

        bottleneck_code = np.sum(structure_array[bneck_anions])
        fourth_code = len(anions_1st_site)
   
        input_tuple = (first_code, second_code, bottleneck_code, fourth_code)
        ea = jump_library[input_tuple]
        event = Event()
        event.initialization3(key[0], key[1], ea)
        events[index] = event
        
    return events

def generate_initial_occupation(structure_array, fraction_of_N):

    num_of_Li = np.count_nonzero(structure_array == 0)

    tet = int(num_of_Li*2/3)
    tet_occupation = [1 for i in range(tet)]
    occupied_oct = int(num_of_Li*1/3*fraction_of_N)
    oct_occupation = [1 for i in range(occupied_oct)]+[-1 for i in range(num_of_Li-tet-occupied_oct)]
    random.shuffle(oct_occupation)

    np.count_nonzero(np.array(oct_occupation) == 1)
    intial_occupation = tet_occupation+oct_occupation

    return intial_occupation
















    