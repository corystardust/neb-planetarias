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
#Importamos el mapa de temperatura y el mapa convolucionado
temp= fits.open('/Users/leslycorina/iraf/archive/hf22-nuevo/hf22temp_4363c_4959c_pv4.fits')
tem_oiii= temp[0].data
temp_header= temp[0].header
extent_normal = [-30,100,-12,29] # Extent en coordenadas físicas

temp_oiii = np.nan_to_num(tem_oiii, nan=0.0)

imagen = fits.open('OIII4959cpv4_hbetapv4.fits')
datos= imagen[0].data
header= imagen[0].header
#Importamos datos atomicos con pyneb
O3 = pn.Atom('O', 3)
nr = datos.shape[0]  # guardamos el número de filas
nf = datos.shape[1]  # número de columnas
ionabun = np.zeros(shape=(nr, nf)) 

# Ahora hay que realizar un bucle que calcule la temperatura en cada fila y columna y lo guarde en la matriz de ceros
for i in range(nr):
    for j in range(nf):
        abundance = O3.getIonAbundance(int_ratio=datos[i, j], tem=temp_oiii[i,j], den=1000., wave=4959, Hbeta=1.)
        ionabun[i, j] = abundance


print('Habemus mapita PV')

# Graficar el mapa de abundancias en escala logarítmica
fig, ax = plt.subplots(figsize=(8,4))

# Mostrar la imagen con escala logarítmica 12 + log10
im = ax.imshow(12 + np.log10(ionabun), cmap=newcmp, aspect='auto', origin='lower',extent=extent_normal,vmin=7.5, vmax= 9 )

# Crear un eje extra para la barra de color
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="3%", pad=0.02)

# Agregar la barra de color
cbar = fig.colorbar(im, cax=cax)
#cbar.set_label('O$^{2+}$/H$^{+}$')

# Agregar título y etiquetas a los ejes
#ax.set_title('O$^{2+}$ CEL')
ax.text(-27, 24,'O$^{2+}$ $\\lambda$4959/H$\\beta$', fontsize=12, bbox=dict(facecolor='white'))
ax.set_xlabel('V (km/s)')
ax.set_ylabel('Spatial Axis (arcsec)')
ax.axhline(y=0,linewidth=0.9, color='black')  

# Guardar la figura
plt.savefig("abundances_OIII4959cpv4_hbetapv4.png", dpi=180, overwrite=True)

# Mostrar la figura
plt.show()

# Guardar el mapa de abundancias en un archivo FITS
imf = fits.PrimaryHDU()
imf.data = ionabun
imf.writeto("abundances_OIII4959cpv4_hbetapv4.fits", overwrite=True)

# Temporizador final
fin = time.time()
print(f"Tiempo de ejecución: {fin-inicio:.2f} segundos")
