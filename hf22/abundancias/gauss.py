import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits


im1=fits.open('/Users/leslycorina/iraf/archive/hf22-nuevo/mapaspv4scaled/Hbetapscaled_v4.fits')
Hbeta=im1[0].data

im2=fits.open('/Users/leslycorina/iraf/archive/hf22-nuevo/descontaminar/oiii4959pv4flux.fits')
OIII4959=im2[0].data


#OIII4959 = np.nan_to_num(OIII4959data, nan=0.0)

reb=len(OIII4959)
dimv=len(OIII4959[0])

OIII4959c = np.zeros((reb,dimv), dtype=float) 

#la temperatura es la asignada al plasma normal o adicional
T =8000
mion=1.
sigma=np.sqrt(82.5*1e-4*T/mion)
print(sigma)
mu=65.5

vel = np.arange(0,dimv,1)
gauss = 1/(sigma * np.sqrt(2 * np.pi)) * np.exp( - (vel-mu)**2 / (2 * sigma**2))


for i in range (reb):
     raw = OIII4959[i,:]
     rawc = np.convolve(raw,gauss, mode = 'same')
     OIII4959c[i,:]=rawc

ratio = OIII4959c/Hbeta
 
plt.subplot(411)  
plt.imshow(Hbeta, aspect ='auto', cmap='jet', origin='lower',vmin=0, vmax=8.e-17)
plt.contour(Hbeta, levels=[8e-18,2e-17,5e-17],colors='black', linewidths=0.4)
plt.title('Hbeta', fontsize=8)
plt.xticks([])
plt.yticks([])

plt.subplot(412)  
plt.imshow(OIII4959, aspect ='auto', cmap='jet', origin='lower',vmin=0, vmax=8.e-17)
plt.contour(OIII4959, levels=[8e-18,2e-17,5e-17],colors='black', linewidths=0.4)
plt.title('OIII4959', fontsize=8)
plt.xticks([])
plt.yticks([])

plt.subplot(413) 
plt.imshow(OIII4959c, aspect ='auto', cmap='jet', origin='lower',vmin=0, vmax=8e-17)
plt.contour(OIII4959, levels=[8e-18,2e-17,5e-17],colors='black', linewidths=0.4)
plt.xticks([])
plt.yticks([])

plt.subplot(414) 
plt.imshow(ratio, aspect ='auto', cmap='jet', origin='lower',vmin=0, vmax=5)
plt.contour(OIII4959, levels=[8e-18,2e-17,5e-17],colors='black', linewidths=0.4)
plt.xticks([])
plt.yticks([])

#plt.show()
imf = fits.PrimaryHDU()
imf.data = OIII4959c
imf.writeto("OIII4959cpv4.fits", overwrite=True)
