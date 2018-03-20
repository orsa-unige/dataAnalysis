#!/usr/bin/env python3

import numpy as np
from matplotlib import pyplot as plt

'''
def sample_spherical(npoints, ndim=3):
        vec = np.random.randn(ndim, npoints) # ndim vectors of npoints each. 
        vec /= np.linalg.norm(vec, axis=0)   # norm of these vectors along each one (axis=0)
        return vec

xi, yi, zi = sample_spherical(1000) 

fig, ax = plt.subplots(1, 1, subplot_kw={'projection':'3d', 'aspect':'equal'})
ax.scatter(xi, yi, zi, s=2, zorder=1)
plt.show()
'''

npoints=10


# theta = np.random.uniform(-np.pi, np.pi, npoints)
# phi = np.arccos( np.random.uniform(-1, 1 ,npoints) )

uu = np.random.random(npoints)
vv = np.random.random(npoints)

theta = 2*np.pi*uu -np.pi
phi = np.arccos( 2*vv-1 ) -np.pi/2

# limit in hour angle HA: -5 h 30 m < HA < 5 h 30 m
# limit in zenith distance ZD: ZD < 70°
# limit in declination DEC: -120° < DEC < +29.5°

from astropy.coordinates import SkyCoord  # High-level coordinates
import astropy.units as u

c = SkyCoord(theta,phi, unit="rad")

ra = c.ra.to(u.hourangle).to_string(sep=(':'))
dec = c.dec.to_string(sep=':')

radec = np.core.defchararray.add(ra, dec) # concat element string by element string

import requests

for rd in radec :
    link = "http://archive.eso.org/skycat/servers/ucac2?c="+rd+"&r=0.25,1.7"

    f = requests.get(link)

    print (f.text)




# plt.figure(figsize=(8,4.2))
# plt.subplot(111, projection="aitoff")
# plt.grid(True)
# plt.plot(theta, phi, 'o', markersize=2, alpha=0.3)
# plt.show()

