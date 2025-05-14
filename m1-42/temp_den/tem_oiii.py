import astropy
import numpy as np
import matplotlib
import scipy
import pyneb as pn
from astropy.io import fits
import matplotlib.pylab as plt

# Este programa es para calcular temperatura a partir de los cocientes de las lineas de emision
imagen1 = fits.open('/Users/leslycorina/iraf/archive/m1-42/abundancias/OIII4363nscpv4_hbetapv4.fits')  # abrimos la imagen a analizar
datos1 = imagen1[0].data  # guardamos los datos 
header1 = imagen1[0].header  # abrimos el header

imagen2 = fits.open('/Users/leslycorina/iraf/archive/m1-42/abundancias/OIII4959nscpv4_hbetapv4.fits')
datos2 = imagen2[0].data  # guardamos los datos 
header2 = imagen2[0].header  # abrimos el header

datos= datos1/datos2

O3 = pn.Atom('O', 3)
nr = datos.shape[0]  # guardamos el número de filas
nf = datos.shape[1]  # número de columnas
ratio = np.zeros(shape=(nr, nf))  # declaramos una matriz de ceros con 39 filas y 140 columnas

# Ahora hay que realizar un bucle que calcule la temperatura en cada fila y columna y lo guarde en la matriz de ceros
for i in range(nr):
    for j in range(nf):
        Ntemp = O3.getTemDen(int_ratio=datos[i, j], den=1e3, wave1=4363, wave2=4959)
        ratio[i, j] = Ntemp

print('Habemus mapita PV')

nii = fits.PrimaryHDU()
nii.data = ratio
nii.writeto("tem_4363c_4959c.fits", overwrite=True)


