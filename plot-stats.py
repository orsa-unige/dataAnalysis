#!/usr/bin/env python3

# Devi fare
#
#   chmod +x questo-file.py
# 
# Provalo dalla console cosi':
# python ./script-python.py '"{\"num1\":\"1.2\",\"num2\":\"1\",\"txt\":\"asd\"}"'
#!/usr/bin/env python3

import sys, json, warnings
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy.modeling import models, fitting
from scipy.optimize import curve_fit

try:
    lines = sys.stdin.readlines();
    inputjson=lines[0];
except:
    print ("ERROR: no data or bad data format provided. Try:")

class input_parameters(object):   # Metto tutto il JSON in un oggetto Python
    def __init__(self, inputjson):
        self.__dict__ = json.loads(inputjson)

p = json.loads(inputjson)

#plt.figure(figsize=(8, 4))

pltscale=0.205

magarr=[]
snrarr=[]
stdarx=[]
stdary=[]
rmsarr=[]

circarr=[]

for i,v in enumerate(p) :
    magarr.append( p[i]['mag'] )
    snrarr.append( p[i]['snr'] )
    stdarx.append( (np.std(p[i]['x_mean_arr'])) )
    stdary.append( (np.std(p[i]['y_mean_arr'])) )
    rmsarr.append( np.sqrt(np.mean(np.square(p[i]['err_vector']))) )

fig,ax=plt.subplots()

ax.scatter(magarr, [x*pltscale for x in stdarx], label='stdev x 1σ')
ax.scatter(magarr, [x*pltscale for x in stdary], label='stdev y 1σ')
ax.scatter(magarr, [x*pltscale for x in rmsarr], label='rms ')

for i,j,k in zip(magarr,[x*pltscale for x in rmsarr],snrarr):
    ax.annotate(str(k),xy=(i,j), xytext=(10,10), textcoords='offset points')

ax.axhline(0.1)

ax.legend()

plt.title("Fitted position for 100 simulated G5V type star as a function of magnitude")
plt.xlabel("V mag")
plt.ylabel("Stdev [arcsec]")

plt.show()

# plt.title("Fit of simulated G0V stars with 16.5<m_v<19.0. 100 stars per magnitude. Circles: stdev at the 2σ level")
# plt.xlabel("px")
# plt.ylabel("px")

#plt.xlim([10.6,20.4])
#plt.ylim([10.6,20.4])

# fig, ax = plt.subplots() # note we must use plt.subplots, not plt.subplot
# (or if you have an existing figure)
# fig = plt.gcf()
# ax = fig.gca()
    
    # circarr.append(plt.Circle((np.mean(p[i]['x_mean_arr']), np.mean(p[i]['y_mean_arr'])),
    #                  2*stdarr[i], alpha=0.4, color='blue', fill=False) )
    # plt.scatter(p[i]['x_mean_arr'], p[i]['y_mean_arr'], alpha=0.4,
    #             label='m_v={:.1f}, diam={:.3f} arcsec'.format(p[i]['mag'], stdarr[i]*pltscale*2))
    # ax.add_artist(circarr[i])
#    print(magarr)
    

# p=input_parameters(inputjson)     # Ecco i dati in un comodo oggetto

# print (json.dumps(p.__dict__, sort_keys=True))  # ...e mostralo in un bel json
