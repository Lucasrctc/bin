import pickle
import matplotlib.pyplot as plt
import numpy as np
from Feather import Orion

with open('Orion.pickle', 'rb') as handle:
    b = pickle.load(handle)

lists = sorted(b.mult_costs.items())
mult_x, mult_y = zip(*lists)

lists = sorted(b.disc_costs.items())
disc_x, disc_y = zip(*lists)

lists = sorted(b.gen_costs.items())
gen_x, gen_y = zip(*lists)

plt.plot(gen_x, gen_y)
plt.plot(gen_x, np.log(gen_y))
plt.show()
