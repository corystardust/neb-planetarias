import matplotlib.pyplot as plt
import astropy.io.fits as fits
import matplotlib.colors as colors
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

# Define custom colormap
color_list = [(1, 1, 1)] + [(0, 0, 1), (0, 1, 1), (0, 1, 0), (1, 1, 0), (1, 0, 0)]  # Blanco a Rojo
cmap_name = 'custom_cmap'
newcmp = LinearSegmentedColormap.from_list(cmap_name, color_list, N=256)

# Open the FITS files and extract the image data
# Load FITS data for OIII
data1_oiii, header1_oiii = fits.getdata('/Users/leslycorina/iraf/archive/hf22-nuevo/mapaspv4scaled/OIII3265pscaled_v4.fits', header=True)
data2_oiii, header2_oiii = fits.getdata('/Users/leslycorina/iraf/archive/hf22-nuevo/mapaspv4scaled/OIII5592pscaled_v4.fits', header=True)

extent_normal = [-30, 100, -4.32, 10.44]  # Extent en coordenadas físicas


fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(16, 3.5), sharex=True, sharey=True)

# Plot OIII images
im1_oiii = ax1.imshow((data1_oiii / 1.5e-18), cmap=newcmp, aspect='auto', vmin=0, vmax=1, extent=extent_normal, origin='lower')
im2_oiii = ax2.imshow((data2_oiii / 1.5e-18), cmap=newcmp, aspect='auto', vmin=0, vmax=1, extent=extent_normal, origin='lower')

# Ajustar la posición de la barra de color para que coincida
cax = fig.add_axes([0.902, 0.11, 0.02, 0.769])  # Posición de la barra de color
cbar = fig.colorbar(im1_oiii, cax=cax)
cbar.set_ticks([0, 0.25, 0.5, 0.75, 1])
cbar.ax.tick_params(labelsize=12)

# Etiquetas y títulos
ax1.text(-27, 8, 'O III $\\lambda$3265\n1.50e-18', fontsize=14, bbox=dict(facecolor='white', edgecolor='none'))
ax2.text(-27, 8, 'O III $\\lambda$5592\n1.50e-18', fontsize=14, bbox=dict(facecolor='white', edgecolor='none'))

# Líneas horizontales
ax1.axhline(y=0, linewidth=0.9, color='black')
ax2.axhline(y=0, linewidth=0.9, color='black')
ax1.yaxis.set_ticks([-3, 0, 3, 6, 9])

# Etiquetas de ejes
ax1.set_ylabel('Spatial axis (arc sec)', fontsize=14)
ax1.set_xlabel('v (km/s)', fontsize=14)
ax2.set_xlabel('v (km/s)', fontsize=14)
ax1.yaxis.set_tick_params(labelsize=14)
ax1.xaxis.set_tick_params(labelsize=14)
ax2.xaxis.set_tick_params(labelsize=14)

# Ajustar los espacios
fig.subplots_adjust(wspace=0.04)  # Espacio entre subplots

# Guardar figura
plt.savefig("OIII_3265_5592_norm.jpg", dpi=2086/16, bbox_inches='tight')

# Mostrar la figura
plt.show()
