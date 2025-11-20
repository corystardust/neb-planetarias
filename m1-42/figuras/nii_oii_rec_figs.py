import matplotlib.pyplot as plt
import astropy.io.fits as fits
import matplotlib.colors as colors
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib as mpl
from PIL import Image

# Define custom colormap
color_list = [(1, 1, 1)] + [(0, 0, 1), (0, 1, 1), (0, 1, 0), (1, 1, 0), (1, 0, 0)]  # White to Red
cmap_name = 'custom_cmap'
newcmp = LinearSegmentedColormap.from_list(cmap_name, color_list, N=256)

# Load FITS data for nii
data1_nii, header1_nii = fits.getdata('/Users/leslycorina/iraf/archive/m1-42/NII4041pv4fluxredcorr_pyneb.fits', header=True)
data2_nii, header2_nii = fits.getdata('/Users/leslycorina/iraf/archive/m1-42/mapaspv4scaled_redcorr/NII5679pv4fluxredcorr_pyneb.fits', header=True)
data3_nii, header3_nii = fits.getdata('ratio_NII4041_5680_redcorr_pv4.fits', header=True)

# Load FITS data for oii
data1_oii, header1_oii = fits.getdata('/Users/leslycorina/iraf/archive/m1-42/mapaspv4scaled_redcorr/OII4089pv4fluxredcorr_pyneb.fits', header=True)
data2_oii, header2_oii = fits.getdata('OII4649spv4fluxredcorr_pyneb.fits', header=True)
data3_oii, header3_oii = fits.getdata('ratio_OII4089_4649_redcorr_pv4.fits', header=True)

extent_normal = [-165,-35,-8.64,8.64] # Extent en coordenadas físicas

# Create a figure with six subplots (3 rows, 2 columns)
fig, axes = plt.subplots(nrows=3, ncols=2, figsize=(16, 10.5), sharex=True, sharey=True)

# Plot nii images
im1_nii = axes[0, 0].imshow((data1_nii / 3.0e-17), cmap=newcmp, aspect='auto', vmin=0, vmax=1, extent=extent_normal, origin='lower')
im2_nii = axes[1, 0].imshow((data2_nii / 4.5e-17), cmap=newcmp, aspect='auto', vmin=0, vmax=1, extent=extent_normal, origin='lower')
im3_nii = axes[2, 0].imshow(data3_nii, cmap=newcmp, aspect='auto', vmin=0, vmax=1.25, extent=extent_normal, origin='lower')

# Plot oii images
im1_oii = axes[0, 1].imshow((data1_oii / 3e-17), cmap=newcmp, aspect='auto', vmin=0, vmax=1, extent=extent_normal, origin='lower')
im2_oii = axes[1, 1].imshow((data2_oii / 8e-17), cmap=newcmp, aspect='auto', vmin=0, vmax=1, extent=extent_normal, origin='lower')
im3_oii = axes[2, 1].imshow(data3_oii, cmap=newcmp, aspect='auto', vmin=0, vmax=1.25, extent=extent_normal, origin='lower')


# Add contours for nii
contour_levels_nii = np.linspace(0, 3e-17, 10)
contour_levels2_nii = np.linspace(0, 4.5e-17, 10)
axes[0, 0].contour(data1_nii, levels=contour_levels_nii, colors='black', linewidths=0.5, extent=extent_normal, origin='lower')
axes[1, 0].contour(data2_nii, levels=contour_levels2_nii, colors='black', linewidths=0.5, extent=extent_normal, origin='lower')
axes[2, 0].contour(data2_nii, levels=contour_levels2_nii, colors='black', linewidths=0.5, extent=extent_normal, origin='lower')

# Add contours for oii
contour_levels_oii = np.linspace(0, 3e-17, 10)
contour_levels2_oii = np.linspace(0, 8e-17, 10)
axes[0, 1].contour(data1_oii, levels=contour_levels_oii, colors='black', linewidths=0.5, extent=extent_normal, origin='lower')
axes[1, 1].contour(data2_oii, levels=contour_levels2_oii, colors='black', linewidths=0.5, extent=extent_normal, origin='lower')
axes[2, 1].contour(data2_oii, levels=contour_levels2_oii, colors='black', linewidths=0.5, extent=extent_normal, origin='lower')

# Titles, labels, and annotations
axes[0, 0].text(-162, 4.5, 'N II $\\lambda$4041\n3e-17', fontsize=14, bbox=dict(facecolor='white', edgecolor='none'))
axes[1, 0].text(-162, 4.5, 'N II $\\lambda$5680\n4.5e-17', fontsize=14, bbox=dict(facecolor='white', edgecolor='none'))  # Corregido
axes[2, 0].text(-162, 5.5, '4041/5680', fontsize=14, bbox=dict(facecolor='white', edgecolor='none'))
axes[0, 1].text(-162, 4.5, 'O II $\\lambda$4089\n3.0e-17', fontsize=14, bbox=dict(facecolor='white', edgecolor='none'))
axes[1, 1].text(-162, 4.5, 'O II $\\lambda$4649\n8.0e-17', fontsize=14, bbox=dict(facecolor='white', edgecolor='none'))
axes[2, 1].text(-162, 5.5, '4089/4649', fontsize=14, bbox=dict(facecolor='white', edgecolor='none'))

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
    ax.set_ylim(-7, 7)
    ax.yaxis.set_ticks([-6,-3, 0, 3, 6])
# Add colorbars
cax1 = fig.add_axes([0.902, 0.37, 0.02, 0.51])
cbar1 = fig.colorbar(im1_oii, cax=cax1)
cbar1.set_ticks([0, 0.25, 0.5, 0.75, 1])
cbar1.ax.tick_params(labelsize=14) 

cax2 = fig.add_axes([0.902, 0.11, 0.02, 0.254])
cbar2 = fig.colorbar(im3_oii, cax=cax2)
cbar2.set_ticks([0, 0.25, 0.5, 0.75, 1.0])
cbar2.ax.tick_params(labelsize=14) 

# Adjust layout for spacing
fig.subplots_adjust(hspace=0.01, wspace=0.04)

# Save and show
plt.savefig("te_rel-m142.jpg", dpi=2086/16, bbox_inches='tight')
plt.show()