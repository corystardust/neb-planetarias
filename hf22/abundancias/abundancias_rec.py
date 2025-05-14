import astropy
import numpy as np
import matplotlib.pyplot as plt 
import scipy
from mpl_toolkits.axes_grid1 import make_axes_locatable
import pyneb as pn
from astropy.io import fits
from matplotlib.colors import LogNorm
import time
from matplotlib.colors import LinearSegmentedColormap

color_list = [(1, 1, 1)] + [(0, 0, 1), (0, 1, 1), (0, 1, 0), (1, 1, 0), (1, 0, 0)]  # Blanco a Rojo
cmap_name = 'custom_cmap'
newcmp = LinearSegmentedColormap.from_list(cmap_name, color_list, N=256)

inicio = time.time()

imagen = fits.open('OII4649cpv4_hbetapv4.fits')
datos= imagen[0].data
header= imagen[0].header

extent_normal = [-30,100,-12,29] # Extent en coordenadas físicas


O2 = pn.RecAtom('O', 2)
nr = datos.shape[0]  # guardamos el número de filas
nf = datos.shape[1]  # número de columnas
ionabun = np.zeros(shape=(nr, nf)) 

# Ahora hay que realizar un bucle que calcule la temperatura en cada fila y columna y lo guarde en la matriz de ceros
for i in range(nr):
    for j in range(nf):
        abundance = O2.getIonAbundance(int_ratio=datos[i, j], tem=2000, den=5000., wave=4649.13, Hbeta=1.)
        ionabun[i, j] = abundance


print('Habemus mapita PV')

# Graficar el mapa de abundancias en escala logarítmica
# Crear la figura y los ejes
fig, ax = plt.subplots(figsize=(8,4))

# Mostrar la imagen con escala logarítmica
im = ax.imshow(12 + np.log10(ionabun), origin='lower', aspect='auto', cmap=newcmp,extent=extent_normal, vmin=9, vmax=10.5)

# Crear un eje extra para la barra de color usando make_axes_locatable
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="3%", pad=0.02)  # Ajustar tamaño y separación

# Agregar la barra de color al nuevo eje
cbar = fig.colorbar(im, cax=cax)
#cbar.set_label('O$^{++}$/H$^{+}$')

# Agregar título y etiquetas
ax.text(-25, 24,'O$^{2+}$ $\\lambda$4649/H$\\beta$', fontsize=12, bbox=dict(facecolor='white'))
ax.set_xlabel('V (km/s)')
ax.set_ylabel('Spatial axis (arc sec)')
ax.axhline(y=0,linewidth=0.9, color='black')  
# Guardar la figura
plt.savefig("abundances_OII4649cpv4_hbetapv4.png", dpi=180, overwrite=True)

# Mostrar la imagen
plt.show()

imf = fits.PrimaryHDU()
imf.data = ionabun
imf.writeto("abundances_OII4649cpv4_hbetapv4.fits", overwrite=True)

fin = time.time()
print(fin-inicio)
