import matplotlib.pyplot as plt
import astropy.io.fits as fits
import matplotlib.colors as colors
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.colors import LogNorm


color_list = [(1, 1, 1)] + [(0, 0, 1), (0, 1, 1), (0, 1, 0), (1, 1, 0), (1, 0, 0)]  # Blanco a Rojo
cmap_name = 'custom_cmap'
newcmp = LinearSegmentedColormap.from_list(cmap_name, color_list, N=256)

# Open the FITS files and extract the image data
data1, header1 = fits.getdata('/Users/leslycorina/iraf/archive/m1-42/NII6583snsv4_flat_ext.fits', header=True)
data2, header2 = fits.getdata('/Users/leslycorina/iraf/archive/m1-42/OIII5007nsv4_flat_ext.fits', header=True)

extent_normal = [-220,30,-17.28,17.28] # Extent en coordenadas físicas

# Create a figure with two subplots arranged horizontally
fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(5, 6), sharex=True, sharey=True)

# Plotting
im1 = ax1.imshow(data1/7e-17, cmap=newcmp, aspect='auto', norm=LogNorm(vmin=0.0001, vmax=1), origin='lower', extent=extent_normal)
im2 = ax2.imshow(data2/2e-16, cmap=newcmp, aspect='auto', norm=LogNorm(vmin=0.0001, vmax=1), origin='lower', extent=extent_normal)

# Ajustar la posición de la barra de color para que coincida
cax = fig.add_axes([0.902, 0.11, 0.03, 0.769])  # Posición de la barra de color
cbar = fig.colorbar(im1, cax=cax)
#cbar.set_ticks([0, 0.25, 0.5, 0.75, 1])
cbar.ax.tick_params(labelsize=14)


# Set titles for the subplots
ax1.text(-215, 10,'[N II] $\\lambda$6583 UVES\n7.0e-17', fontsize=12, bbox=dict(facecolor='white', edgecolor='none'))
ax2.text(-215, 10,'[O III] $\\lambda$5007 UVES\n2.0e-16', fontsize=12, bbox=dict(facecolor='white', edgecolor='none'))
#ax1.axhline(y=0,linewidth=0.9, color='black')  
#ax2.axhline(y=0,linewidth=0.9, color='black')  

for ax in ax1,ax2:
	 #ax.set_xticks([])
	 #ax.set_yticks([])
	 #ax.axhline(y=24, linewidth=0.9, color='black')
	 #ax.set_ylim(4, 44)
	 ax.yaxis.set_ticks([-15,-10,-5, 0, 5, 10, 15])
	 ax.set_yticklabels(['-7.5', '-5', '-2.5', '0', '2.5','5','7.5'])
	 ax.xaxis.set_tick_params(labelsize=12)
	 ax.yaxis.set_tick_params(labelsize=12)


#ax.set_ylabel("'Spatial axis (arc sec)', fontsize=12")

fig.supylabel('Spatial axis (arc sec)', fontsize=14)
# Etiquetas de ejes
ax1.set_xlabel('v (km/s)', fontsize=14)
ax2.set_xlabel('v (km/s)', fontsize=14)
#ax1.axvline(x=125,linewidth=0.9,color='black') 
#ax2.axvline(x=125,linewidth=0.9,color='black') 

# Ajustar los espacios
fig.subplots_adjust(hspace=0.04)  # Espacio entre subplots

# Guardar figura
plt.savefig("nii_oiii_log_axes.jpg", dpi=2086/16, bbox_inches='tight')
# Show the figure
plt.show()