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
data1, header1 = fits.getdata('relmass_fractional_mass_n++_additional_plasma_comp.fits', header=True)
data2, header2 = fits.getdata('relmass_fractional_mass_additional_plasma_comp.fits', header=True)
oii_4649, header4 = fits.getdata('/Users/leslycorina/iraf/archive/hf22-nuevo/descontaminar/decomp_OII4649_perm_additional.fits', header=True)

extent_normal = [-30,100,-4.32, 10.44] # Extent en coordenadas físicas

num_levels = 9  # Number of contour levels (10% to 90% in 10% intervals)
contour_levels = [0+ i * 0.1 * (4.53e-18 - 0) for i in range(1, num_levels + 1)]

# Create a figure with two subplots arranged horizontally
fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(16, 3.5), sharey=True, sharex=True)#, gridspec_kw={'width_ratios': [1, 1]})

# Plotting
ax1.contour(oii_4649, levels=contour_levels, colors='black', linewidths=0.5, origin='lower',extent=extent_normal)
im1 = ax1.imshow(data1, cmap=newcmp, aspect='auto', vmin=0, vmax=1, extent=extent_normal, origin='lower')
ax2.contour(oii_4649, levels=contour_levels, colors='black', linewidths=0.5, origin='lower',extent=extent_normal)
im2 = ax2.imshow(data2, cmap=newcmp, aspect='auto', vmin=0, vmax=1, extent=extent_normal, origin='lower')


# Add a colorbar to the figure with limits set to the data range of the first two subplots
cax = fig.add_axes([0.902, 0.11, 0.02, 0.769])  # Posición de la barra de color
cbar = fig.colorbar(im1, cax=cax)
cbar.ax.tick_params(labelsize=14)

# Invert the y-axis of both subplots
#ax1.invert_yaxis()
#ax2.invert_yaxis()
# Set titles for the subplots
ax1.text(-27, 9,'N$^{2+}$', fontsize=14, bbox=dict(facecolor='white', edgecolor='none'))
ax2.text(-27, 9,'O$^{2+}$', fontsize=14, bbox=dict(facecolor='white', edgecolor='none'))
ax1.axhline(y=0,linewidth=0.9, color='black')  
ax2.axhline(y=0,linewidth=0.9, color='black')  
ax1.yaxis.set_ticks([-3, 0, 3, 6, 9])
ax2.yaxis.set_ticks([-3, 0, 3, 6, 9])

ax1.set_ylabel('Spatial axis (arc sec)', fontsize=14)
ax1.set_xlabel('v (km/s)', fontsize=14)
ax2.set_xlabel('v (km/s)', fontsize=14)
ax1.yaxis.set_tick_params(labelsize=14)
ax1.xaxis.set_tick_params(labelsize=14)
ax2.xaxis.set_tick_params(labelsize=14)
# Adjust the spacing between subplots and colorbar
fig.subplots_adjust(wspace=0.04)

# Save the figure
plt.savefig("n++_o++_rel_fracc_mass.jpg",dpi=2086/16, bbox_inches='tight')
# Show the figure
plt.show()