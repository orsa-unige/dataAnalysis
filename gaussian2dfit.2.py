#!/usr/bin/env python

import sys, json, warnings
import numpy as np
import matplotlib.pyplot as plt
from astropy.modeling import models, fitting
from astropy.io import fits

# python3 gaussian2dfit.2.py '"{ \"filename\":\"./gaussian2d_example.fits\",  \"x\":682, \"y\":410, \"box\":10 }\"'
try:
    inputjson = json.loads(sys.argv[1])
except:
    print ("ERROR: no data or bad data format provided")
    sys.exit(1)
    
# Mettere tutto il JSON in un oggetto Python per poter trattare i dati come credi    
class input_parameters(object):
    def __init__(self, inputjson):
        self.__dict__ = json.loads(inputjson)

# Ecco i dati in un comodo oggetto        
p = input_parameters(inputjson)

# Immagine vera
hdus=fits.open(p.filename)
ima=hdus[0].data[p.y-p.box:p.y+p.box, p.x-p.box:p.x+p.box]

# Modello con stima iniziale dei parametri (alcuni nel json di input, altri no per pigrizia)
#f_init=models.Moffat2D(amplitude=4200, x_0=p.x, y_0=p.y, gamma=6, alpha=1 )
f_init=models.Gaussian2D(amplitude=4200, x_mean=p.x, y_mean=p.y, x_stddev=6, y_stddev=6, theta=0.2 )
y,x = np.mgrid[ p.y-p.box:p.y+p.box, p.x-p.box:p.x+p.box ]

# Inizializzo il fitter: Levenberg-Marquardt 
fit_g = fitting.LevMarLSQFitter()

# Faccio il fit
with warnings.catch_warnings():
    # Ignore model linearity warning from the fitter
    warnings.simplefilter('ignore')
    f_fit = fit_g(f_init, x, y, ima)
    
plt.figure(figsize=(8, 2.5))
plt.inferno()
plt.subplot(1,3,1).imshow(ima,               vmax=f_fit.amplitude.value)
plt.title("Data")
plt.subplot(1,3,2).imshow(      f_fit(x, y), vmax=f_fit.amplitude.value)
plt.title("Model")
plt.subplot(1,3,3).imshow(ima - f_fit(x, y), vmax=f_fit.amplitude.value)
plt.title("Residual")

plt.savefig("all.png")

# Serializza in json e mostra il risultato
outputjson=dict(zip(f_fit.param_names, f_fit.parameters))
print (json.dumps(outputjson))
