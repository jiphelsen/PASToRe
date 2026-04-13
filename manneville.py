import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple,Union,Literal,Set, Union,List
from util import n_letter_alphabet
from PASToRe import PASToRe
from scipy.optimize import root_scalar

######################## MANNEVILLE ########################

############## CONFIG ##############

PLOT_MANNEVILLE = False

flatten = lambda arr : [x for sub in arr for x in sub]
POWER = 4

SIZES = [1,5] + flatten([[(10**j)*i for i in range(1,11)] for j in range(1,POWER+1)])
NUMBER_OF_PARTITIONS = 10 # make sure this is still a character in the ascii range!
ALPHABET=n_letter_alphabet(NUMBER_OF_PARTITIONS)
Z=4
past = PASToRe(ALPHABET)
###########

manneville = lambda z : (lambda x : (x+ x**z) % 1 )
mannevillez =  manneville(Z)

if PLOT_MANNEVILLE:
    x = np.linspace(0, 1, 1000)
    y = mannevillez(x)
    plt.plot(x, y)
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.title("Manneville map (z=2)")
    plt.show()


# making the partitions

def get_next(prev,z):
    f = lambda x: x + x**z - prev
    sol = root_scalar(f, bracket=[0, 1], method='bisect')
    return sol.root

eta = get_next(1,Z) # finding jump in manneville map


#partitions work their way down from the starting number
def make_partitions(z,nb,start):
    assert nb >0
    result = []
    prev = start
    for i in range(nb-1):
        result.append(prev)
        prev=get_next(prev,z)
    return result

partitions = make_partitions(Z,NUMBER_OF_PARTITIONS,eta)

def get_partition(part,y):
    assert 0<=y<=1
    i=0
    for i in range(len(part)):
        p=part[i]
        if y > p:
            return ALPHABET[i]
    return ALPHABET[len(part)]

def get_orbits_I(part,start,sizes=None):
    if sizes is None:
        sizes= [10**3]

    to_compress_str = ""
    cur=start
    res = []
    for i in range(sizes[-1]):
        if i in sizes: # this still can be optimized
            res.append(past.I_Z(to_compress_str))
            past.clear()
        to_compress_str+=get_partition(part,cur)
        cur = mannevillez(cur)

    res.append(past.I_Z(to_compress_str)) # hard coded for last i
    past.clear()
    return res

start_points = np.random.uniform(0.0, 1.0, 7) # [0.2,0.42,0.45,eta,get_next(0.42,Z)]
data  =[]
for point in start_points:
    data.append(get_orbits_I(partitions,point,SIZES))




for series in data:
    plt.plot(SIZES[:len(series)], series, marker='x')

plt.xscale("log")
plt.yscale("log")

plt.xlabel("iterations")
plt.ylabel("length of compressed orbit")

plt.show()
#print(get_partition(partitions, 0.32))
#print(get_orbits_I(partitions,0.11))


