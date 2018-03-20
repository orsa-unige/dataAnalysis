#!/usr/bin/env python3

import sys, json
import numpy as np
import matplotlib.pyplot as plt

#lines = sys.stdin.read().splitlines()

#if len(lines) == 0 :

lines=[
    'o-g-50/stats-o-g-50.json',
    'o-g-marginal/stats-o-g-marginal.json',
    'r-g-50/stats-r-g-50.json',
    'r-g-marginal/stats-r-g-marginal.json',
    'o-g-bad-seeing/stats-o-g-bad-seeing.json',
    'o-g-bad-seeing-marginal/stats-o-g-bad-seeing-marginal.json'
]

labels=[
    'No filter, seeing 0.8 arcsec, gaussian 2D',
    'No filter, seeing 0.8 arcsec, marginal distribution',
    'SDSS r filter, seeing 0.8 arcsec, gaussian 2D',
    'SDSS r filter, seeing 0.8 arcsec, marginal distribution',
    'No filter, seeing 1.6 arcsec, gaussian 2D',
    'No filter, seeing 1.6 arcsec, marginal distribution'
]
    
fig,ax=plt.subplots()

for il,l in enumerate(lines) :
    p = json.load(open(l))

    pscale=0.205
    
    magarr=[]
    snrarr=[]
    rmsarr=[]

    for i,v in enumerate(p) :
#        pscale=p[0].pscale
        magarr.append( p[i]['mag'] )
        snrarr.append( p[i]['snr'] )
        rmsarr.append( np.sqrt(np.mean(np.square(p[i]['err_vector']))) )

    ax.scatter(magarr, [x*pscale for x in rmsarr], label=labels[il])
    
    for i,j,k in zip(magarr, [x*pscale for x in rmsarr], snrarr):
        ax.annotate(str(k),xy=(i,j), xytext=(10,10), textcoords='offset points')

ax.axhline(0.1)
ax.legend()

plt.title("RMS of star positions of 100 simulated stars as a function of magnitude. SNR is shown near points.")
plt.xlabel("SDSS r mag")
plt.ylabel("RMS [arcsec]")

plt.show()
