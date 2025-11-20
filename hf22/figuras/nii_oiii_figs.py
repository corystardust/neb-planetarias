import matplotlib.pyplot as plt
import astropy.io.fits as fits
import matplotlib.colors as colors
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib as mpl

# Cambiar la fuente globalmente
mpl.rcParams['font.family'] = 'sans-serif'
mpl.rcParams['font.serif'] = ['Verdana']
#mpl.rcParams['font.size'] = 12

# Define custom colormap
color_list = [(1, 1, 1)] + [(0, 0, 1), (0, 1, 1), (0, 1, 0), (1, 1, 0), (1, 0, 0)]  # White to Red
cmap_name = 'custom_cmap'
newcmp = LinearSegmentedColormap.from_list(cmap_name, color_list, N=256)

# Load FITS data for OIII
data1_oiii, header1_oiii = fits.getdata('/Users/leslycorina/iraf/archive/hf22-nuevo/mapaspv4scaled/OIII4363pscaled_v4.fits', header=True)
data2_oiii, header2_oiii = fits.getdata('/Users/leslycorina/iraf/archive/hf22-nuevo/mapaspv4scaled/OIII4959pscaled_v4.fits', header=True)
data3_oiii, header3_oiii = fits.getdata('TOIII4363_4959redcorr.fits', header=True)

# Load FITS data for NII
data1_nii, header1_nii = fits.getdata('/Users/leslycorina/iraf/archive/hf22-nuevo/descontaminar/nii5755collpv4.fits', header=True)
data2_nii, header2_nii = fits.getdata('/Users/leslycorina/iraf/archive/hf22-nuevo/descontaminar/nii6583coll_noflat_pv4.fits', header=True)
data3_nii, header3_nii = fits.getdata('/Users/leslycorina/iraf/archive/hf22-nuevo/temp_den/hf22temp_5755_6583_flat_pv4.fits', header=True)

extent_normal = [-30, 100, -4.32, 10.44]  # Extent in physical coordinates

# Create a figure with six subplots (3 rows, 2 columns)
fig, axes = plt.subplots(nrows=3, ncols=2, figsize=(16, 10.5), sharex=True, sharey=True)


# Plot NII images
im1_nii = axes[0, 0].imshow((data1_nii / 8e-19), cmap=newcmp, aspect='auto', vmin=0, vmax=1, extent=extent_normal, origin='lower')
im2_nii = axes[1, 0].imshow((data2_nii / 1e-16), cmap=newcmp, aspect='auto', vmin=0, vmax=1, extent=extent_normal, origin='lower')
im3_nii = axes[2, 0].imshow(data3_nii, cmap=newcmp, aspect='auto', vmin=5000, vmax=16000, extent=extent_normal, origin='lower')

# Plot OIII images
im1_oiii = axes[0, 1].imshow((data1_oiii / 1.5e-18), cmap=newcmp, aspect='auto', vmin=0, vmax=1, extent=extent_normal, origin='lower')
im2_oiii = axes[1, 1].imshow((data2_oiii / 6.3e-17), cmap=newcmp, aspect='auto', vmin=0, vmax=1, extent=extent_normal, origin='lower')
im3_oiii = axes[2, 1].imshow(data3_oiii, cmap=newcmp, aspect='auto', vmin=5000, vmax=16000, extent=extent_normal, origin='lower')

# Add contours for NII
contour_levels_nii = np.linspace(0, 1e-18, 10)
contour_levels2_nii = np.linspace(0, 5e-17, 10)
axes[0, 0].contour(data1_nii, levels=contour_levels_nii, colors='black', linewidths=0.5, extent=extent_normal, origin='lower')
axes[1, 0].contour(data2_nii, levels=contour_levels2_nii, colors='black', linewidths=0.5, extent=extent_normal, origin='lower')
axes[2, 0].contour(data2_nii, levels=contour_levels2_nii, colors='black', linewidths=0.5, extent=extent_normal, origin='lower')

# Add contours for OIII
contour_levels_oiii = np.linspace(0, 2e-18, 10)
contour_levels2_oiii = np.linspace(0, 6.3e-17, 10)
axes[0, 1].contour(data1_oiii, levels=contour_levels_oiii, colors='black', linewidths=0.5, extent=extent_normal, origin='lower')
axes[1, 1].contour(data2_oiii, levels=contour_levels2_oiii, colors='black', linewidths=0.5, extent=extent_normal, origin='lower')
axes[2, 1].contour(data2_oiii, levels=contour_levels2_oiii, colors='black', linewidths=0.5, extent=extent_normal, origin='lower')


# Titles, labels, and annotations
axes[0, 0].text(-27.5, 7.8, '[N II] $\\lambda$5755\n8.0e-19', fontsize=14, bbox=dict(facecolor='white', edgecolor='none'))
axes[1, 0].text(-27.5, 7.8, '[N II] $\\lambda$6583\n1.0e-16', fontsize=14, bbox=dict(facecolor='white', edgecolor='none'))
axes[2, 0].text(-27.5, 9, 'T$_e$ [N II]', fontsize=14, bbox=dict(facecolor='white', edgecolor='none'))
axes[0, 1].text(-27.5, 7.8, '[O III] $\\lambda$4363\n1.5e-18', fontsize=14, bbox=dict(facecolor='white', edgecolor='none'))
axes[1, 1].text(-27.5, 7.8, '[O III] $\\lambda$4959\n6.3e-17', fontsize=14, bbox=dict(facecolor='white', edgecolor='none'))
axes[2, 1].text(-27.5, 9, 'T$_e$ [O III]', fontsize=14, bbox=dict(facecolor='white', edgecolor='none'))

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
cbar1 = fig.colorbar(im1_oiii, cax=cax1)
cbar1.set_ticks([0, 0.25, 0.5, 0.75, 1])
cbar1.ax.tick_params(labelsize=14) 
cax2 = fig.add_axes([0.902, 0.11, 0.02, 0.254])
cbar2 = fig.colorbar(im3_oiii, cax=cax2)
cbar2.set_ticks([6000, 8000, 10000, 12000, 14000])
cbar2.ax.tick_params(labelsize=14)
# Adjust layout for spacing
fig.subplots_adjust(hspace=0.01, wspace=0.04)

# Save and show
plt.savefig("te_cel-hf22.jpg", dpi=2086/16, bbox_inches='tight')
plt.show()