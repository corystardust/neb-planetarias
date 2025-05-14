#Este script es para retirar la contribución de líneas permitidas en lineas prohibidas
import matplotlib.pyplot as plt
import astropy.io.fits as fits
import matplotlib.colors as colors
import numpy as np
import pyneb as pn
from peq91 import emis


#Voy a importar los mapas P-V que voy a utilizar:
#[N II] 5755
hdu_5755= fits.open('/Users/leslycorina/iraf/archive/hf22-nuevo/mapaspv4/nii5754pv4flux.fits')
data_5755 = hdu_5755[0].data
hdu_5755.close()
#[N II] 6583
hdu_6583= fits.open('/Users/leslycorina/iraf/archive/hf22-nuevo/NII6583pv4_flat.fits')
data_6583 = hdu_6583[0].data
hdu_6583.close()
#[O III] 4959
hdu_4959= fits.open('/Users/leslycorina/iraf/archive/hf22-nuevo/mapaspv4/oiii4959pv4flux.fits')
data_4959 = hdu_4959[0].data
hdu_4959.close()
#N II 5680
hdu_5680 = fits.open('/Users/leslycorina/iraf/archive/hf22-nuevo/NII5679pv4_flat.fits')
data_5680 = hdu_5680[0].data
hdu_5680.close()
#mapa de temperatur:
temp_O3= fits.open('/Users/leslycorina/iraf/archive/hf22-nuevo/temp_den/TOIII4363_4959redcorrpv4.fits')
data_tempO3 = temp_O3[0].data
temp_O3.close()

#Voy a establecer las temperaturas del plasma normal y adicional:
#Plasma normal:
Te_pn=8000
ne_pn=1000
#Plasma adicional:
#Para el plasma adicional:
Te_pa=2000 
ne_pa=5000

O3 = pn.Atom('O',3)
N2_rec = pn.RecAtom('N',2)

# Obtener dimensiones de la imagen
nr, nf = data_tempO3.shape

# Crear matrices vacías para las emisividades
emis_4959 = np.zeros((nr, nf))
emis_5679 = np.zeros((nr, nf))

# Calcular la emisividad para cada punto
for i in range(nr):
    for j in range(nf):
        emisO3 = O3.getEmissivity(data_tempO3[i, j], ne_pn, wave='4959A')
        emisN2 = N2_rec.getEmissivity(data_tempO3[i, j], ne_pn, wave='5679.56')
        emis_4959[i, j] = emisO3
        emis_5679[i, j] = emisN2

ratio_emis= emis_5679/emis_4959



#ahora hay que descomponer N II 5680:

rel_N_O= 0.46 #este valor viene de la abundancia relativa de N/O obtenida de Liu et al 2006

decomp_NII5679_perm_normal= data_4959*ratio_emis
decomp_NII5679_perm_normal_1 = decomp_NII5679_perm_normal*rel_N_O
decomp_NII5679_perm_additional= data_5680-decomp_NII5679_perm_normal_1

plt.imshow(decomp_NII5679_perm_normal, origin='lower', cmap='jet', aspect='auto')
plt.colorbar(label='Intensidad')
plt.ylabel('Posición')
plt.xlabel('Velocidad')
plt.title('decomp_NII5679_perm_normal')
plt.show()

# guardar como FITS
#imf = fits.PrimaryHDU()
#imf.data = decomp_NII5679_perm_normal
#imf.writeto('decomp_NII5679_perm_normal.fits')

plt.imshow(decomp_NII5679_perm_normal_1, origin='lower', cmap='jet', aspect='auto')
plt.colorbar(label='Intensidad')
plt.ylabel('Posición')
plt.xlabel('Velocidad')
plt.title('decomp_NII5679_perm_normal_1')
plt.show()

# guardar como FITS
imf = fits.PrimaryHDU()
imf.data = decomp_NII5679_perm_normal_1
imf.writeto('decomp_NII5679_perm_normal_1.fits', overwrite=True)

plt.imshow(decomp_NII5679_perm_additional, origin='lower', cmap='jet', aspect='auto')
plt.colorbar(label='Intensidad')
plt.ylabel('Posición')
plt.xlabel('Velocidad')
plt.title('decomp_NII5679_perm_additional')
plt.show()

# guardar como FITS
imf = fits.PrimaryHDU()
imf.data = decomp_NII5679_perm_additional
imf.writeto('decomp_NII5679_perm_additional.fits', overwrite=True)

#Ahora hay que crear la emisión permitida del plasma adicional para [N II] 5755 y 6583
#utilizando los datos de emisividad de Péquignot et al. (1991) a una Te de 2500 K
emis_5755_ad = emis(5755,Te_pa)
emis_5680_ad = emis(5680,Te_pa)
emis_6583_ad = emis(6583,Te_pa)
#cociente de emisividades:
ratio_emis5755_5680_ad = round(emis_5755_ad/emis_5680_ad,3)
ratio_emis6583_5680_ad = round(emis_6583_ad/emis_5680_ad,3)
print('emis_5755_ad/emis_5680_ad = ',ratio_emis5755_5680_ad)
print('emis_6583_ad/emis_5680_ad =', ratio_emis6583_5680_ad)

decomp_NII5755_perm_additional=decomp_NII5679_perm_additional*ratio_emis5755_5680_ad
decomp_NII6583_perm_additional=decomp_NII5679_perm_additional*ratio_emis6583_5680_ad

plt.imshow(decomp_NII5755_perm_additional, origin='lower', cmap='jet', aspect='auto')
plt.colorbar(label='Intensidad')
plt.ylabel('Posición')
plt.xlabel('Velocidad')
plt.title('decomp_NII5755_perm_additional')
plt.show()
# guardar como FITS
imf = fits.PrimaryHDU()
imf.data = decomp_NII5755_perm_additional
imf.writeto('decomp_NII5755_perm_additional.fits', overwrite=True)

plt.imshow(decomp_NII6583_perm_additional, origin='lower', cmap='jet', aspect='auto')
plt.colorbar(label='Intensidad')
plt.ylabel('Posición')
plt.xlabel('Velocidad')
plt.title('decomp_NII6583_perm_additional(sin flat)')
plt.show()
# guardar como FITS
imf = fits.PrimaryHDU()
imf.data = decomp_NII6583_perm_additional
imf.writeto('decomp_NII6583_perm_additional_flat.fits', overwrite=True)

#Generar emisión permitida en el plasma normal, utilizando los datos de de Péquignot et al. (1991) a 2500 K
emis_5755_nor = emis(5755,Te_pn)
emis_5680_nor = emis(5680,Te_pn)
emis_6583_nor = emis(6583,Te_pn)
ratio_emis5755_5680_nor = round(emis_5755_nor/emis_5680_nor,3)
ratio_emis6583_5680_nor = round(emis_6583_nor/emis_5680_nor,3)
print('ratio_emis5755/5680_nor = ',ratio_emis5755_5680_nor)
print('ratio_emis6583/5680_nor =',ratio_emis6583_5680_nor)


decomp_NII5755_perm_normal= decomp_NII5679_perm_normal_1*ratio_emis5755_5680_nor
decomp_NII6583_perm_normal= decomp_NII5679_perm_normal_1*ratio_emis6583_5680_nor

plt.imshow(decomp_NII5755_perm_normal, origin='lower', cmap='jet', aspect='auto')
plt.colorbar(label='Intensidad')
plt.ylabel('Posición')
plt.xlabel('Velocidad')
plt.title('decomp N II 5755 perm normal')
plt.show()
# guardar como FITS
imf = fits.PrimaryHDU()
imf.data = decomp_NII5755_perm_normal
imf.writeto('decomp_NII5755_perm_normal.fits', overwrite=True)

plt.imshow(decomp_NII6583_perm_normal, origin='lower', cmap='jet', aspect='auto')
plt.colorbar(label='Intensidad')
plt.ylabel('Posición')
plt.xlabel('Velocidad')
plt.title('decomp N II 6583 perm normal (sin flat)')
plt.show()

# guardar como FITS
imf = fits.PrimaryHDU()
imf.data = decomp_NII6583_perm_normal
imf.writeto('decomp_NII6583_perm_normal_noflat.fits',overwrite=True)



#Ahora hay que crear la emisión permitida total de cada línea:

decomp_NII5755_perm_total= decomp_NII5755_perm_normal+decomp_NII5755_perm_additional
decomp_NII6583_perm_total = decomp_NII6583_perm_normal+decomp_NII6583_perm_additional

#plt.imshow(decomp_NII5755_perm_total, origin='lower', cmap='jet', aspect='auto')
#plt.colorbar(label='Intensidad')
#plt.xlabel('Posición')
#plt.ylabel('Velocidad')
#plt.title('decomp_NII5755_perm_total')
#plt.show()
# guardar como FITS
#imf = fits.PrimaryHDU()
#imf.data = decomp_NII5755_perm_total
#imf.writeto('decomp_NII5755_perm_total.fits')


plt.imshow(decomp_NII6583_perm_total, origin='lower', cmap='jet', aspect='auto')
plt.colorbar(label='Intensidad')
plt.xlabel('Velocidad')
plt.ylabel('Posición')
plt.title('decomp_NII6583_perm_total (noflat)')
plt.show()
# guardar como FITS
imf = fits.PrimaryHDU()
imf.data = decomp_NII6583_perm_total
imf.writeto('decomp_NII6583_perm_total_noflat.fits', overwrite=True)


#Ahora, hay que generar los mapas PV de emisión prohibida 'pura':

data_5755_cleaned = data_5755 - decomp_NII5755_perm_total
data_6583_cleaned = data_6583 -decomp_NII6583_perm_total

plt.imshow(data_5755_cleaned, origin='lower', cmap='jet', aspect='auto')
plt.colorbar(label='Intensidad')
plt.ylabel('Posición')
plt.xlabel('Velocidad')
plt.title('data_5755_cleaned')
plt.show()
# guardar como FITS
imf = fits.PrimaryHDU()
imf.data = data_5755_cleaned
imf.writeto('nii5755collpv4.fits',overwrite=True)

plt.imshow(data_6583_cleaned, origin='lower', cmap='jet', aspect='auto')
plt.colorbar(label='Intensidad')
plt.xlabel('Velocidad')
plt.ylabel('Posición')
plt.title('data_6583_coll (noflat)')
plt.show()

imf = fits.PrimaryHDU()
imf.data = data_6583_cleaned
imf.writeto('nii6583coll_noflat_pv4.fits', overwrite=True)




