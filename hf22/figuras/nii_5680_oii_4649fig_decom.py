import matplotlib.pyplot as plt
import astropy.io.fits as fits
import matplotlib.colors as colors
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

# Colormap personalizado
color_list = [(1, 1, 1)] + [(0, 0, 1), (0, 1, 1), (0, 1, 0), (1, 1, 0), (1, 0, 0)]
cmap_name = 'custom_cmap'
newcmp = LinearSegmentedColormap.from_list(cmap_name, color_list, N=256)

# Cargar datos
data_files = [
    '/Users/leslycorina/iraf/archive/hf22-nuevo/NII5679pv4_flat.fits',
    '/Users/leslycorina/iraf/archive/hf22-nuevo/mapaspv4scaled/OII4649pscaled_v4.fits',
    '/Users/leslycorina/iraf/archive/hf22-nuevo/descontaminar/decomp_NII5679_perm_normal_1.fits',
    '/Users/leslycorina/iraf/archive/hf22-nuevo/descontaminar/decomp_OII4649_perm_normal_1.fits',    
    '/Users/leslycorina/iraf/archive/hf22-nuevo/descontaminar/decomp_NII5679_perm_additional.fits',
    '/Users/leslycorina/iraf/archive/hf22-nuevo/descontaminar/decomp_OII4649_perm_additional.fits',
]

scaling_factors = [2e-18, 4.53e-18, 2e-19, 4.53e-19, 2e-18,  4.53e-18]
data = [fits.getdata(f) / s for f, s in zip(data_files, scaling_factors)]

extent_normal = [-30, 100, -4.32, 10.44]  # Extent en coordenadas físicas

# Crear figura y subplots (3 filas × 2 columnas)
fig, axs = plt.subplots(nrows=3, ncols=2, figsize=(16, 10.5), sharex=True, sharey=True)

# Aplanar la matriz de subplots para iterar fácilmente
axs_flat = axs.flatten()

# Plotear las imágenes en cada subplot
for ax, img_data in zip(axs_flat, data):
    im = ax.imshow(img_data, cmap=newcmp, aspect='auto', vmin=0, vmax=1, 
                  extent=extent_normal, origin='lower')
    ax.axhline(y=0, linewidth=0.9, color='black')
    ax.yaxis.set_tick_params(labelsize=14)
    ax.xaxis.set_tick_params(labelsize=14)
    ax.yaxis.set_ticks([-3, 0, 3, 6, 9])

# Crear un mapeo de color común
mappable = plt.cm.ScalarMappable(norm=colors.Normalize(vmin=0, vmax=1), cmap=newcmp)
mappable.set_array([])

# Barra de color
cax = fig.add_axes([0.902, 0.11, 0.02, 0.77])
cbar = fig.colorbar(mappable, cax=cax)
cbar.set_ticks([0, 0.25, 0.5, 0.75, 1])
cbar.ax.tick_params(labelsize=14)

# Etiquetas y títulos (usando axs_flat para acceder a los subplots)
axs_flat[-2].set_xlabel('v (km/s)', fontsize=14)
axs_flat[-1].set_xlabel('v (km/s)', fontsize=14)
axs_flat[2].set_ylabel('Spatial axis (arc sec)', fontsize=14)  # Subplot central izquierdo

titles = [
    'N II $\\lambda$5680 (obs)\n2e-18',
    'O II $\\lambda$4649 (obs)\n4.53e-18',
    'N II $\\lambda$5680 (norm)\n2e-19',
    'O II $\\lambda$4649 (norm)\n4.53e-19',
    'N II $\\lambda$5680 (add)\n2e-18',
    'O II $\\lambda$4649 (add)\n4.53e-18',
]

for ax, title in zip(axs_flat, titles):
    ax.text(-27, 7.5, title, fontsize=14, bbox=dict(facecolor='white', edgecolor='none'))

# Ajustar espaciado
fig.subplots_adjust(hspace=0.01, wspace=0.04)

# Guardar y mostrar figura
plt.savefig("nii_oiidecom.jpg", dpi=2086/16, bbox_inches="tight")
plt.show()