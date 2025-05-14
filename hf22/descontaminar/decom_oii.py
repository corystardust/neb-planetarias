import matplotlib.pyplot as plt
import astropy.io.fits as fits
import matplotlib.colors as colors
import numpy as np
import pyneb as pn
from peq91 import emis


#Voy a importar los mapas P-V que voy a utilizar:
#[N II] 5755
hdu_4959= fits.open('/Users/leslycorina/iraf/archive/hf22-nuevo/mapaspv4/oiii4959pv4flux.fits')
data_4959 = hdu_4959[0].data
hdu_4959.close()
#N II 4649
hdu_4649 = fits.open('/Users/leslycorina/iraf/archive/hf22-nuevo/mapaspv4scaled/OII4649pscaled_v4.fits')
data_4649 = hdu_4649[0].data
hdu_4649.close()
hdu_toiii = fits.open('/Users/leslycorina/iraf/archive/hf22-nuevo/TOIII4363_4959redcorr.fits')
data_tempO3 = hdu_toiii[0].data
hdu_toiii.close()


#Voy a establecer las temperaturas del plasma normal y adicional:
#Plasma normal:
Te_pn=8000
ne_pn=1000
#Plasma adicional:
#Para el plasma adicional:
Te_pa=2000 
ne_pa=5000


#-------EMISIVIDAD CON PYNEB PARA 4649 Y 4959 USANDO EL MAPA DE TEMPERATURA-------
#Ahora voy a modelar las emisividades de las líneas de 4959 y 4649
#Para [O III] usaré los datos atómicos de PyNeb:
O3 = pn.Atom('O',3)
O2_rec = pn.RecAtom('O',2)

# Obtener dimensiones de la imagen
nr, nf = data_tempO3.shape

# Crear matrices vacías para las emisividades
emis_4959 = np.zeros((nr, nf))
emis_4649 = np.zeros((nr, nf))

# Calcular la emisividad para cada punto
for i in range(nr):
    for j in range(nf):
        emisO3 = O3.getEmissivity(data_tempO3[i, j], ne_pn, wave='4959A')
        emisO2 = O2_rec.getEmissivity(data_tempO3[i, j], ne_pn, wave='4649.13')
        emis_4959[i, j] = emisO3
        emis_4649[i, j] = emisO2

ratio_emis= emis_4649/emis_4959

#-------------------------------------------------------------------------------

rel_N_O= 1 #este valor viene de la abundancia relativa 

decomp_OII4649_perm_normal= data_4959*ratio_emis
decomp_OII4649_perm_normal_1 = decomp_OII4649_perm_normal*rel_N_O
decomp_OII4649_perm_additional= data_4649-decomp_OII4649_perm_normal_1

plt.imshow(decomp_OII4649_perm_normal, origin='lower', cmap='jet', aspect='auto')
plt.colorbar(label='Intensidad')
plt.ylabel('Posición')
plt.xlabel('Velocidad')
plt.title('decomp_OII4649_perm_normal')
plt.show()

# guardar como FITS
imf = fits.PrimaryHDU()
imf.data = decomp_OII4649_perm_normal
imf.writeto('decomp_OII4649_perm_normal.fits', overwrite=True)

plt.imshow(decomp_OII4649_perm_normal_1, origin='lower', cmap='jet', aspect='auto')
plt.colorbar(label='Intensidad')
plt.ylabel('Posición')
plt.xlabel('Velocidad')
plt.title('decomp_OII4649_perm_normal_1')
plt.show()

# guardar como FITS
imf = fits.PrimaryHDU()
imf.data = decomp_OII4649_perm_normal_1
imf.writeto('decomp_OII4649_perm_normal_1.fits',overwrite=True)

plt.imshow(decomp_OII4649_perm_additional, origin='lower', cmap='jet', aspect='auto')
plt.colorbar(label='Intensidad')
plt.ylabel('Posición')
plt.xlabel('Velocidad')
plt.title('decomp_OII4649_perm_additional',)
plt.show()

# guardar como FITS
imf = fits.PrimaryHDU()
imf.data = decomp_OII4649_perm_additional
imf.writeto('decomp_OII4649_perm_additional.fits',overwrite=True)



