#!/usr/bin/env python3

import sys, json, warnings
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy.modeling import models, fitting

try:
    inputjson=json.loads(sys.argv[1])
except:
    print ("ERROR: no data or bad data format provided. Try:")
    print ('\'"{ \\"filename\\":\\"./gaussian2d_example.fits\\",  \\"x\\":682, \\"y\\":410, \\"box\\":10 }\"\'')
    sys.exit(1)

class input_parameters(object):   # Metto tutto il JSON in un oggetto Python
    def __init__(self, inputjson):
        self.__dict__ = json.loads(inputjson)

p=input_parameters(inputjson)     # Ecco i dati in un comodo oggetto

# Immagine vera
hdus=fits.open(p.filename)           
ima=hdus[0].data[p.y-p.box//2:p.y+p.box//2, p.x-p.box//2:p.x+p.box//2]

# Modello e stima iniziale (alcuni nel json di input, altri no per pigrizia)
bell=models.Gaussian2D(amplitude=1200, x_mean=p.x, y_mean=p.y,
                       x_stddev=6, y_stddev=6, bounds={'theta': [-3.14,3.14]} )
back=models.Polynomial2D(degree=0) # Altro modello per il fondo (una costante)

f_init=bell+back # Sommo i due modelli (cfr compound model pyastropd)

# # Per il futuro: un modello migliore per le PSF (la gaussiana fa schifo)
# f_init=models.Moffat2D(amplitude=4200, x_0=p.x, y_0=p.y, gamma=6, alpha=1 )

fit_g=fitting.LevMarLSQFitter()   # Inizializzo il fitter: Levenberg-Marquardt

y,x=np.mgrid[ p.y-p.box//2:p.y+p.box//2, p.x-p.box//2:p.x+p.box//2 ]
with warnings.catch_warnings():     # Faccio il fit
    warnings.simplefilter('ignore') # Ignore model linearity warning from the fitter
    f_fit = fit_g(f_init, x, y, ima)

plt.figure(figsize=(8, 2.5))
plt.inferno()
plt.subplot(1,3,1).imshow(ima,               vmax=ima.max())
plt.title("Data")
plt.subplot(1,3,2).imshow(      f_fit(x, y), vmax=ima.max())
plt.title("Model")
plt.subplot(1,3,3).imshow(ima - f_fit(x, y), vmax=ima.max())
plt.title("Residual")

plt.savefig("data-model-residuals.png")

outputjson=dict(zip(f_fit.param_names, f_fit.parameters)) # Serializza in risultato...
print (json.dumps(outputjson, sort_keys=True, indent=2))  # ...e mostralo in un bel json
