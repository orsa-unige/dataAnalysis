

from sys import argv
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from scipy.optimize import leastsq

def gaussian(amplitude, center_x, center_y, sigma_x, sigma_y, deg, offset):
    """Returns a gaussian function with the given parameters"""
    sigma_x = float(sigma_x)
    sigma_y = float(sigma_y)
    theta = deg / 360. * 2 * np.pi
    a = (np.cos(theta)**2)/(2*sigma_x**2) + (np.sin(theta)**2)/(2*sigma_y**2)
    b = (np.sin(2*theta))/(4*sigma_x**2) - (np.sin(2*theta))/(4*sigma_y**2)
    c = (np.sin(theta)**2)/(2*sigma_x**2) + (np.cos(theta)**2)/(2*sigma_y**2)
    return lambda x,y: offset + amplitude*np.exp(- (a*((center_x-x)**2)
        + c*((center_y-y)**2) - 2*b*(center_x-x)*(center_y-y)))

def moments(data):
    """Returns (height, x, y, width_x, width_y, theta)
    the gaussian parameters of a 2D distribution by calculating its
    moments """
    total = data.sum()
    X, Y = np.indices(data.shape)
    x = (X*data).sum()/total  # mass center along x axis
    y = (Y*data).sum()/total  # mass center along y axis
    col = data[:, int(y)]
    width_x = np.sqrt(np.abs((np.arange(col.size)-y)**2*col).sum()/col.sum())
    row = data[int(x), :]
    width_y = np.sqrt(np.abs((np.arange(row.size)-x)**2*row).sum()/row.sum())
    height = data.max()
    offset = np.sum(data[:, 0])/(X.shape[0])
    deg=0.   
    return height, x, y, np.abs(width_x), np.abs(width_y), deg%360, offset

def fitgaussian(data, shift):
    """Returns (height, x, y, width_x, width_y)
    the gaussian parameters of a 2D distribution found by a fit"""
    params = moments(data)
    errorfunction = lambda p: np.ravel(gaussian(*p)(*np.indices(data.shape))-data)
    p, success = leastsq(errorfunction, params)
    return p

def main(argv):

    fitsname = argv[1]
    fitsfile = fits.open(fitsname)
    image = fitsfile["PRIMARY"].data
    plt.imshow(image); plt.colorbar()
    plt.show()
    plt.close()

    posy = int(input("enter x you see on the plot: "))
    posx = int(input("enter y you see on the plot: "))
    box = int(input("enter box edge: "))

    fitsfile.close()

    if (box > posx) or (box > posy) or (box < 1) or (posx < 1) or (posy < 1):
        raise ValueError("input error")

    x, y = np.mgrid[0:box, 0:box]
    data = image[posx-box//2:posx+box//2, posy-box//2:posy+box//2]
    params = fitgaussian(data, shift=[posx-box//2, posy-box//2])

    fit = gaussian(*params)
    plt.imshow(data)
    plt.contour(fit(*np.indices(data.shape)), cmap=plt.cm.copper)
    ax = plt.gca()
    plt.show()
    paramsname = ["amplitude", "x0", "y0", "sigmax",
        "sigmay", "angle", "offset"]
    dictionary=dict()
    for idxp, p in enumerate(paramsname):
        if(idxp) == 1:
            dictionary[p] = params[idxp] + posx - box//2
        elif(idxp) == 2:
            dictionary[p] = params[idxp] + posy - box//2
        else:
            dictionary[p] = params[idxp]
            
    print(dictionary)

if __name__ == '__main__':
    main(argv)
