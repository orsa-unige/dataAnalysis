#!/usr/bin/env python

import sys, json
import warnings

import matplotlib.pyplot as plt
import numpy as np

from astropy.modeling.models import Gaussian2D
from astropy.modeling import models, fitting
from astropy.io import fits

# Caricare il JSON in input
# python3.6 gaussian2dfit.2.py '"{ \"filename\":\"./gaussian2d_example.fits\",  \"x\":682, \"y\":410, \"box\":10 }\"'
try:
    inputjson = json.loads(sys.argv[1])
except:
    print ("ERROR: no data or bad data format provided")
    sys.exit(1)
    
# Mettere tutto il JSON in un oggetto Python per poter trattare i dati come credi    
class Payload(object):
    def __init__(self, inputjson):
        self.__dict__ = json.loads(inputjson)

# Ecco i dati in un comodo oggetto        
p = Payload(inputjson)

# Immagine vera
hdus=fits.open(p.filename)
ima1=hdus[0].data[p.y-p.box:p.y+p.box, p.x-p.box:p.x+p.box]

# Modello con stima iniziale dei parametri
f_init=Gaussian2D(amplitude=15000, x_mean=p.x, y_mean=p.y, x_stddev=2, y_stddev=1, theta=0.2 )
y,x = np.mgrid[ p.y-p.box:p.y+p.box, p.x-p.box:p.x+p.box ]

ima2=f_init(x,y)

# fitter: Levenberg-Marquardt 
fit_g = fitting.LevMarLSQFitter()

# Faccio il fit
with warnings.catch_warnings():
    # Ignore model linearity warning from the fitter
    warnings.simplefilter('ignore')
    f_fit = fit_g(f_init, x, y, ima1)

# print results
print ("IN:")
print (f_init)
print ("OUT:")
print (f_fit)
    
plt.figure(figsize=(8, 2.5))
plt.subplot(1, 3, 1)
plt.imshow(ima1, vmax=12000)
plt.title("Data")
plt.subplot(1, 3, 2)
plt.imshow(f_fit(x, y), vmax=12000)
plt.title("Model")
plt.subplot(1, 3, 3)
plt.imshow(ima1 - f_fit(x, y) , vmax=12000)
plt.title("Residual")

plt.savefig("all.png")

# # Serializza in json e rispedisci il risultato al PHP
# #print (json.dumps(f_fit))

# print(f_fit.param_names)
# print(f_fit.parameters)
