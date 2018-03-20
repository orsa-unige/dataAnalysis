#!/usr/bin/env python3
# import time
# start_time = time.time();

import sys, json, warnings
from numpy import pi, mgrid, degrees, linspace, meshgrid, exp, power, argmax
from astropy.io import fits
from scipy import interpolate

#from astropy.modeling import models, fitting
import matplotlib.pyplot as plt

try:
    lines = sys.stdin.readlines();
    inputjson=lines[0];
except:
    print ("ERROR: no data or bad data format provided. You sent:")
    print (sys.stdin)
    sys.exit(1)

class input_parameters(object):   # Metto tutto il JSON in un oggetto Python
    def __init__(self, inputjson):
        self.__dict__ = json.loads(inputjson)

p=input_parameters(inputjson)     # Ecco i dati in un comodo oggetto

# Immagine vera
hdus=fits.open(p.filename)
ima=hdus[0].data[p.y-p.box//2:p.y+p.box//2, p.x-p.box//2:p.x+p.box//2]
hdr=hdus[0].header

imax=ima.sum(axis=0)
imay=ima.sum(axis=1)
x=mgrid[ p.x-p.box//2:p.x+p.box//2 ]
y=mgrid[ p.y-p.box//2:p.y+p.box//2 ]

f_fitx = interpolate.interp1d(x, imax, kind='cubic')
f_fity = interpolate.interp1d(y, imay, kind='cubic')

xx=linspace(x[0], x[len(x)-1], num=10*len(x)) # Resampling just for plot
yy=linspace(y[0], y[len(y)-1], num=10*len(y)) # Resampling just for plot

outputjson=dict() # Serializza in risultato...

outputjson['x_mean_0'] = xx[argmax(f_fitx(xx))]
outputjson['y_mean_0'] = yy[argmax(f_fity(yy))]

# outputjson['x_mean_1'] = daotab['xcentroid'].quantity.value[0] #outputjson.pop('mean_0')
# outputjson['y_mean_1'] = daotab['ycentroid'].quantity.value[0] #outputjson.pop('mean_0')

p.output=outputjson;
p.snr=float(hdr['STON']);
p.pscale=float(hdr['PSCALE']);

print (json.dumps(p.__dict__, sort_keys=True))  # ...e mostralo in un bel json

# fig,ax=plt.subplots()

# ax.scatter(x, imax)
# ax.plot(xx, f_fitx(xx))
# # ax.scatter(y, imay)
# # ax.plot(xx, f_fity(xx))

# plt.show()
