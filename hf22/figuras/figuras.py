import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import astropy.io.fits as fits
from matplotlib import cm
from matplotlib.colors import LinearSegmentedColormap

color_list = [(1, 1, 1)] + [(0, 0, 1), (0, 1, 1), (0, 1, 0), (1, 1, 0), (1, 0, 0)]  # Blanco a Rojo
cmap_name = 'custom_cmap'
newcmp = LinearSegmentedColormap.from_list(cmap_name, color_list, N=256)

# Open the FITS files and extract the image data for the remaining plots
data5680, header5680= fits.getdata('/Users/leslycorina/iraf/archive/hf22-nuevo/NII5679pv4_flat.fits', header=True)
data1, header1 = fits.getdata('nii5754pv4flux.fits', header=True)
data2, header2 = fits.getdata('decomp_NII5755_perm_normal.fits', header=True)
data3, header3 = fits.getdata('decomp_NII5755_perm_additional.fits', header=True)
data4, header4 = fits.getdata('nii5755collpv4.fits', header=True)


data5, header5 = fits.getdata('/Users/leslycorina/iraf/archive/hf22-nuevo/NII6583pv4_flat.fits', header=True)
data6, header6 = fits.getdata('decomp_NII6583_perm_normal_noflat.fits', header=True)
data7, header7 = fits.getdata('decomp_NII6583_perm_additional_flat.fits', header=True)
data8, header8 = fits.getdata('nii6583coll_noflat_pv4.fits', header=True)

extent_normal = [-30,100,-4.32, 10.44] # Extent en coordenadas físicas
#nuevo extent porque el eje Y está mal, hay que multiplicarlo por 0.72


fig, axs = plt.subplots(nrows=4, ncols=2, figsize=(16, 14), sharex=True, sharey=True)

# Plot the images on the subplots with inverted y-axes
im1 = axs[0, 0].imshow(data1/1e-18, cmap=newcmp, aspect='auto', vmin=0, vmax=1, extent=extent_normal, origin='lower')
im2 = axs[1, 0].imshow(data2/1e-18, cmap=newcmp, aspect='auto', vmin=0, vmax=1, extent=extent_normal, origin='lower')
im3 = axs[2, 0].imshow(data3/1e-18, cmap=newcmp, aspect='auto', vmin=0, vmax=1, extent=extent_normal, origin='lower')
im4 = axs[3, 0].imshow(data4/1e-18, cmap=newcmp, aspect='auto', vmin=0, vmax=1, extent=extent_normal, origin='lower')
im5 = axs[0, 1].imshow(data5/1e-16, cmap=newcmp, aspect='auto', vmin=0, vmax=1, extent=extent_normal, origin='lower')
im6 = axs[1, 1].imshow(data6/1e-16, cmap=newcmp, aspect='auto', vmin=0, vmax=1, extent=extent_normal, origin='lower')
im7 = axs[2, 1].imshow(data7/1e-16, cmap=newcmp, aspect='auto', vmin=0, vmax=1, extent=extent_normal, origin='lower')
im8 = axs[3, 1].imshow(data8/1e-16, cmap=newcmp, aspect='auto', vmin=0, vmax=1, extent=extent_normal, origin='lower')

# Create a mappable object with the data range and colormap used for the first two subplots
mappable = plt.cm.ScalarMappable(norm=colors.Normalize(vmin=0, vmax=1), cmap=newcmp)
mappable.set_array([])  # Dummy array for colorbar

# Add a colorbar to the figure with limits set to the data range of the first two subplots
cax = fig.add_axes([0.852, 0.11, 0.02, 0.77])
cbar = fig.colorbar(mappable, cax=cax)
cbar.ax.xaxis.set_ticks_position('top')
cbar.ax.xaxis.set_label_position('top')
cbar.ax.tick_params(labelsize=14)
# Add a colorbar to the figure
for ax in axs.flat:
    #ax.invert_yaxis()           # Invertir el eje y
    ax.axhline(y=0, linewidth=0.9, color='black')  # Agregar línea horizontal
    ax.yaxis.set_ticks([-3, 0, 3, 6, 9])

# Set titles for the subplots

titles = ['[N II] 5755 (obs) \n1e-18', '[N II] 6583 (obs)\n1e-16', '[N II] 5755 (norm)\n1e-18', '[N II] 6583 (norm)\n1e-16',
          '[N II] 5755 (add)\n1e-18', '[N II] 6583 (add)\n1e-16', '[N II] 5755 (coll)\n1e-18', '[N II] 6583 (coll) \n1e-16']
for i, ax in enumerate(axs.flat):
    ax.text(-27, 8, titles[i], fontsize=14, bbox=dict(facecolor='white', edgecolor='none'))
    ax.yaxis.set_tick_params(labelsize=14)
    ax.xaxis.set_tick_params(labelsize=14)

num_levels=9
contour_levels2 = [0 + i * 0.1 * (2.2e-18 - 0) for i in range(1, num_levels + 1)]

# Supongamos que axs es un array de subplots
contours2 = axs[0, 0].contour(data5680, levels=contour_levels2, colors='black', linewidths=0.5,extent=extent_normal, origin='lower')
contours2 = axs[1, 0].contour(data5680, levels=contour_levels2, colors='black', linewidths=0.5,extent=extent_normal, origin='lower')
contours2 = axs[2, 0].contour(data5680, levels=contour_levels2, colors='black', linewidths=0.5,extent=extent_normal, origin='lower')
contours2 = axs[3, 0].contour(data5680, levels=contour_levels2, colors='black', linewidths=0.5,extent=extent_normal, origin='lower')
contours2 = axs[0, 1].contour(data5680, levels=contour_levels2, colors='black', linewidths=0.5,extent=extent_normal, origin='lower')
contours2 = axs[1, 1].contour(data5680, levels=contour_levels2, colors='black', linewidths=0.5,extent=extent_normal, origin='lower')
contours2 = axs[2, 1].contour(data5680, levels=contour_levels2, colors='black', linewidths=0.5,extent=extent_normal, origin='lower')
contours2 = axs[3, 1].contour(data5680, levels=contour_levels2, colors='black', linewidths=0.5,extent=extent_normal, origin='lower')



# Etiquetas de los ejes
axs[-1, 0].set_xlabel('v (km/s)',fontsize=14)
axs[-1, 1].set_xlabel('v (km/s)',fontsize=14)
#axs[1, 0].set_ylabel('Spatial axis (arc sec)',fontsize=14)
axs[len(axs) // 2, 0].set_ylabel('Spatial axis (arc sec)', fontsize=14)

# Ajustar el espacio entre subplots y la barra de color
fig.subplots_adjust(right=0.85, hspace=0.01, wspace=0.01)

# Save and show the figure
plt.savefig("hf22_decom_6583_noflat.jpg", dpi=2086/16, bbox_inches='tight')
plt.show()


# Cargar los datos de los archivos FITS
data1, header1 = fits.getdata('/Users/leslycorina/iraf/archive/hf22-nuevo/TNII5754_6583redcorrpv4_prueba2.fits', header=True)
data2, header2 = fits.getdata('/Users/leslycorina/iraf/archive/hf22-nuevo/temp_den/hf22temp_5755_6583_flat_pv4.fits', header=True)
data3, header3 = fits.getdata('/Users/leslycorina/iraf/archive/hf22-nuevo/TOIII4363_4959redcorr.fits', header=True)

# Crear una figura con 2 subplots verticales
fig, axs = plt.subplots(nrows=3, figsize=(7, 10), sharex=True)

# Establecer los límites de la barra de color (5000 K a 15000 K)
vmin, vmax = 5000, 16000

# Graficar los datos sin normalización
im1 = axs[0].imshow(data1, cmap=newcmp, aspect='auto', vmin=vmin, vmax=vmax, extent=extent_normal, origin='lower')
im2 = axs[1].imshow(data2, cmap=newcmp, aspect='auto', vmin=vmin, vmax=vmax, extent=extent_normal, origin='lower')
im3 = axs[2].imshow(data3, cmap=newcmp, aspect='auto', vmin=vmin, vmax=vmax, extent=extent_normal, origin='lower')

axs[0].text(-27, 23,'T$_{e}$ (no corr)', fontsize=14, bbox=dict(facecolor='white',edgecolor='none'))
axs[1].text(-27, 23,'T$_{e}$ (corr)', fontsize=12, bbox=dict(facecolor='white', edgecolor='none'))
axs[2].text(-27, 23,'T$_{e}$ [O III]', fontsize=12, bbox=dict(facecolor='white', edgecolor='none'))




for ax in axs.flat:
    #ax.invert_yaxis()           # Invertir el eje y
    ax.axhline(y=0, linewidth=0.9, color='black')  # Agregar línea horizontal
    
# Agregar una barra de color común para ambos subplots
cax = fig.add_axes([0.902, 0.11, 0.02, 0.77])  # [left, bottom, width, height]
cbar = fig.colorbar(im1, cax=cax)
#cbar.set_label('Temperatura (K)')
cbar.ax.xaxis.set_ticks_position('top')
cbar.ax.xaxis.set_label_position('top')

#contours2 = axs[0].contour(data5680, levels=contour_levels2, colors='black', linewidths=0.5)
#contours2 = axs[1].contour(data5680, levels=contour_levels2, colors='black', linewidths=0.5)

# Ajustar el espacio entre subplots
fig.subplots_adjust(hspace=0.01)

# Agregar etiquetas de los ejes
axs[-1].set_xlabel('V (km/s)')
axs[1].set_ylabel('Spatial axis (arc sec)')

# Mostrar la figura
# Save and show the figure
#plt.savefig("hf22_decom_tempNII_6583_noflat.png", dpi=2086/16, overwrite=True)
#plt.show()
