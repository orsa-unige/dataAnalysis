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

try:
    lines = sys.stdin.readlines();
    inputjson=lines[0];
except:
    print ("ERROR: no data or bad data format provided. Try:")
    print ('echo \{\"filename\":\"/home/indy/desktop/sim/v-vega/NTT15_31.fits\",\"x\":48,\"y\":47,\"box\":30\} | ./gaussian2dfit-davide.py')
    print ('You sent:')
    print (sys.stdin)
    sys.exit(1)

class input_parameters(object):   # Metto tutto il JSON in un oggetto Python
    def __init__(self, inputjson):
        self.__dict__ = json.loads(inputjson)

p = json.loads(inputjson)

# print (np.mean(p[0]['x_mean_arr']))
# print (np.mean(p[0]['y_mean_arr']))

#plt.figure(figsize=(8, 4))

std19 = (np.std(p[4]['x_mean_arr'])+np.std(p[4]['y_mean_arr']))/2
std18 = (np.std(p[3]['x_mean_arr'])+np.std(p[3]['y_mean_arr']))/2
std17 = (np.std(p[2]['x_mean_arr'])+np.std(p[2]['y_mean_arr']))/2
std16 = (np.std(p[1]['x_mean_arr'])+np.std(p[1]['y_mean_arr']))/2
std15 = (np.std(p[0]['x_mean_arr'])+np.std(p[0]['y_mean_arr']))/2

circle4 = plt.Circle((np.mean(p[4]['x_mean_arr']), np.mean(p[4]['y_mean_arr'])),
                     2*std19,
                     alpha=0.4, color='blue', fill=False)
circle3 = plt.Circle((np.mean(p[3]['x_mean_arr']), np.mean(p[3]['y_mean_arr'])),
                     2*std18,
                     alpha=0.4, color='orange', fill=False)
circle2 = plt.Circle((np.mean(p[2]['x_mean_arr']), np.mean(p[2]['y_mean_arr'])),
                     2*std17,
                     alpha=0.4, color='green', fill=False)
circle1 = plt.Circle((np.mean(p[1]['x_mean_arr']), np.mean(p[1]['y_mean_arr'])),
                     2*std16,
                     alpha=0.4, color='red', fill=False)
circle0 = plt.Circle((np.mean(p[0]['x_mean_arr']), np.mean(p[0]['y_mean_arr'])),
                     2*std15,
                     alpha=0.4, color='purple', fill=False)

pltscale=0.205

fig, ax = plt.subplots() # note we must use plt.subplots, not plt.subplot
# (or if you have an existing figure)
# fig = plt.gcf()
# ax = fig.gca()

plt.title("Fit of simulated stars with 15<m_v<19. 100 stars per magnitude. Circles: stdev at the 2σ level")
plt.xlabel("px")
plt.ylabel("px")

plt.xlim([49.6,50.4])
plt.ylim([49.6,50.4])

plt.scatter(p[4]['x_mean_arr'], p[4]['y_mean_arr'], alpha=0.4, label='m_v=19, ø=%.3f arcsec' %(2*std19*pltscale*2))
plt.scatter(p[3]['x_mean_arr'], p[3]['y_mean_arr'], alpha=0.4, label='m_v=18, ø=%.3f arcsec' %(2*std18*pltscale*2))
plt.scatter(p[2]['x_mean_arr'], p[2]['y_mean_arr'], alpha=0.4, label='m_v=17, ø=%.3f arcsec' %(2*std17*pltscale*2))
plt.scatter(p[1]['x_mean_arr'], p[1]['y_mean_arr'], alpha=0.4, label='m_v=16, ø=%.3f arcsec' %(2*std16*pltscale*2))
plt.scatter(p[0]['x_mean_arr'], p[0]['y_mean_arr'], alpha=0.4, label='m_v=15, ø=%.2f arcsec' %(2*std15*pltscale*2))

ax.add_artist(circle4)
ax.add_artist(circle3)
ax.add_artist(circle2)
ax.add_artist(circle1)
ax.add_artist(circle0)

# plt.scatter( np.mean(p[4]['x_mean_arr']), np.mean(p[4]['y_mean_arr']),)
# plt.scatter( np.mean(p[3]['x_mean_arr']), np.mean(p[3]['y_mean_arr']),)
# plt.scatter( np.mean(p[2]['x_mean_arr']), np.mean(p[2]['y_mean_arr']),)
# plt.scatter( np.mean(p[1]['x_mean_arr']), np.mean(p[1]['y_mean_arr']),)
# plt.scatter( np.mean(p[0]['x_mean_arr']), np.mean(p[0]['y_mean_arr']),)

plt.legend()
plt.show()


# p=input_parameters(inputjson)     # Ecco i dati in un comodo oggetto

# print (json.dumps(p.__dict__, sort_keys=True))  # ...e mostralo in un bel json
