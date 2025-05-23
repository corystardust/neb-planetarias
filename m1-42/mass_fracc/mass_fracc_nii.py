import matplotlib.pyplot as plt
import astropy.io.fits as fits
import matplotlib.colors as colors
import numpy as np
import pyneb as pn
#from peq91 import emis


# Cargar los archivos FITS
NII5680_perm_additional = fits.getdata("/Users/leslycorina/iraf/archive/m1-42/descontaminar/decomp_NII5679_perm_additional.fits")
NII5680_perm_normal = fits.getdata("/Users/leslycorina/iraf/archive/m1-42/descontaminar/decomp_NII5679_perm_normal_1.fits")
NII5680_obs = fits.getdata('/Users/leslycorina/iraf/archive/m1-42/mapaspv4scaled_redcorr/NII5679pv4fluxredcorr_pyneb.fits')
temp_o3 = fits.getdata('/Users/leslycorina/iraf/archive/m1-42/TOIII4363_4959nsredcorrpv4.fits')

#Voy a establecer las temperaturas del plasma normal y adicional:
#Plasma normal:
Te_pn=7500 #En el caso del plasma normal, se puede establecer la temperatura fija o usar el mapa de temperatura
#no afecta significativamente al resultado
ne_pn=1000
#Plasma adicional:
#Para el plasma adicional:
Te_pa=2000 
ne_pa=7500
#-------EMISIVIDAD CON PYNEB PARA 5680 USANDO EL MAPA DE TEMPERATURA-------
#Ahora voy a modelar las emisividades de las línea de 5680
#Para N II usaré los datos atómicos de PyNeb: (en el script de michael vienen asi)
N2_rec = pn.RecAtom('N',2)

# Obtener dimensiones de la imagen
nr, nf = temp_o3.shape

# Crear matrices vacías para las emisividades
emisN2_norm = np.zeros((nr, nf))
emisN2_add = np.zeros((nr, nf))

# Calcular la emisividad para cada punto usando el mapa de temperatura para O II 4649 tanto para el plasma normal como adicional
for i in range(nr):
    for j in range(nf):
        emisN2_n = N2_rec.getEmissivity(Te_pn, ne_pn, wave='5679.56')
        emisN2_a = N2_rec.getEmissivity(Te_pa, ne_pa, wave='5679.56')
        emisN2_norm[i, j] = emisN2_n
        emisN2_add[i, j] = emisN2_a


# Conversión de emisividad y densidad a masa de iones
# Plasma normal nebular: emisividad a 7,500 K y densidad 1,000 cm^-3
mass_ions_norm = emisN2_norm * ne_pn
relmass_mass_normal_nebular_plasma = NII5680_perm_normal / mass_ions_norm

# Plasma adicional: emisividad a 6,500 K y densidad 7,500 cm^-3
mass_ions_add = emisN2_add * ne_pa
relmass_mass_additional_plasma_comp = NII5680_perm_additional / mass_ions_add


# Cálculo de la masa total
relmass_total_mass = relmass_mass_normal_nebular_plasma + relmass_mass_additional_plasma_comp

# Calcular fracciones de masa
relmass_fractional_mass_normal_nebular_plasma = (
    relmass_mass_normal_nebular_plasma / relmass_total_mass
)
relmass_fractional_mass_additional_plasma_comp = (
    relmass_mass_additional_plasma_comp / relmass_total_mass
)
rel_fracc_mass_total=relmass_fractional_mass_normal_nebular_plasma+relmass_fractional_mass_additional_plasma_comp

num_levels = 9  # Number of contour levels (10% to 90% in 10% intervals)
contour_levels = [0+ i * 0.1 * (4.6e-17 - 0) for i in range(1, num_levels + 1)]
plt.contour(NII5680_obs, levels=contour_levels, colors='black', linewidths=0.5, origin='lower')



plt.imshow(relmass_total_mass, origin='lower', cmap='jet', aspect='auto')
plt.colorbar()
plt.ylabel('Posición')
plt.xlabel('Velocidad')
plt.title('Relmass_total_mass de N++')
plt.show()

plt.contour(NII5680_obs, levels=contour_levels, colors='black', linewidths=0.5, origin='lower')
plt.imshow(relmass_fractional_mass_normal_nebular_plasma, origin='lower', cmap='jet', aspect='auto', vmin=0, vmax=1)
plt.colorbar()
plt.ylabel('Posición')
plt.xlabel('Velocidad')
plt.title('Fracc de masa de N++ plasma normal')
plt.show()

plt.contour(NII5680_obs, levels=contour_levels, colors='black', linewidths=0.5, origin='lower')
plt.imshow(relmass_fractional_mass_additional_plasma_comp, origin='lower', cmap='jet', aspect='auto', vmin=0, vmax=1)
plt.colorbar()
plt.ylabel('Posición')
plt.xlabel('Velocidad')
plt.title('Fracc de masa de N++ add')
plt.show()

plt.contour(NII5680_obs, levels=contour_levels, colors='black', linewidths=0.5, origin='lower')
plt.imshow(rel_fracc_mass_total, origin='lower', cmap='jet', aspect='auto')
plt.colorbar()
plt.ylabel('Posición')
plt.xlabel('Velocidad')
plt.title('Fracc de masa de N++ total')
plt.show()

# Guardar los resultados en nuevos archivos FITS
fits.writeto("relmass_mass_n++_normal_nebular_plasma.fits", relmass_mass_normal_nebular_plasma, overwrite=True)
fits.writeto("relmass_mass_n++_additional_plasma_comp.fits", relmass_mass_additional_plasma_comp, overwrite=True)
fits.writeto("relmass_n++_total_mass.fits", relmass_total_mass, overwrite=True)
fits.writeto("relmass_fractional_mass_n++_normal_nebular_plasma.fits", relmass_fractional_mass_normal_nebular_plasma, overwrite=True)
fits.writeto("relmass_fractional_mass_n++_additional_plasma_comp.fits", relmass_fractional_mass_additional_plasma_comp, overwrite=True)
