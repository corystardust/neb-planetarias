#Este script incluye la parte de corrección por enrojecimiento (en caso de que no se haya hecho anteriormente)
import astropy
import pyneb as pn
import matplotlib
import scipy
from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np

im1=fits.open('/Users/leslycorina/iraf/archive/hf22-nuevo/mapaspv4/OII3729pv4.fits')
datos1=im1[0].data
datos1f=datos1

im2=fits.open('/Users/leslycorina/iraf/archive/hf22-nuevo/mapaspv4/OII3726pv4.fits')
datos2=im2[0].data
datos2f=datos2

#im3=fits.open('chbg.fits')
#datos3=im3[0].data

re = 41
rv = 131
     
o2 = np.zeros((41,131), dtype=float)
O2 = pn.Atom('O',2)

for i in range(re):
 for j in range(rv):
   file=open('f4.dat','w')
   file.write('LINE PN\n')
   file.write('O2_3729A\t')
   file.write('%.5E\n'%datos1f[i,j])
   file.write('O2_3726A\t')
   file.write('%.5E\n'%datos2f[i,j])
   file.close()
   obs = pn.Observation('f4.dat', fileFormat='lines_in_rows', correcLaw='F99')
#  obs.extinction.cHbeta = 0.5
   obs.extinction.E_BV=0.0
   obs.correctData()
   int1=obs.getIntens()['O2_3729A'][0]
   int2=obs.getIntens()['O2_3726A'][0]
   ratio=int1/int2
   val = O2.getTemDen(int_ratio=ratio, tem=1e4, wave1=3729, wave2 = 3726)
   o2[i,j] = val


imf = fits.PrimaryHDU()
imf.data = np.arange(41,131)
imf.data = o2
imf.writeto('nOII3729_3726redcorrpv4.fits')
