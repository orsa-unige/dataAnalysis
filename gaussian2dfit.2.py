import matplotlib.pyplot as plt
import numpy as np

from astropy.modeling.models import Gaussian2D

#cov_matrix=None,

f=Gaussian2D(amplitude=100, x_mean=0, y_mean=0, x_stddev=10, y_stddev=30, theta=np.pi/6)
y, x = np.mgrid[-120:120, -180:180]

ima=f(x,y)

fig,ax=plt.subplots()
ax.imshow(ima,origin='lower',vmin=0,vmax=0.1*ima.max())

fig.savefig("fig1a.png")

