import matplotlib.pyplot as plt
import astropy.io.fits as fits
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.colors as colors
from mpl_toolkits.axes_grid1 import make_axes_locatable
# Configuración inicial
color_list = [(1, 1, 1)] + [(0, 0, 1), (0, 1, 1), (0, 1, 0), (1, 1, 0), (1, 0, 0)]
cmap_name = 'custom_cmap'
newcmp = LinearSegmentedColormap.from_list(cmap_name, color_list, N=256)

# Rutas de archivos (6 para cada columna)
file_paths_column1 = [
    '/Users/leslycorina/iraf/archive/hf22-nuevo/mapaspv4scaled/HeII4686pscaled_v4.fits',
    '/Users/leslycorina/iraf/archive/hf22-nuevo/mapaspv4scaled/ArIV4740pscaled_v4.fits',
    '/Users/leslycorina/iraf/archive/hf22-nuevo/mapaspv4scaled/OIII4959pscaled_v4.fits',
    '/Users/leslycorina/iraf/archive/hf22-nuevo/mapaspv5_sinflat_sinflujocorr/ArIII7135pv5_sincosmicos.fits',
    '/Users/leslycorina/iraf/archive/hf22-nuevo/NII6583pv4_flat.fits',
    '/Users/leslycorina/iraf/archive/hf22-nuevo/OI6300pv5_noflat_noflujo_sincosmicos.fits'
]

file_paths_column2 = [
    '/Users/leslycorina/iraf/archive/hf22-nuevo/mapaspv4scaled/NeII3694pscaled_v4.fits',
    '/Users/leslycorina/iraf/archive/hf22-nuevo/mapaspv4scaled/OII4649pscaled_v4.fits',
    '/Users/leslycorina/iraf/archive/hf22-nuevo/mapaspv4scaled/OII4089pscaled_v4.fits',
    '/Users/leslycorina/iraf/archive/hf22-nuevo/NII5679pv4_flat.fits',
    '/Users/leslycorina/iraf/archive/hf22-nuevo/mapaspv4scaled/NII5666pscaled_v4.fits',
    '/Users/leslycorina/iraf/archive/hf22-nuevo/mapaspv5_sinflat_sinflujocorr/CII7231pv5_sincosmicos.fits'
]
extent_normal = [-30, 100, -4.32, 10.44]  # Extent en coordenadas físicas

# Factores de escala y IP (de tu imagen)
scaling_factors1 = [1.0e-17, 5.0e-19, 6.3e-17, 8.0e-18, 1.0e-16, 2.0e-18]
scaling_factors2 = [4.5e-19, 4.53e-18, 1.85e-18, 2.2e-18, 1.1e-18, 2.6e-18]
ip_values1 = ["54.4 eV", "40.7 eV", "35.1 eV", "27.6 eV", "14.5 eV", "0 eV"]
ip_values2 = ["41 eV","35.1 eV", "35.1 eV", "29.6 eV", "29.6 eV", "24.4 eV" ]  # IP para col2

# Función para cargar y normalizar (asegurando datos 2D)
def load_and_normalize(file_paths, scaling_factors):
    normalized_data = []
    for i, file in enumerate(file_paths):
        data = fits.getdata(file)
        if data.ndim == 1:
            data = data.reshape(1, -1)  # Convertir a 2D si es 1D
        elif data.ndim > 2:
            data = data[0]  # Tomar primer frame si es 3D+
        normalized_data.append((data / scaling_factors[i], fits.getheader(file)))
    return normalized_data

# Cargar datos
data_column1 = load_and_normalize(file_paths_column1, scaling_factors1)
data_column2 = load_and_normalize(file_paths_column2, scaling_factors2)

# Crear figura (6 filas × 2 columnas)
fig, axes = plt.subplots(6, 2, figsize=(16, 21), constrained_layout=False, sharex=True, sharey=True)
plt.subplots_adjust(hspace=0.01, wspace=0.02)

# Rango de visualización
vmin, vmax = 0, 1


# Función para graficar con control de ejes
def plot_column(axes_column, data_list, labels, ip_values, scaling_factors):
    last_im = None
    for i, (data, _) in enumerate(data_list):
        ax = axes_column[i]
        im = ax.imshow(data, cmap=newcmp, origin='lower', aspect='auto', extent=extent_normal, vmin=vmin, vmax=vmax)
        
        # Etiqueta de línea iónica, factor de escala y IP
        ax.text(-28, 5.6, f"{labels[i]}\n{scaling_factors[i]:.1e}\nIP: {ip_values[i]}", 
        fontsize=18, bbox=dict(facecolor='white', edgecolor='none'))
        ax.axhline(y=0, linewidth=0.9, color='black')
        ax.yaxis.set_ticks([-3, 0, 3, 6, 9])
        ax.xaxis.set_ticks([-20, 0 , 20, 40, 60, 80])
        last_im = im
    return last_im


# Añadir etiquetas de ejes X para cada columna
for i in range(6):
    axes[i, 0].set_xlabel('v (km/s)', fontsize=20) if i == 5 else None  # Solo última fila columna 1
    axes[i, 1].set_xlabel('v (km/s)', fontsize=20) if i == 5 else None  # Solo última fila columna 2
    
   
# Añadir etiqueta de eje Y solo para columna izquierda
for i in range(6):
	axes[i,0].yaxis.set_tick_params(labelsize=20)

#Solo lo añade una etiqueta
axes[len(axes) // 2, 0].set_ylabel('Spatial axis (arc sec)', fontsize=22)
axes[5,0].xaxis.set_tick_params(labelsize=20)
axes[5,1].xaxis.set_tick_params(labelsize=20)

# Etiquetas para cada columna
labels_column1 = ["He II λ4686", "[Ar IV] λ4740", "[O III] λ4959", 
                 "[Ar III] λ7135", "[N II] λ6583", "[O I] λ6300"]
labels_column2 = ["[O II] λ4649", "[O II] λ4089", "N II λ5680", 
                 "N II λ5666", "C II λ7231", "[Ne II] λ3694"]


# Etiquetas
labels_column1 = ["He II λ4686", "[Ar IV] λ4740", "[O III] λ4959", 
                 "[Ar III] λ7135", "[N II] λ6583", "[O I] λ6300"]
labels_column2 = ["Ne II λ3694", "O II λ4649", "O II λ4089", "N II λ5680", 
                 "N II λ5666", "C II λ7231"]

# Graficar ambas columnas
im1 = plot_column(axes[:, 0], data_column1, labels_column1, ip_values1, scaling_factors1)
im2 = plot_column(axes[:, 1], data_column2, labels_column2, ip_values2, scaling_factors2)

cbar_ax1 = fig.add_axes([0.902, 0.11, 0.02, 0.77])
cbar1 = fig.colorbar(im1, cax=cbar_ax1)
cbar1.ax.tick_params(labelsize=20)
#cbar1.set_label("Intensidad Normalizada")
# Guardar y mostrar
plt.savefig("hf22_is.jpg", dpi=2086/16, bbox_inches='tight')
plt.show()

