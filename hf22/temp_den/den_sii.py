#Este incluye una parte la corrección por enrojecimiento
import astropy
import pyneb as pn
import matplotlib
import scipy
from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np

im1=fits.open('/Users/leslycorina/iraf/archive/hf22-nuevo/SII6730pv4_flat.fits')
datos1=im1[0].data
datos1f=datos1

im2=fits.open('/Users/leslycorina/iraf/archive/hf22-nuevo/SII6716pv4_flat.fits')
datos2=im2[0].data
datos2f=datos2

#im3=fits.open('chbg.fits')
#datos3=im3[0].data

re = 41
rv = 131
     
s2 = np.zeros((41,131), dtype=float)
S2 = pn.Atom('S',2)

for i in range(re):
 for j in range(rv):
   file=open('f4.dat','w')
   file.write('LINE PN\n')
   file.write('S2_6731A\t')
   file.write('%.5E\n'%datos1f[i,j])
   file.write('S2_6716A\t')
   file.write('%.5E\n'%datos2f[i,j])
   file.close()
   obs = pn.Observation('f4.dat', fileFormat='lines_in_rows', correcLaw='F99')
#  obs.extinction.cHbeta = 0.5
   obs.extinction.E_BV=0.0
   obs.correctData()
   int1=obs.getIntens()['S2_6731A'][0]
   int2=obs.getIntens()['S2_6716A'][0]
   ratio=int1/int2
   val = S2.getTemDen(int_ratio=ratio, tem=1e4, wave1=6731, wave2 = 6716)
   s2[i,j] = val


imf = fits.PrimaryHDU()
imf.data = np.arange(41,131)
imf.data = s2
imf.writeto('nSII6730_6716_sinflat.fits')
