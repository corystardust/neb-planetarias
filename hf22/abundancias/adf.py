import astropy
import numpy as np
import matplotlib.pyplot as plt  
import scipy
import pyneb as pn
from mpl_toolkits.axes_grid1 import make_axes_locatable
from astropy.io import fits
from matplotlib.colors import LogNorm
import time
from matplotlib.colors import LinearSegmentedColormap
inicio = time.time()

color_list = [(1, 1, 1)] + [(0, 0, 1), (0, 1, 1), (0, 1, 0), (1, 1, 0), (1, 0, 0)]  # Blanco a Rojo
cmap_name = 'custom_cmap'
newcmp = LinearSegmentedColormap.from_list(cmap_name, color_list, N=256)


imagen1 = fits.open('abundances_OII4649cpv4_hbetapv4.fits')  #abrimos la imagen a analizar
datos1 = imagen1[0].data  # guardamos los datos 
header1 = imagen1[0].header  # abrimos el header

imagen2 = fits.open('abundances_OIII4959cpv4_hbetapv4.fits')
datos2 = imagen2[0].data  # guardamos los datos 
header2 = imagen2[0].header  # abrimos el header

datos= datos1/datos2

extent_normal = [-30,100,-12,29] # Extent en coordenadas físicas

print(datos[24,60])

imf = fits.PrimaryHDU()
imf.data = datos
imf.writeto('oii_adf.fits', overwrite=True)


fig, ax = plt.subplots(figsize=(8,3.5))

# Mostrar la imagen con escala logarítmica
im = ax.imshow(datos, cmap=newcmp, aspect='auto', origin='lower',extent=extent_normal, norm=LogNorm(vmin=1, vmax=400))

# Crear un eje extra para la barra de color usando make_axes_locatable
cax = fig.add_axes([0.902, 0.106, 0.03, 0.773])  # Posición de la barra de color para la primera imagen
cbar = fig.colorbar(im, cax=cax)
cbar.ax.tick_params(labelsize=12)
#divider = make_axes_locatable(ax)
#cax = divider.append_axes("right", size="3%", pad=0.02)  # Ajustar tamaño y separación

# Agregar la barra de color al nuevo eje
cbar = fig.colorbar(im, cax=cax)
#cbar.set_label('ADF')

# Agregar título y etiquetas
#ax.set_title('ADF O$^{++}$')
ax.xaxis.set_tick_params(labelsize=14)
ax.yaxis.set_tick_params(labelsize=14)
ax.text(-28, 24,'ADF O$^{2+}$', fontsize=14, bbox=dict(facecolor='white', edgecolor='none'))
ax.set_xlabel('v (km/s)',fontsize=14)
ax.set_ylabel('Spatial axis (arc sec)', fontsize=14)
ax.axhline(y=0,linewidth=0.9, color='black')  

# Guardar la figura
plt.savefig("adf_4649_4959.png", dpi=2086/16, bbox_inches='tight')

# Mostrar la imagen
plt.show()

# Temporizador final
fin = time.time()
print(f"Tiempo de ejecución: {fin-inicio:.2f} segundos")
