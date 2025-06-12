import astropy
import numpy as np
import matplotlib
import scipy
import pyneb as pn
from astropy.io import fits
import matplotlib.pylab as plt
#Este programa es para calcular temperatura a partir de los cocientes de las lineas de emision
imagen=fits.open('ClIII5537_5517.fits') #abrimos la imagen a analizar
datos= imagen[0].data #guardamos los datos 
header = imagen[0].header #abrimos el header
#print (datos[5,40]) #ejemplo del valor de la fila 5 columna 40
Cl3 = pn.Atom('Cl',3)
temp = Cl3.getTemDen(int_ratio=datos[5,40], tem=1e4, wave1=5537, wave2=5517) #ejemplo de la temperatura en la fila 5 columna 4
print (temp)
nr = datos.shape[0] #guardamos el numero de filas
nf = datos.shape[1] #numero de columnas
print (nr)
print (nf)
ratio = np.zeros(shape=(nr,nf)) #declaramos una matriz de ceros con 39 filas y 140 columnas
#print (mar3)
#Ahora hay que realizar un bucle que calcule la temperatura en cada fila y columna y lo guarde en la matriz de ceros
for i in range(nr):
	for j in range(nf):
		Ntemp=Cl3.getTemDen(int_ratio=datos[i,j], tem=1e4, wave1=5537, wave2=5517)
		#print (artemp)
		ratio[i,j] = Ntemp
		#print (mar3)
		#print(i,j)
plt.imshow(ratio);#representar cada punto de la matriz graficamente

print('terminó')
nii = fits.PrimaryHDU()
nii.data = np.arange(nr,nf)
nii.data = ratio
nii.writeto("NClIII5537_5517pv8.fits")



