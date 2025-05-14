import astropy
import numpy as np
import matplotlib
import scipy
import pyneb as pn
from astropy.io import fits
import matplotlib.pylab as plt
# Este programa es para calcular temperatura a partir de los cocientes de las lineas de emision
imagen1 = fits.open('/Users/leslycorina/iraf/archive/hf22-nuevo/descontaminar/nii5755collpv4.fits')  # abrimos la imagen a analizar
datos1 = imagen1[0].data  # guardamos los datos 
header1 = imagen1[0].header  # abrimos el header

imagen2 = fits.open('/Users/leslycorina/iraf/archive/hf22-nuevo/descontaminar/nii6583coll_noflat_pv4.fits')
datos2 = imagen2[0].data  # guardamos los datos 
header2 = imagen2[0].header  # abrimos el header

#cociente de líneas
datos= datos1/datos2

#importamos datos atomicos de pyneb
N2 = pn.Atom('N', 2)
nr = datos.shape[0]  # guardamos el número de filas
nf = datos.shape[1]  # número de columnas
ratio = np.zeros(shape=(nr, nf))  # declaramos una matriz de ceros con 39 filas y 140 columnas

# Ahora hay que realizar un bucle que calcule la temperatura en cada fila y columna y lo guarde en la matriz de ceros
for i in range(nr):
    for j in range(nf):
        Ntemp = N2.getTemDen(int_ratio=datos[i, j], den=1e3, wave1=5755, wave2=6584)
        ratio[i, j] = Ntemp

print('Habemus mapita PV')

nii = fits.PrimaryHDU()
nii.data = ratio
nii.writeto("hf22temp_5755_6583_flat_pv4.fits", overwrite=True)
