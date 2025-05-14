import astropy
import numpy as np
import matplotlib
import scipy
import pyneb as pn
from astropy.io import fits
import matplotlib.pylab as plt
# Este programa es para calcular temperatura a partir de los cocientes de las lineas de emision
imagen1 = fits.open('/Users/leslycorina/iraf/archive/m1-42/SII6716pv4_flat.fits')  # abrimos la imagen a analizar
datos1 = imagen1[0].data  # guardamos los datos 
header1 = imagen1[0].header  # abrimos el header

imagen2 = fits.open('/Users/leslycorina/iraf/archive/m1-42/SII6730pv4_flat.fits')
datos2 = imagen2[0].data  # guardamos los datos 
header2 = imagen2[0].header  # abrimos el header

datos= datos1/datos2
S2 = pn.Atom('S',2)

nr = datos.shape[0] #guardamos el numero de filas
nf = datos.shape[1] #numero de columnas
print (nr)
print (nf)
ratio = np.zeros(shape=(nr,nf)) #declaramos una matriz de ceros con 39 filas y 140 columnas
#Ahora hay que realizar un bucle que calcule la temperatura en cada fila y columna y lo guarde en la matriz de ceros
for i in range(nr):
	for j in range(nf):
		Ntemp=S2.getTemDen(int_ratio=datos[i,j], tem=1e4, wave1=6716, wave2=6731)
		ratio[i,j] = Ntemp

print('terminó')
nii = fits.PrimaryHDU()
nii.data = np.arange(nr,nf)
nii.data = ratio
nii.writeto("Ne_SII6716_6730_flatpv4.fits")


