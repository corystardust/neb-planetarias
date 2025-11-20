import matplotlib.pyplot as plt
import astropy.io.fits as fits
import matplotlib.colors as colors
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

color_list = [(1, 1, 1)] + [(0, 0, 1), (0, 1, 1), (0, 1, 0), (1, 1, 0), (1, 0, 0)]  # Blanco a Rojo
cmap_name = 'custom_cmap'
newcmp = LinearSegmentedColormap.from_list(cmap_name, color_list, N=256)

# Open the FITS files and extract the image data
data1, header1 = fits.getdata('/Users/leslycorina/iraf/archive/m1-42/mapaspv4scaled_redcorr/OIII3265pv4fluxredcorr_pyneb.fits', header=True)
data2, header2 = fits.getdata('/Users/leslycorina/iraf/archive/m1-42/mapaspv4scaled_redcorr/OIII5592pv4fluxredcorr_pyneb.fits', header=True)

extent_normal = [-165,-35,-24,24] # Extent en coordenadas físicas


# Create a figure with two subplots arranged horizontally
fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(16, 3.5), sharex=True, sharey=True)

# Plotting
im1 = ax1.imshow(data1/8e-17, cmap=newcmp, aspect='auto', vmin=0, vmax=1, extent=extent_normal, origin='lower')
im2 = ax2.imshow(data2/8e-17, cmap=newcmp, aspect='auto', vmin=0, vmax=1, extent=extent_normal, origin='lower')

# Ajustar la posición de la barra de color para que coincida
cax = fig.add_axes([0.902, 0.11, 0.02, 0.769])  # Posición de la barra de color
cbar = fig.colorbar(im1, cax=cax)
cbar.set_ticks([0, 0.25, 0.5, 0.75, 1])
cbar.ax.tick_params(labelsize=12)


# Set titles for the subplots
ax1.text(-163, 13,'O III $\\lambda$3265\n8.0e-17', fontsize=14, bbox=dict(facecolor='white', edgecolor='none'))
ax2.text(-163, 13,'O III $\\lambda$5592\n8.0e-17', fontsize=14, bbox=dict(facecolor='white', edgecolor='none'))
ax1.axhline(y=0,linewidth=0.9, color='black')  
ax2.axhline(y=0,linewidth=0.9, color='black')  

for ax in ax1,ax2:
    ax.axhline(y=0, linewidth=0.9, color='black')
    ax.set_ylim(-20, 20)
    ax.yaxis.set_ticks([-15,-10, -5, 0, 5, 10, 15])
    ax.xaxis.set_tick_params(labelsize=14)
    ax.yaxis.set_tick_params(labelsize=14)

# Etiquetas de ejes
ax1.set_ylabel('Spatial axis (arc sec)', fontsize=14)
ax1.set_xlabel('v (km/s)', fontsize=14)
ax2.set_xlabel('v (km/s)', fontsize=14)


# Ajustar los espacios
fig.subplots_adjust(wspace=0.04)  # Espacio entre subplots

# Guardar figura
plt.savefig("OIII_3265_5592_norm.jpg", dpi=2086/16, bbox_inches='tight')
# Show the figure
plt.show()