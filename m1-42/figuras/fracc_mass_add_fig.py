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
data1, header1 = fits.getdata('relmass_fractional_mass_n++_additional_plasma_comp_temo3.fits', header=True)
data2, header2 = fits.getdata('relmass_fractional_mass_additional_plasma_comp_temo3.fits', header=True)
oii_4649, header4 = fits.getdata('/Users/leslycorina/iraf/archive/m1-42/descontaminar/decomp_OII4649_perm_additional.fits', header=True)

extent_normal = [-165,-35,-24,24] # Extent en coordenadas físicas

num_levels = 9  # Number of contour levels (10% to 90% in 10% intervals)
contour_levels = [0+ i * 0.1 * (8e-17 - 0) for i in range(1, num_levels + 1)]

# Create a figure with two subplots arranged horizontally
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 3.5), sharey=True, sharex=True) #gridspec_kw={'width_ratios': [1, 1]})

# Plotting
ax1.contour(oii_4649, levels=contour_levels, colors='black', linewidths=0.5, origin='lower',extent=extent_normal)
im1 = ax1.imshow(data1, cmap=newcmp, aspect='auto', vmin=0, vmax=1, extent=extent_normal, origin='lower')
ax2.contour(oii_4649, levels=contour_levels, colors='black', linewidths=0.5, origin='lower',extent=extent_normal)
im2 = ax2.imshow(data2, cmap=newcmp, aspect='auto', vmin=0, vmax=1, extent=extent_normal, origin='lower')


# Add a colorbar to the figure with limits set to the data range of the first two subplots
cax = fig.add_axes([0.902, 0.11, 0.02, 0.769])  # Posición de la barra de color
cbar = fig.colorbar(im1, cax=cax)
cbar.ax.tick_params(labelsize=12)

for ax in ax1,ax2:
    ax.axhline(y=0, linewidth=0.9, color='black')
    ax.set_ylim(-20, 20)
    ax.yaxis.set_ticks([-15,-10, -5, 0, 5, 10, 15])


# Set titles for the subplots
ax1.text(-162, 16,'N$^{2+}$', fontsize=14, bbox=dict(facecolor='white', edgecolor= 'none'))
ax2.text(-162, 16,'O$^{2+}$', fontsize=14, bbox=dict(facecolor='white', edgecolor='none'))

ax1.set_ylabel('Spatial axis (arc sec)', fontsize=14)
ax1.set_xlabel('v (km/s)', fontsize=14)
ax2.set_xlabel('v (km/s)', fontsize=14)
ax1.yaxis.set_tick_params(labelsize=14)
ax1.xaxis.set_tick_params(labelsize=14)
ax2.xaxis.set_tick_params(labelsize=14)
# Adjust the spacing between subplots and colorbar
fig.subplots_adjust(wspace=0.04)

# Save the figure
plt.savefig("fracc-mass-add_temo3.png", dpi=2086/16, bbox_inches='tight')
# Show the figure
plt.show()