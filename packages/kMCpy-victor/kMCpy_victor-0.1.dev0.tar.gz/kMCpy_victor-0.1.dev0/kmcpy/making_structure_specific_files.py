# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 09:08:03 2024

@author: vlandgraf
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 17:26:40 2024

@author: vlandgraf
"""

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
import numba
import numpy as np 

def make_supercell_size_specific_files(size=(2,2,2)):

    LNS = Structure.from_spacegroup("Fm-3m", Lattice.cubic(5.578),
                                    ['S2-', "Na+", "Li+"], [[0, 0, 0], [0, 0.5, 0], [0.25, 0.25, 0.25]])



    big_supercell = LNS*size
    big_supercell_dict = big_supercell.as_dict()
    big_supercell.sort()


    lattice = Lattice.from_dict(big_supercell.lattice.as_dict())

    oct_cutoff = int(big_supercell.composition.as_dict()['Na+'])
    tet_cutoff = int(big_supercell.composition.as_dict()['Li+'] + oct_cutoff)
    oct_boundary = [0, oct_cutoff]
    tet_boundary = [oct_cutoff, tet_cutoff]
    anion_boundary = [tet_cutoff, None]
    f_coords = big_supercell.frac_coords

    f_coords_oct =  f_coords[:oct_boundary[1]]






    @numba.jit
    def sort_distances_and_add_index(input_distances, add_to_index): 
        return sorted([(i+add_to_index,j) for i,j in enumerate(input_distances) ], key=lambda x: x[1])

    @numba.jit
    def make_integer_list(input_list): 
        return [int(i) for i in input_list]

    @numba.jit
    def check_fraction(input_number, target): 
        return np.abs(input_number - target) <=0.015

    def make_random_structure(tet_boundary, N_fraction, num_atoms_supercell): 
        list_to_sample_from = ['N' for i in range(int(1E5))] + ['S' for i in range(int(1E5*(1-N_fraction)/N_fraction))]
        random.shuffle(list_to_sample_from)
        continuation=True
        while continuation: 
            
            s = ['Li' for i in range(tet_boundary[1])] + [random.choice(list_to_sample_from) for i in range(tet_boundary[1],num_atoms_supercell)]
            
            u,c = np.unique(s, return_counts=True)
            count_dict = dict(zip(u,c))
            if 'N' not in count_dict.keys():
                pass
            elif check_fraction(count_dict['N']/(count_dict['S']+count_dict['N']), N_fraction):
                continuation=False
            else:
                pass
        return np.array(s)


    def get_composition_of_structure(input_structure): 
            u,c = np.unique(s, return_counts=True)
            count_dict = dict(zip(u,c))
            return count_dict, count_dict['N']/(count_dict['N']+count_dict['S'])
        
    # def filter_out_distances(index_1, array_of_indices, lattice, coords): 
    #     lattice.get_distance_and_image(coords[index_1], coords[i], jimage = [0,0,0])

    oct_tet_keys = []
    tet_oct_keys = []
    tet_tet_keys = []

    anions_surrounding_site = {k:[] for k,_ in enumerate(f_coords)}


    for index,site in enumerate(f_coords[oct_boundary[0]:oct_boundary[1]]):
        
        site_index = index+0
        tmp_v = tet_boundary[0]
        #Find tetrahedral neighbors
        distances = lattice.get_all_distances(site, f_coords[tmp_v:])[0]
        sorted_distances_with_index = np.array(sort_distances_and_add_index(distances,tmp_v))#1 to keep the 1 distance away
        neighbouring_tet = sorted_distances_with_index[:8,0]
        neighbouring_anions = sorted_distances_with_index[8:14,0]
        #Get the eight tetrahedra ssorteurroundingurrounding the octahedra
        oct_tet_keys.extend([(site_index,int(i)) for i in neighbouring_tet])
        tet_oct_keys.extend([(int(i),site_index) for i in neighbouring_tet])
        anions_surrounding_site[index].extend(make_integer_list(neighbouring_anions))
        
    for index,site in enumerate(f_coords[tet_boundary[0]:tet_boundary[1]]):
        tmp_v = tet_boundary[0]
        site_index = index+tmp_v
        distances = lattice.get_all_distances(site, f_coords[tmp_v:])[0]
        sorted_distances_with_index = np.array(sort_distances_and_add_index(distances,tmp_v))#1 to keep the 1 distance away
        neighbouring_tet = sorted_distances_with_index[5:11,0]
        neighbouring_anions = sorted_distances_with_index[1:5,0] 
        anions_surrounding_site[site_index].extend(make_integer_list(neighbouring_anions))
        tet_tet_keys.extend([(site_index, int(i)) for i in neighbouring_tet])
    

    bottleneck_dictionary = {k:[] for k in tet_oct_keys+oct_tet_keys+tet_tet_keys}

    for site_pair in oct_tet_keys+tet_tet_keys:
        surr_anions = anions_surrounding_site[site_pair[0]] + anions_surrounding_site[site_pair[1]]
        unique, count = np.unique(surr_anions, return_counts=1)
        bottleneck_anions = [j for i,j in enumerate(unique) if count[i]==2]
        bottleneck_dictionary[site_pair] = bottleneck_anions
        bottleneck_dictionary[site_pair[::-1]] = bottleneck_anions





    with open('anions_surrounding_site', 'wb') as h: 
        pkl.dump(anions_surrounding_site, h)
        
    with open('keys_both_ways.pkl', 'wb') as h:
        keys = [oct_tet_keys, tet_oct_keys, tet_tet_keys]

        pkl.dump(keys, h)

    with open('bottlenecks.pkl', 'wb') as h: 
        pkl.dump(bottleneck_dictionary, h)

    big_supercell.replace_species({'Na+': 'Li+'})

    Poscar(big_supercell).write_file('kmc_supercell_reference_poscar.vasp')

    keys_2 = keys[0]+keys[1]+keys[2]
    site_to_event_list = {i:[]  for i in range(np.max(keys_2)+1)}
    for index, k in enumerate(keys_2):
        site_to_event_list[k[0]].append(index)
        site_to_event_list[k[1]].append(index)


    with open('site_to_event_list.pkl', 'wb') as h: 
        pkl.dump(site_to_event_list,h)






