import matplotlib.pyplot as plt
import astropy.io.fits as fits
import matplotlib.colors as colors
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib as mpl

# Cambiar la fuente globalmente
#mpl.rcParams['font.family'] = 'sans-serif'
#mpl.rcParams['font.serif'] = ['Verdana']
#mpl.rcParams['font.size'] = 12

# Define custom colormap
color_list = [(1, 1, 1)] + [(0, 0, 1), (0, 1, 1), (0, 1, 0), (1, 1, 0), (1, 0, 0)]  # White to Red
cmap_name = 'custom_cmap'
newcmp = LinearSegmentedColormap.from_list(cmap_name, color_list, N=256)

# Load FITS data for oii
data1_sii, header1_sii = fits.getdata('/Users/leslycorina/iraf/archive/hf22-nuevo/SII6730pv4_flat.fits', header=True)
data2_sii, header2_sii = fits.getdata('/Users/leslycorina/iraf/archive/hf22-nuevo/SII6716pv4_flat.fits', header=True)
data3_sii, header3_sii = fits.getdata('nSII6730_6716_sinflat.fits', header=True)

# Load FITS data for sii
data1_oiir, header1_oii = fits.getdata('/Users/leslycorina/iraf/archive/hf22-nuevo/mapaspv5_sinflat_sinflujocorr/OII3729pv5_sincosmicos.fits', header=True)
data1_oii=data1_oiir*1.03
data2_oii, header2_oii = fits.getdata('/Users/leslycorina/iraf/archive/hf22-nuevo/mapaspv4scaled/OII3726pscaled_v4.fits', header=True)
data3_oii, header3_oii = fits.getdata('nOII3729_3726redcorrpv4.fits', header=True)

extent_normal = [-30, 100, -4.32, 10.44]  # Extent in physical coordinates

# Create a figure with six subplots (3 rows, 2 columns)
fig, axes = plt.subplots(nrows=3, ncols=2, figsize=(14, 10), sharex=True, sharey=True)


# Plot sii images
im1_sii = axes[0, 0].imshow((data1_sii / 1.5e-17), cmap=newcmp, aspect='auto', vmin=0, vmax=1, extent=extent_normal, origin='lower')
im2_sii = axes[1, 0].imshow((data2_sii / 1.5e-17), cmap=newcmp, aspect='auto', vmin=0, vmax=1, extent=extent_normal, origin='lower')
im3_sii = axes[2, 0].imshow(data3_sii, cmap=newcmp, aspect='auto', vmin=0, vmax=3000, extent=extent_normal, origin='lower')

# Plot oii images
im1_oii = axes[0, 1].imshow((data1_oii / 1e-17), cmap=newcmp, aspect='auto', vmin=0, vmax=1, extent=extent_normal, origin='lower')
im2_oii = axes[1, 1].imshow((data2_oii / 1.5e-17), cmap=newcmp, aspect='auto', vmin=0, vmax=1, extent=extent_normal, origin='lower')
im3_oii = axes[2, 1].imshow(data3_oii, cmap=newcmp, aspect='auto', vmin=0, vmax=3000, extent=extent_normal, origin='lower')

# Add contours for sii
contour_levels_sii = np.linspace(0, 1.5e-17, 10)
contour_levels2_sii = np.linspace(0, 1.5e-17, 10)
axes[0, 0].contour(data1_sii, levels=contour_levels_sii, colors='black', linewidths=0.5, extent=extent_normal, origin='lower')
axes[1, 0].contour(data2_sii, levels=contour_levels2_sii, colors='black', linewidths=0.5, extent=extent_normal, origin='lower')
axes[2, 0].contour(data2_sii, levels=contour_levels2_sii, colors='black', linewidths=0.5, extent=extent_normal, origin='lower')

# Add contours for oii
contour_levels_oii = np.linspace(0, 1e-17, 10)
contour_levels2_oii = np.linspace(0, 1.5e-17, 10)
axes[0, 1].contour(data1_oii, levels=contour_levels_oii, colors='black', linewidths=0.5, extent=extent_normal, origin='lower')
axes[1, 1].contour(data2_oii, levels=contour_levels2_oii, colors='black', linewidths=0.5, extent=extent_normal, origin='lower')
axes[2, 1].contour(data2_oii, levels=contour_levels2_oii, colors='black', linewidths=0.5, extent=extent_normal, origin='lower')


# Titles, labels, and annotations
axes[0, 0].text(-27.5, 7.5, '[S II] $\\lambda$6731\n1,5e-17', fontsize=14, bbox=dict(facecolor='white', edgecolor='none'))
axes[1, 0].text(-27.5, 7.5, '[S II] $\\lambda$6716\n1.5e-17', fontsize=14, bbox=dict(facecolor='white', edgecolor='none'))
axes[2, 0].text(-27.5, 9, 'n$_e$ [S II]', fontsize=14, bbox=dict(facecolor='white', edgecolor='none'))
axes[0, 1].text(-27.5, 7.5, '[O II] $\\lambda$3729\n1e-17', fontsize=14, bbox=dict(facecolor='white', edgecolor='none'))
axes[1, 1].text(-27.5, 7.5, '[O II] $\\lambda$3726\n1.5e-17', fontsize=14, bbox=dict(facecolor='white', edgecolor='none'))
axes[2, 1].text(-27.5, 9, 'n$_e$ [O II]', fontsize=14, bbox=dict(facecolor='white', edgecolor='none'))

# Set labels and ticks
axes[2, 0].set_xlabel('v (km/s)', fontsize=14)
axes[2, 1].set_xlabel('v (km/s)', fontsize=14)
axes[1, 0].set_ylabel('Spatial axis (arc sec)', fontsize=14)
axes[0, 0].yaxis.set_tick_params(labelsize=14)
axes[1, 0].yaxis.set_tick_params(labelsize=14)
axes[2, 0].yaxis.set_tick_params(labelsize=14)
axes[2, 0].xaxis.set_tick_params(labelsize=14)
axes[2, 1].xaxis.set_tick_params(labelsize=14)
for ax in axes.flat:
    ax.axhline(y=0, linewidth=0.9, color='black')
    ax.yaxis.set_ticks([-3, 0, 3, 6, 9])
# Add colorbars
cax1 = fig.add_axes([0.902, 0.37, 0.02, 0.51])
cbar1 = fig.colorbar(im1_oii, cax=cax1)
cbar1.set_ticks([0, 0.25, 0.5, 0.75, 1])
cbar1.ax.tick_params(labelsize=14)

cax2 = fig.add_axes([0.902, 0.11, 0.02, 0.254])
cbar2 = fig.colorbar(im3_oii, cax=cax2)
cbar2.set_ticks([400,1200, 2000, 2800])
cbar2.ax.tick_params(labelsize=14)

# Adjust layout for spacing
fig.subplots_adjust(hspace=0.01, wspace=0.04)

# Save and show
plt.savefig("ne_cel-hf22.jpg", dpi=2086/16, bbox_inches='tight')
plt.show()