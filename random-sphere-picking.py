#!/usr/bin/env python3

import numpy as np
from astropy.coordinates import SkyCoord
import astropy.units as u
import pandas as pd # manage tables

npoints=10

# Setting limit in declination for NTT telescope: -90° < DEC < +29.5°
d1 = np.cos((-90.0 + 90)*u.deg)
d2 = np.cos((+29 + 90)*u.deg)

# Generating random points between limits in declination
uu = np.random.uniform(-np.pi, np.pi, npoints)
vv = np.random.uniform(d1, d2, npoints)

# Uniform points on a sphere
theta = uu  # right ascension in radians
phi = np.arccos( vv ) - np.pi/2 # declination in radians

# Creating astronomical coordinates arrays
c = SkyCoord(theta, phi, unit="rad")

# Transforming to sexagesimal string
ra = c.ra.to(u.hourangle).to_string(sep=(':'))
dec = c.dec.to_string(sep=':')

# Concat arrays, element string by element string: 00:00:00.000-70:00:00.000
radec = np.core.defchararray.add(ra, dec)

nstars = []
for rd in radec :
    link = "http://archive.eso.org/skycat/servers/ucac2?c="+rd+"&r=0.25,1.7"
    #print(link)
    df=pd.read_csv(link, delimiter="\t")
    df=df.drop(df.index[0]).drop(df.tail(1).index) # "-----" and "[EOD]"
    #   if df["UCAC2 ID"].count() == 0 :
    nstars.append(df["UCAC2 ID"].count())

    
from matplotlib import pyplot as plt
plt.figure(figsize=(8,4.2))
plt.subplot(111, projection="aitoff")
plt.grid(True)
plt.plot(theta, phi, 'o', markersize=2, alpha=0.3)
#plt.plot(emptheta, empphi, 'o', markersize=2, alpha=1)
plt.show()
