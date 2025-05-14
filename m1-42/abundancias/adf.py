import astropy
import numpy as np
import matplotlib.pyplot as plt  # Cambiar a pyplot en lugar de pylab
import scipy
import pyneb as pn
from mpl_toolkits.axes_grid1 import make_axes_locatable
from astropy.io import fits
from matplotlib.colors import LogNorm
import time
from matplotlib.colors import LinearSegmentedColormap

color_list = [(1, 1, 1)] + [(0, 0, 1), (0, 1, 1), (0, 1, 0), (1, 1, 0), (1, 0, 0)]  # Blanco a Rojo
cmap_name = 'custom_cmap'
newcmp = LinearSegmentedColormap.from_list(cmap_name, color_list, N=256)

imagen1 = fits.open('abundances_OII4649cpv4_Hbetapnsv4.fits')  #abrimos la imagen a analizar
datos1 = imagen1[0].data  # guardamos los datos 
header1 = imagen1[0].header  # abrimos el header

imagen2 = fits.open('abundances_OIII5007nsv4_hbetapnsv4.fits')
datos2 = imagen2[0].data  # guardamos los datos 
header2 = imagen2[0].header  # abrimos el header
extent_normal = [-165,-35,-24,24] # Extent en coordenadas físicas


datos= datos1/datos2

imf = fits.PrimaryHDU()
imf.data = datos
imf.writeto('oiiadf.fits', overwrite=True)

fig, ax = plt.subplots(figsize=(8,3.5))

# Mostrar la imagen con escala logarítmica
im = ax.imshow(datos,cmap=newcmp, aspect='auto', extent=extent_normal, origin='lower', norm=LogNorm(vmin=1, vmax=150))

# Crear un eje extra para la barra de color usando make_axes_locatable
cax = fig.add_axes([0.902, 0.106, 0.03, 0.773])  # Posición de la barra de color para la primera imagen
cbar = fig.colorbar(im, cax=cax)
cbar.ax.tick_params(labelsize=12)
ax.xaxis.set_tick_params(labelsize=14)
ax.yaxis.set_tick_params(labelsize=14)
# Agregar título y etiquetas
ax.text(-163,16,'ADF O$^{2+}$', fontsize=14, bbox=dict(facecolor='white', edgecolor='none'))
#ax.set_title('ADF O$^{++}$ (add)')
ax.set_xlabel('v (km/s)', fontsize=14)
ax.set_ylabel('Spatial axis (arc sec)', fontsize=14)
ax.axhline(y=0,linewidth=0.9, color='black')  
ax.set_ylim(-20, 20)
ax.yaxis.set_ticks([-15,-10, -5, 0, 5, 10, 15])
# Guardar la figura
#plt.savefig("adfo++.png", dpi=2086/16, bbox_inches='tight')

# Mostrar la imagen
plt.show()
