from kmc import KMC
from tracker import Tracker
from event import Event
from line_profiler import LineProfiler
import time
import making_structure_specific_files
import event_generator
from matplotlib import pyplot as plt 


# #The below is only necessary one time
# making_structure_specific_files.make_supercell_size_specific_files(size=(6,6,6))

specific_structure = event_generator.make_random_structure(0.5)
events = event_generator.generate_events(structure_array=specific_structure)
initial_occupation = event_generator.generate_initial_occupation(specific_structure, 0.5)
kmc_object = KMC()

events = kmc_object.initialization3(v=1E13, event_fname=events, 
                                    occ = initial_occupation, T=300)
# start = time.time()
tracker = kmc_object.run3(kmc_pass=100, events=events, T=300)





