#!/usr/bin/env python3
# import time
# start_time = time.time();

import sys, json, warnings
from numpy import pi, mgrid, degrees
from astropy.io import fits
from astropy.modeling import models, fitting

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

# Modello e stima iniziale (alcuni nel json di input, altri no per pigrizia)
bell=models.Gaussian2D(amplitude=1200, x_mean=p.x, y_mean=p.y,
                       x_stddev=6, y_stddev=6, bounds={'theta': [-pi,pi]} )
back=models.Polynomial2D(degree=0) # Altro modello per il fondo (una costante)

f_init=bell+back # Sommo i due modelli (cfr compound model pyastropd)

# # # Per il futuro: un modello migliore per le PSF (la gaussiana fa schifo)
# f_init=models.Moffat2D(amplitude=4200, x_0=p.x, y_0=p.y, gamma=6, alpha=1 )

fit_g=fitting.LevMarLSQFitter()   # Inizializzo il fitter: Levenberg-Marquardt

y,x=mgrid[ p.y-p.box//2:p.y+p.box//2, p.x-p.box//2:p.x+p.box//2 ]
with warnings.catch_warnings():     # Faccio il fit
    warnings.simplefilter('ignore') # Ignore model linearity warning from the fitter
    f_fit = fit_g(f_init, x, y, ima)

try:
    f_fit.theta_0  =  degrees(f_fit.theta_0)  # Trasformo in gradi
except:
    pass  # Se scommento la moffat, theta non esiste. Cosi' non si pianta.

outputjson=dict(zip(f_fit.param_names, f_fit.parameters)) # Serializza in risultato...

p.output=outputjson;
p.snr=float(hdr['STON']);
p.pscale=float(hdr['PSCALE']);

# end_time = time.time();
# p.elapsed_time =  end_time - start_time;

print (json.dumps(p.__dict__, sort_keys=True))  # ...e mostralo in un bel json
