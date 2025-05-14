import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits


im1=fits.open('/Users/leslycorina/iraf/archive/m1-42/mapaspv4scaled_redcorr/Hbetansv4fluxredcorr_pyneb.fits')
Hbeta=im1[0].data

im2=fits.open('/Users/leslycorina/iraf/archive/m1-42/mapaspv4scaled_redcorr/OII4649pv4fluxredcorr_pyneb.fits')
OII4649=im2[0].data

#OII4649 = np.nan_to_num(OII4649pv, nan=0.0)

reb=len(OII4649)
dimv=len(OII4649[0])

OII4649c = np.zeros((reb,dimv), dtype=float) 

#temperatura del plasma normal o adicional 
T =2000
mion=1.
sigma=np.sqrt(82.5*1e-4*T/mion)
print(sigma)
mu=65.5 
vel = np.arange(0,dimv,1)
gauss = 1/(sigma * np.sqrt(2 * np.pi)) * np.exp( - (vel-mu)**2 / (2 * sigma**2))


for i in range (reb):
     raw = OII4649[i,:]
     rawc = np.convolve(raw,gauss, mode = 'same')
     OII4649c[i,:]=rawc

ratio = OII4649c/Hbeta
 
plt.subplot(411)  
plt.imshow(Hbeta, aspect ='auto', cmap='jet', origin='lower',vmin=0, vmax=2.e-15)
plt.contour(Hbeta, levels=[8e-17,2e-16,5e-16],colors='black', linewidths=0.4)
plt.title('Hbeta', fontsize=8)
plt.xticks([])
plt.yticks([])

plt.subplot(412)  
plt.imshow(OII4649, aspect ='auto', cmap='jet', origin='lower',vmin=0, vmax=2.e-15)
plt.contour(OII4649, levels=[8e-17,2e-16,5e-16],colors='black', linewidths=0.4)
plt.title('OII4649', fontsize=8)
plt.xticks([])
plt.yticks([])

plt.subplot(413) 
plt.imshow(OII4649c, aspect ='auto', cmap='jet', origin='lower',vmin=0, vmax=2e-15)
plt.contour(OII4649, levels=[8e-17,2e-16,5e-16],colors='black', linewidths=0.4)
plt.xticks([])
plt.yticks([])

plt.subplot(414) 
plt.imshow(ratio, aspect ='auto', cmap='jet', origin='lower',vmin=0, vmax=0.1)
plt.contour(OII4649, levels=[8e-17,2e-16,5e-16],colors='black', linewidths=0.4)
plt.xticks([])
plt.yticks([])

plt.show()
imf = fits.PrimaryHDU()
imf.data = ratio
imf.writeto("OII4649cpv4_hbetansv4.fits", overwrite=True)
