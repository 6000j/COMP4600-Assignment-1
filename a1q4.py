import scipy
import networkx as nx
import math
import matplotlib.pyplot as plt
import numpy as np
import typing



def graphsConnected(ns, r):
    for n in ns:
        # print("\t", n)
        rn = r/(math.sqrt(n))
        for _ in range(10):
            G = nx.random_geometric_graph(n, rn, dim = 2)
            if not nx.is_connected(G):
                return False
    return True

# startingGuessValue is a term used to more efficiently repeatedly run this process, but setting it to any value other than 1 makes the algorithm
# much worse at approximating r_c in adversarial cases. 
# This could be optimised furhter to have error cases and such if our initial upper bound guess is wrong
def empiricalDeterminationOfRC(ns, maxDist, errTol, startingGuessRatio = 1):
    
    l = 0
    # We have to consider that because we have a value of 1/2, we need to set this more carefully
    u = maxDist*math.sqrt(max(ns)) * startingGuessRatio
    while (u - l) > errTol:
        r = (u+l)/2
        # print(r)
        if (graphsConnected(ns, r)):
            u = r
        else:
            l = r
    
    return u

def determineRC():
    ns = [100, 500, 1000, 2000]
    rcg = empiricalDeterminationOfRC(ns, math.sqrt(2), 0.01, startingGuessRatio=1)
    return rcg

showHistogram = True
showChecks = True

rc = determineRC()
print(rc)

if showHistogram:
    fig, ax1 = plt.subplots(nrows=1, ncols=1, figsize=(9, 4), sharey=True)
    ns = [100, 500, 1000, 2000] #DeterminationOfRC(ns, math.sqrt(2), 0.01))
    rcs = [rc]
    attmps = 30
    for i in range(attmps):
        # print(i)
        rcs.append(empiricalDeterminationOfRC(ns, math.sqrt(2), 0.01, startingGuessRatio=1/16))

    n_bins = 10
    N, bins, patches = ax1.hist(rcs, bins=n_bins)

    # print(len(bins), len(patches))
    # print(bins)
    for i in range(len(patches)):
        # patches.patches
        if bins[i] < rc and bins[i+1] >= rc:
            patches.patches[i].set_color('green')
            break
    
    ax1.set_xlim(0, 5)
    title_name = "Histogram of found approximations of r_c over " + str(attmps+1) + " attempts"
    ax1.set_title(title_name)
    ax1.set_xlabel("r_c approximations")
    fig.show()


# rcg = empiricalDeterminationOfRC(ns, math.sqrt(2), 0.01)
if showChecks:

    ns = [100, 500, 1000, 2000]
    fig, ax1 = plt.subplots(nrows=1, ncols=1, figsize=(9, 4), sharey=True)
    xs = []
    ys = []
    for rt in range(10, 51, 1):
        r = rt/10
        c = 0
        for n in ns:
            rn = r/(math.sqrt(n))
            for i in range(10):
                G = nx.random_geometric_graph(n, rn, dim = 2)
                if nx.is_connected(G):
                    c += 1
        xs.append(r)
        ys.append(c) 
    
    ax1.plot(xs, ys)
    ax1.axvline(rc, ls='-')
    ax1.set_title("Number of connected graphs in sample of " + str(len(ns)*10) + " graphs for values of r")
    ax1.set_xlabel("r")
    ax1.set_ylabel("Number of connected graphs")

# n_bins = 20
# plt.hist(rcs, bins=n_bins)
# plt.xlim(2, 3)
# title_name = "Histogram of found approximations of r_c over " + str(attmps) + " attempts"
# plt.title(title_name)
# plt.xlabel("r_c approximations")
# plt.show()

# axs[0].hist(rcs)





plt.show()

# rcs = []
# attmps = 30
# for i in range(attmps):
#     print(i)
#     rcs.append(empiricalDeterminationOfRC(ns, math.sqrt(2), 0.01))

# # fig, axs = plt.subplots(1,1)
# n_bins = 20
# plt.hist(rcs, bins=n_bins)
# plt.xlim(2, 3)
# title_name = "Histogram of found approximations of r_c over " + str(attmps) + " attempts"
# plt.title(title_name)
# plt.xlabel("r_c approximations")
# plt.show()

# axs[0].hist(rcs)