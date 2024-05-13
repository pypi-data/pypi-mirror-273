"""
Event is a database storing site and cluster info for each migration event

Author: Zeyu Deng
Email: dengzeyu@gmail.com
"""
import numpy as np
import numba as nb
from copy import deepcopy
import json


class Event: 
    """
    mobile_ion_specie_1_index
    mobile_ion_specie_2_index
    local_env_indices_list
    """
    def __init__(self):
        pass

   
    def initialization3(self,mobile_ion_specie_1_index=12,mobile_ion_specie_2_index=15,ea=0.3):
        """3rd version of initialization. The input local_env_indices_list is already sorted. Center atom is equivalent to the Na1 in the 1st version and mobile_ion_specie_2_index is equivalent to the Na2 in the 1st version

        Args:
            mobile_ion_specie_1_index (int, optional): the global index (index in supercell) of the center atom. Defaults to 12.
            mobile_ion_specie_2_index (int, optional): the global index of the atom that the center atom is about to diffuse to. Defaults to 15.
            local_env_indices_list (list, optional): list of integers, which is a list of indices of the neighboring sites in supercell, and is already sorted. Defaults to [1,2,3,4,5].
        """
        self.mobile_ion_specie_1_index = mobile_ion_specie_1_index
        self.mobile_ion_specie_2_index = mobile_ion_specie_2_index

        self.ea = ea
      
    # # @profile
    # def set_occ(self,occ_global):
    #     self.occ_sublat = deepcopy(occ_global[self.local_env_indices_list]) # occ is an 1D numpy array
    

    # @profile
    def set_probability(self,occ_global,v,T): # calc_probability() will evaluate migration probability for this event, should be updated everytime when change occupation
        k = 8.6173303E-5 #ev/K
        if occ_global[self.mobile_ion_specie_1_index] + occ_global[self.mobile_ion_specie_2_index] ==2:
            self.probability = 0.0
        elif occ_global[self.mobile_ion_specie_1_index] == -1:
            self.probability = 0.0
        else: 
            self.probability =  v*np.exp(-1*self.ea/(k*T))

    # @profile
    def update_event(self,occ_global,v,T):
        # self.set_occ(occ_global) # change occupation and correlation for this unit
        self.set_probability(occ_global,v,T)



