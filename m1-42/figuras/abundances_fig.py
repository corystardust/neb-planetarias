import astropy
import numpy as np
import matplotlib.pyplot as plt  # Cambiar a pyplot en lugar de pylab
import scipy
from mpl_toolkits.axes_grid1 import make_axes_locatable
import pyneb as pn
from astropy.io import fits
from matplotlib.colors import LogNorm
import time

imagen = fits.open('/Users/leslycorina/iraf/archive/m1-42/abundancias/abundances_nii6583nsv4_hbetapnsv4.fits')  #abrimos la imagen a analizar
datos = imagen[0].data  # guardamos los datos 
header = imagen[0].header  # abrimos el header


# Graficar el mapa de abundancias en escala logarítmica
# Crear la figura y los ejes
fig, ax = plt.subplots()

# Mostrar la imagen con escala logarítmica
im = ax.imshow(datos, origin='lower', cmap='jet', norm=LogNorm(vmin=1e-8, vmax=1e-5))

# Crear un eje extra para la barra de color usando make_axes_locatable
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.05)  # Ajustar tamaño y separación

# Agregar la barra de color al nuevo eje
cbar = fig.colorbar(im, cax=cax)
cbar.set_label('Abundancia de [N II] (log)')

# Agregar título y etiquetas
ax.set_title('Mapa de Abundancia de [N II] 6583')
ax.set_xlabel('v')
ax.set_ylabel('posición')

# Guardar la figura
plt.savefig("abundances_NII6583nsv4_hbetapnsv4.png", dpi=300, overwrite=True)

# Mostrar la imagen
plt.show()