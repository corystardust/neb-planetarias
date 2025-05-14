import matplotlib.pyplot as plt
import astropy.io.fits as fits
import matplotlib.colors as colors
import numpy as np
import pyneb as pn
#from peq91 import emis


# Cargar los archivos FITS
OII4649_perm_additional = fits.getdata("/Users/leslycorina/iraf/archive/hf22-nuevo/descontaminar/decomp_OII4649_perm_additional.fits")
OII4649_perm_normal = fits.getdata("/Users/leslycorina/iraf/archive/hf22-nuevo/descontaminar/decomp_OII4649_perm_normal_1.fits")
OII4649obs = fits.getdata("/Users/leslycorina/iraf/archive/hf22-nuevo/mapaspv4scaled/OII4649pscaled_v4.fits")
temp_o3 = fits.getdata('/Users/leslycorina/iraf/archive/hf22-nuevo/TOIII4363_4959redcorr.fits')

#Voy a establecer las temperaturas del plasma normal y adicional:
#Plasma normal:
Te_pn=8000
ne_pn=1000
#Plasma adicional:
Te_pa=2000 
ne_pa=5000


#-------EMISIVIDAD CON PYNEB PARA 4649 USANDO EL MAPA DE TEMPERATURA-------
#Ahora voy a modelar las emisividades de la línea y 4649
O2_rec = pn.RecAtom('O',2)

# Obtener dimensiones de la imagen
nr, nf = temp_o3.shape

# Crear matrices vacías para las emisividades
emisO2_norm = np.zeros((nr, nf))
emisO2_add = np.zeros((nr, nf))

# Calcular la emisividad para cada punto usando el mapa de temperatura para O II 4649 tanto para el plasma normal como adicional
for i in range(nr):
    for j in range(nf):
        emisO2_n = O2_rec.getEmissivity(Te_pn, ne_pn, wave='4649.13')
        emisO2_a = O2_rec.getEmissivity(Te_pa, ne_pa, wave='4649.13')
        emisO2_norm[i, j] = emisO2_n
        emisO2_add[i, j] = emisO2_a


# Conversión de emisividad y densidad a masa de iones
# Plasma normal nebular: emisividad a 8,000 K y densidad 5,000 cm^-3
mass_ions_norm = emisO2_norm * ne_pn
relmass_mass_normal_nebular_plasma = OII4649_perm_normal / mass_ions_norm

# Plasma adicional: emisividad a 2,000 K y densidad 10,000 cm^-3
mass_ions_add = emisO2_add * ne_pa
relmass_mass_additional_plasma_comp = OII4649_perm_additional / mass_ions_add

# Suma de las masas para obtener la masa total
relmass_total_mass = relmass_mass_normal_nebular_plasma + relmass_mass_additional_plasma_comp

# Calcular la fracción de masa para los componentes
relmass_fractional_mass_normal_nebular_plasma = (
    relmass_mass_normal_nebular_plasma / relmass_total_mass
)
relmass_fractional_mass_additional_plasma_comp = (
    relmass_mass_additional_plasma_comp / relmass_total_mass
)

num_levels = 9  # Number of contour levels (10% to 90% in 10% intervals)
contour_levels = [0+ i * 0.1 * (4.4e-18 - 0) for i in range(1, num_levels + 1)]
plt.contour(OII4649obs, levels=contour_levels, colors='black', linewidths=0.5, origin='lower')

plt.imshow(relmass_total_mass, origin='lower', cmap='jet', aspect='auto')
plt.colorbar()
plt.ylabel('Posición')
plt.xlabel('Velocidad')
plt.title('Relmass_total_mass de O++')
plt.show()

plt.contour(OII4649obs, levels=contour_levels, colors='black', linewidths=0.5, origin='lower')
plt.imshow(relmass_fractional_mass_normal_nebular_plasma, origin='lower', cmap='jet', aspect='auto',vmin=0, vmax=1)
plt.colorbar()
plt.ylabel('Posición')
plt.xlabel('Velocidad')
plt.title('Fracc de masa de O++ plasma normal')
plt.show()

plt.contour(OII4649obs, levels=contour_levels, colors='black', linewidths=0.5, origin='lower')
plt.imshow(relmass_fractional_mass_additional_plasma_comp, origin='lower', cmap='jet', aspect='auto', vmin=0, vmax=1)
plt.colorbar()
plt.ylabel('Posición')
plt.xlabel('Velocidad')
plt.title('Fracc de masa de O++ add')
plt.show()

# Guardar los resultados en nuevos archivos FITS
fits.writeto("relmass_mass_normal_nebular_plasma.fits", relmass_mass_normal_nebular_plasma, overwrite=True)
fits.writeto("relmass_mass_additional_plasma_comp.fits", relmass_mass_additional_plasma_comp, overwrite=True)
fits.writeto("relmass_total_mass.fits", relmass_total_mass, overwrite=True)
fits.writeto("relmass_fractional_mass_normal_nebular_plasma.fits", relmass_fractional_mass_normal_nebular_plasma, overwrite=True)
fits.writeto("relmass_fractional_mass_additional_plasma_comp.fits", relmass_fractional_mass_additional_plasma_comp, overwrite=True)
