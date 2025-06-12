import matplotlib.pyplot as plt
import astropy.io.fits as fits
import matplotlib.colors as colors
import numpy as np

# Open the FITS files and extract the image data
data1, header1 = fits.getdata('OIII4363pv4fluxredcorr_pyneb.fits', header=True)
data2, header2 = fits.getdata('OIII4959nsv4fluxredcorr_pyneb.fits', header=True)
data3, header3 = fits.getdata('TOIII4363_4959nsredcorrpv4.fits', header=True)

# Create a figure with three subplots
fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, figsize=(8, 10), sharex=True)

# Plot the images on the subplots and store the images as variables
im1 = ax1.imshow(data1/7.8e-17, cmap='jet', aspect='auto', vmin=0, vmax=1)
im2 = ax2.imshow(data2/5.5e-15, cmap='jet', aspect='auto', vmin=0, vmax=1)
# Create a mappable object with the data range and colormap used for the first two subplots
mappable = plt.cm.ScalarMappable(norm=colors.Normalize(vmin=0, vmax=1), cmap='jet')
mappable.set_array([])  # Dummy array for colorbar

# Add a colorbar to the figure with limits set to the data range of the first two subplots
cax = fig.add_axes([0.853, 0.4, 0.02, 0.48])
cbar = fig.colorbar(mappable, cax=cax)

# Add contours to the first two plots
# Plot the third image on its subplot and store the image as a variable
im3 = ax3.imshow(data3, cmap='jet', aspect='auto', vmin=5000, vmax=15000)

#contour_levels = np.linspace(-1e-16 + 0.1 * (2e-15 - (-1e-16)), -1e-16 + 0.6 * (2e-15- (-1e-16)), 10)
num_levels = 9  # Number of contour levels (10% to 90% in 10% intervals)
contour_levels = [0+ i * 0.1 * (7.8e-17 - 0) for i in range(1, num_levels + 1)]
contour_levels2 = [0+ i * 0.1 * (5.5e-15 - 0) for i in range(1, num_levels + 1)]

contours2 = ax1.contour(data1, levels=contour_levels, colors='black', linewidths=0.5)
# Add contours to the second plot (ax2)
contours2 = ax2.contour(data2, levels=contour_levels2, colors='black', linewidths=0.5)
# Add contours to the third plot (ax3) using its own color limits
contours3 = ax3.contour(data2, levels=contour_levels2, colors='black', linewidths=0.5)

# Add a colorbar to the figure for the third subplot
cax2 = fig.add_axes([0.853, 0.123, 0.02, 0.25])
cbar2 = fig.colorbar(im3, cax=cax2)
#contours3 = ax3.contour(data2, levels=10, colors='black', linewidths=0.5)
# Invert the y-axis of each subplot
ax1.invert_yaxis()
ax2.invert_yaxis()
ax3.invert_yaxis()

ax1.axhline(y=24,linewidth=0.9, color='white')  
ax2.axhline(y=24,linewidth=0.9, color='white')  
ax3.axhline(y=24,linewidth=0.9, color='white')  
# Set titles for the subplots with adjusted font size
ax1.text(1.5, 38,'[O III] $\\lambda$4363\n7.8e-17', fontsize=12, bbox=dict(facecolor='white'))
ax2.text(1.5, 38,'[O III] $\\lambda$4959\n5.5e-15', fontsize=12, bbox=dict(facecolor='white'))
ax3.text(1.5, 42,'T$_{e}$ [O III]', fontsize=12, bbox=dict(facecolor='white'))
ax2.set_ylabel('Eje espacial')
ax3.set_xlabel('V (km/s)')
plt.xlabel('T (K)')

# Adjust the spacing between subplots and colorbars
fig.subplots_adjust(right=0.85, hspace=0.4, wspace=0.2)

# Adjust the spacing between the first two subplots
fig.subplots_adjust(hspace=0.01)
#plt.savefig("[OIII]_withcontours_m142_norm.png",dpi=300, overwrite=True)# Show the figure
plt.show()