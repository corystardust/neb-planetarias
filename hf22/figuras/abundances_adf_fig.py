import matplotlib.pyplot as plt
import astropy.io.fits as fits
import numpy as np
from matplotlib.colors import LogNorm
from matplotlib.colors import LinearSegmentedColormap

# Define custom colormap
color_list = [(1, 1, 1)] + [(0, 0, 1), (0, 1, 1), (0, 1, 0), (1, 1, 0), (1, 0, 0)]  # Blanco a Rojo
cmap_name = 'custom_cmap'
newcmp = LinearSegmentedColormap.from_list(cmap_name, color_list, N=256)

# Cargar los datos de los nuevos archivos FITS
data1, header1 = fits.getdata('abundances_OIII4959cpv4_hbetapv4_sm230.fits', header=True)
data2, header2 = fits.getdata('abundances_OII4649cpv4_hbetapv4.fits', header=True)
data3, header3 = fits.getdata('oiicadf.fits',header=True)
oii_4649, header4 = fits.getdata('/Users/leslycorina/iraf/archive/hf22-nuevo/descontaminar/decomp_OII4649_perm_additional.fits', header=True)
# Definir el extent (coordenadas físicas)
extent_normal = [-30, 100, -4.32, 10.44]  # Ajusta según tus datos
num_levels = 9  # Number of contour levels (10% to 90% in 10% intervals)
contour_levels = [0+ i * 0.1 * (4.53e-18 - 0) for i in range(1, num_levels + 1)]

# Crear una figura con 2 filas y 1 columna
fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(8, 10.5), sharex=True, sharey=True)
axes[0].contour(oii_4649, levels=contour_levels, colors='black', linewidths=0.5, origin='lower',extent=extent_normal)
# Plotear la primera imagen en la primera fila
im1 = axes[0].imshow(12 + np.log10(data1), cmap=newcmp, aspect='auto', origin='lower',extent=extent_normal,vmin=7.5, vmax= 9 )

# Título y etiquetas para la primera imagen
axes[0].text(-27.5, 9,'O$^{2+}$ $\\lambda$4959/H$\\beta$', fontsize=14, bbox=dict(facecolor='white', edgecolor='none'))
axes[0].set_xlabel('v (km/s)', fontsize=14)
#axes[0].set_ylabel('Spatial Axis (arcsec)', fontsize=14)
axes[0].axhline(y=0,linewidth=0.9, color='black') 

# Plotear la segunda imagen en la segunda fila
axes[1].contour(oii_4649, levels=contour_levels, colors='black', linewidths=0.5, origin='lower',extent=extent_normal)
im2 = axes[1].imshow(12 + np.log10(data2), origin='lower', aspect='auto', cmap=newcmp,extent=extent_normal, vmin=8.8, vmax=10.4)
axes[2].contour(oii_4649, levels=contour_levels, colors='black', linewidths=0.5, origin='lower',extent=extent_normal)
im3 = axes[2].imshow(data3, cmap=newcmp, aspect='auto', origin='lower',extent=extent_normal, norm=LogNorm(vmin=1, vmax=400))

# Título y etiquetas para la segunda imagen
axes[2].set_xlabel('v (km/s)', fontsize=14)
#axes[1].set_ylabel('Spatial axis (arc sec)', fontsize=12)
axes[1].text(-27.5, 9, 'O$^{2+}$ $\\lambda$4649/H$\\beta$', fontsize=14, bbox=dict(facecolor='white', edgecolor='none'))
axes[2].text(-28, 9,'ADF O$^{2+}$', fontsize=14, bbox=dict(facecolor='white', edgecolor='none'))

axes[0].xaxis.set_tick_params(labelsize=14)
axes[2].xaxis.set_tick_params(labelsize=14)
axes[0].yaxis.set_tick_params(labelsize=14)
axes[1].yaxis.set_tick_params(labelsize=14)
axes[2].yaxis.set_tick_params(labelsize=14)
axes[1].axhline(y=0,linewidth=0.9, color='black')
for ax in axes.flat:
    #ax.invert_yaxis()           # Invertir el eje y
    ax.axhline(y=0, linewidth=0.9, color='black')  # Agregar línea horizontal
    ax.yaxis.set_ticks([-3, 0, 3, 6, 9])
fig.text(0.04, 0.5, 'Spatial axis (arc sec)', va='center', rotation='vertical', fontsize=14)
# Añadir dos barras de color (una para cada imagen)
cax1 = fig.add_axes([0.902, 0.625, 0.03, 0.255])  # Posición de la barra de color para la primera imagen
cbar1 = fig.colorbar(im1, cax=cax1)
cbar1.ax.tick_params(labelsize=14) 
cax2 = fig.add_axes([0.902, 0.368, 0.03, 0.255])  # Posición de la barra de color para la segunda imagen
cbar2 = fig.colorbar(im2, cax=cax2)
cbar2.set_ticks([9.0, 9.2, 9.4, 9.6, 9.8, 10.0, 10.2])
cbar2.ax.tick_params(labelsize=14)
cax3 = fig.add_axes([0.902, 0.11, 0.03, 0.255])  # Posición de la barra de color para la tercera imagen
cbar3 = fig.colorbar(im3, cax=cax3)
cbar3.ax.tick_params(labelsize=14)
 
# Ajustar el espacio entre subplots
fig.subplots_adjust(hspace=0.01)  # Espacio vertical entre subplots

# Guardar la figura
plt.savefig("abundanceso2++_sm230.jpg", dpi=2086/16, bbox_inches='tight')

# Mostrar la figura
plt.show()