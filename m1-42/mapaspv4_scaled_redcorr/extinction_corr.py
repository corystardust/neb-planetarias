import os
import numpy as np
import pyneb as pn
from astropy.io import fits
import matplotlib.pyplot as plt

# Directorio donde se encuentran los archivos escalados .fits
fits_directory = '/Users/leslycorina/iraf/archive/m1-42/mapaspv4scaled/'

# Factor de extinción
extinction_E_BV = 0.35

# Crear el modelo de extinción usando pyneb
rc = pn.RedCorr(R_V=3.1, law='F99')
rc.E_BV = extinction_E_BV

# Leer el archivo lineas3b.dat para obtener las correspondencias
with open('/Users/leslycorina/iraf/archive/m1-42/lineas3b.dat', 'r') as file:
    lines = file.readlines()

# Iterar sobre cada línea del archivo
for line in lines:
    parts = line.split()
    identifier = parts[0]
    line_name = parts[1]
    wavelength_angstrom = float(parts[2])  # Longitud de onda en angstroms
    suffix = parts[-3]  # La columna con las letras p, ns, s

    fits_name = f"{line_name}{suffix}scaled_v4.fits"
    fits_path = os.path.join(fits_directory, fits_name)

    # Verificar si el archivo escalado .fits existe
    if os.path.exists(fits_path):
        # Leer el archivo escalado .fits
        with fits.open(fits_path) as im1:
            datos1 = im1[0].data

            # Inicializar un arreglo 2D para almacenar los resultados
            o3 = np.zeros_like(datos1)

            # Obtener el factor de corrección en pyneb para la longitud de onda
            corr = rc.getCorr(wavelength_angstrom)
            print(f"Corrección para {fits_name}: {corr}")

            # Aplicar la corrección por extinción al mapa de datos
            for i in range(datos1.shape[0]):
                for j in range(datos1.shape[1]):
                    o3[i, j] = datos1[i, j] * corr

            # Guardar el mapa PV corregido como un archivo FITS
            new_fits_name = f"{line_name}{suffix}v4fluxredcorr_pyneb.fits"
            new_fits_path = os.path.join(fits_directory, new_fits_name)
            imf = fits.PrimaryHDU(data=o3)
            imf.writeto(new_fits_path, overwrite=True)

            # Mostrar la gráfica del mapa PV resultante
            plt.imshow(o3, origin='lower')
            plt.title(f'Mapa PV para {fits_name}')
            plt.colorbar()
            plt.show()

            # Calcular y mostrar la relación entre el mapa corregido y el original
            ratio = o3 / datos1
            plt.imshow(ratio, origin='lower')
            plt.title(f'Ratio entre mapa corregido y original para {fits_name}')
            plt.colorbar()
            plt.show()
    else:
        print(f'Archivo no encontrado: {fits_name}')
