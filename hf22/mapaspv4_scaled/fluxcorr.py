import os
import numpy as np
from astropy.io import fits

# Directorio donde se encuentran los archivos .fits
fits_directory = '/Users/leslycorina/iraf/archive/hf22-nuevo/mapaspv4/'

# Factores de escala basados en la primera columna del archivo
scaling_factors = {
    '1': 1.03,
    '2': 1,
    '2s': 1,
    '3b': 2.17,
    '3bs': 2.17,
    '3r': 0.65,
    '3rs': 0.65,
    '4b': 0.5,
    '4r': 0.4,
    '4rs': 0.4,
}

# Leer el archivo lineas3b.dat para obtener las correspondencias
with open('/Users/leslycorina/iraf/archive/m1-42/lineas3b.dat', 'r') as file:
    lines = file.readlines()

# Iterar sobre cada línea del archivo
for line in lines:
    parts = line.split()
    identifier = parts[0]
    line_name = parts[1]
    suffix = parts[-3]  # La columna con las letras p, ns, s

    fits_name = f"{line_name}{suffix}v4.fits"

    # Construir la ruta completa al archivo .fits
    fits_path = os.path.join(fits_directory, fits_name)

    # Verificar si el archivo .fits existe
    if os.path.exists(fits_path):
        # Leer el archivo .fits
        with fits.open(fits_path) as hdul:
            data = hdul[0].data

            # Aplicar el factor de escala correspondiente
            scaling_factor = scaling_factors.get(identifier, 1)  # Usar 1 si no se encuentra el identificador
            scaled_data = data * scaling_factor

            # Guardar los datos escalados en un nuevo archivo .fits
            new_fits_name = fits_name.replace('v4.fits', 'scaled_v4.fits')
            new_fits_path = os.path.join(fits_directory, new_fits_name)
            hdul[0].data = scaled_data
            hdul.writeto(new_fits_path, overwrite=True)

        print(f'Archivo escalado guardado: {new_fits_name}')
    else:
        print(f'Archivo no encontrado: {fits_name}')
