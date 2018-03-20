#!/usr/bin/env python3
# import time
# start_time = time.time();

import sys, json, warnings
from numpy import pi, mgrid, degrees, linspace
from astropy.io import fits
from astropy.modeling import models, fitting
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

# Modello e stima iniziale ***solo su x***
bellx=models.Gaussian1D(amplitude=1200, mean=p.x, stddev=6)
belly=models.Gaussian1D(amplitude=1200, mean=p.y, stddev=6)
back=models.Polynomial1D(degree=0) # Altro modello per il fondo (una costante)
f_initx=bellx+back # Sommo i due modelli (cfr compound model pyastropd)
f_inity=belly+back # Sommo i due modelli (cfr compound model pyastropd)

fit_g=fitting.LevMarLSQFitter()   # Inizializzo il fitter: Levenberg-Marquardt

x=mgrid[ p.x-p.box//2:p.x+p.box//2 ]
y=mgrid[ p.y-p.box//2:p.y+p.box//2 ]

with warnings.catch_warnings():     # Faccio il fit
    warnings.simplefilter('ignore') # Ignore model linearity warning from the fitter
    f_fitx = fit_g(f_initx, x, imax)
    f_fity = fit_g(f_inity, y, imay)

outputjson=dict(zip(f_fitx.param_names, f_fitx.parameters)) # Serializza in risultato...
outputjson['x_mean_0'] = outputjson.pop('mean_0')
outputjson['x_stddev_0'] = outputjson.pop('stddev_0')
outputjson.update(dict(zip(f_fity.param_names, f_fity.parameters))) # Serializza in risultato...
outputjson['y_mean_0'] = outputjson.pop('mean_0')
outputjson['y_stddev_0'] = outputjson.pop('stddev_0')

p.output=outputjson;
p.snr=float(hdr['STON']);
p.pscale=float(hdr['PSCALE']);

print (json.dumps(p.__dict__, sort_keys=True))  # ...e mostralo in un bel json

# fig,ax=plt.subplots()
# xx=linspace(x[0], x[len(x)-1], num=10*len(x))
# ax.scatter(x, imax)
# ax.plot(xx, f_fitx(xx))
# ax.scatter(y, imay)
# ax.plot(xx, f_fity(xx))

# plt.show()
