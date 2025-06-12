from astropy.io import fits as pyfits
import matplotlib.pyplot as plt
from matplotlib.pyplot import *
import numpy as np
from scipy import interpolate

def nonlinearwave(nwave, specstr, verbose=False):

    fields = specstr.split()
    if int(fields[2]) != 2:
        raise ValueError('Not nonlinear dispersion: dtype=' + fields[2])
    if len(fields) < 12:
        raise ValueError('Bad spectrum format (only %d fields)' % len(fields))
    wt = float(fields[9])
    w0 = float(fields[10])
    ftype = int(fields[11])
    if ftype == 3:
        # cubic spline
        if len(fields) < 15:
            raise ValueError('Bad spline format (only %d fields)' % len(fields))
        npieces = int(fields[12])
        pmin = float(fields[13])
        pmax = float(fields[14])
        if verbose:
            print ('Dispersion is order-%d cubic spline' % npieces)
        if len(fields) != 15 + npieces + 3:
            raise ValueError('Bad order-%d spline format (%d fields)' % (npieces, len(fields)))
        coeff = np.asarray(fields[15:], dtype=float)
        # normalized x coordinates
        s = (np.arange(nwave, dtype=float) + 1 - pmin) / (pmax - pmin) * npieces
        j = s.astype(int).clip(0, npieces - 1)
        a = (j + 1) - s
        b = s - j
        x0 = a ** 3
        x1 = 1 + 3 * a * (1 + a * b)
        x2 = 1 + 3 * b * (1 + a * b)
        x3 = b ** 3
        wave = coeff[j] * x0 + coeff[j + 1] * x1 + coeff[j + 2] * x2 + coeff[j + 3] * x3
    elif ftype == 1 or ftype == 2:
        # chebyshev or legendre polynomial
        # legendre not tested yet
        if len(fields) < 15:
            raise ValueError('Bad polynomial format (only %d fields)' % len(fields))
        order = int(fields[12])
        pmin = float(fields[13])
        pmax = float(fields[14])
        if verbose:
            if ftype == 1:
                print ('Dispersion is order-%d Chebyshev polynomial' % order)
            else:
                print ('Dispersion is order-%d Legendre polynomial (NEEDS TEST)' % order)
        if len(fields) != 15 + order:
            # raise ValueError('Bad order-%d polynomial format (%d fields)' % (order, len(fields)))
            if verbose:
                print ('Bad order-%d polynomial format (%d fields)' % (order, len(fields)))
                print ("Changing order from %i to %i" % (order, len(fields) - 15))
            order = len(fields) - 15
        coeff = np.asarray(fields[15:], dtype=float)
        # normalized x coordinates
        pmiddle = (pmax + pmin) / 2
        prange = pmax - pmin
        x = (np.arange(nwave, dtype=float) + 1 - pmiddle) / (prange / 2)
        p0 = np.ones(nwave, dtype=float)
        p1 = x
        wave = p0 * coeff[0] + p1 * coeff[1]
        for i in range(2, order):
            if ftype == 1:
                # chebyshev
                p2 = 2 * x * p1 - p0
            else:
                # legendre
                p2 = ((2 * i - 1) * x * p1 - (i - 1) * p0) / i
            wave = wave + p2 * coeff[i]
            p0 = p1
            p1 = p2
    else:
        raise ValueError('Cannot handle dispersion function of type %d' % ftype)
    return wave, fields

def readmultispec(fitsfile, reform=True, quiet=True):
    fh = pyfits.open(fitsfile)
    try:
        header = fh[0].header
        flux = fh[0].data
    finally:
        fh.close()
    temp = flux.shape
    nwave = temp[-1]
    if len(temp) == 1:
        nspec = 1
    else:
        nspec = temp[-2]
    # first try linear dispersion
    try:
        crval1 = header['crval1']
        crpix1 = header['crpix1']
        cd1_1 = header['cd1_1']
        ctype1 = header['ctype1']
        if ctype1.strip() == 'LINEAR':
            wavelen = np.zeros((nspec, nwave), dtype=float)
            ww = (np.arange(nwave, dtype=float) + 1 - crpix1) * cd1_1 + crval1
            for i in range(nspec):
                wavelen[i, :] = ww
            # handle log spacing too
            dcflag = header.get('dc-flag', 0)
            if dcflag == 1:
                wavelen = 10.0 ** wavelen
                if not quiet:
                    print ('Dispersion is linear in log wavelength')
            elif dcflag == 0:
                if not quiet:
                    print ('Dispersion is linear')
            else:
                raise ValueError('Dispersion not linear or log (DC-FLAG=%s)' % dcflag)

            if nspec == 1 and reform:
                # get rid of unity dimensions
                flux = np.squeeze(flux)
                wavelen.shape = (nwave,)
            return {'flux': flux, 'wavelen': wavelen, 'header': header, 'wavefields': None}
    except KeyError:
        pass
    # get wavelength parameters from multispec keywords
    try:
        wat2 = header['wat2_*']
        count = len(wat2)
    except KeyError:
        raise ValueError('Cannot decipher header, need either WAT2_ or CRVAL keywords')
    # concatenate them all together into one big string
    watstr = []
    for i in range(len(wat2)):
        # hack to fix the fact that older pyfits versions (< 3.1)
        # strip trailing blanks from string values in an apparently
        # irrecoverable way
        # v = wat2[i].value
        v = wat2[i]
        v = v + (" " * (68 - len(v)))  # restore trailing blanks
        watstr.append(v)
    watstr = ''.join(watstr)
    # find all the spec#="..." strings
    specstr = [''] * nspec
    for i in range(nspec):
        sname = 'spec' + str(i + 1)
        p1 = watstr.find(sname)
        p2 = watstr.find('"', p1)
        p3 = watstr.find('"', p2 + 1)
        if p1 < 0 or p1 < 0 or p3 < 0:
            raise ValueError('Cannot find ' + sname + ' in WAT2_* keyword')
        specstr[i] = watstr[p2 + 1:p3]
    wparms = np.zeros((nspec, 9), dtype=float)
    w1 = np.zeros(9, dtype=float)
    for i in range(nspec):
        w1 = np.asarray(specstr[i].split(), dtype=float)
        wparms[i, :] = w1[:9]
        if w1[2] == -1:
            raise ValueError('Spectrum %d has no wavelength calibration (type=%d)' %
                             (i + 1, w1[2]))
            # elif w1[6] != 0:
            #    raise ValueError('Spectrum %d has non-zero redshift (z=%f)' % (i+1,w1[6]))
    wavelen = np.zeros((nspec, nwave), dtype=float)
    wavefields = [None] * nspec
    for i in range(nspec):
        # if i in skipped_orders:
        #    continue
        verbose = (not quiet) and (i == 0)
        if wparms[i, 2] == 0 or wparms[i, 2] == 1:
            # simple linear or log spacing
            wavelen[i, :] = np.arange(nwave, dtype=float) * wparms[i, 4] + wparms[i, 3]
            if wparms[i, 2] == 1:
                wavelen[i, :] = 10.0 ** wavelen[i, :]
                if verbose:
                    print ('Dispersion is linear in log wavelength')
            elif verbose:
                print ('Dispersion is linear')
        else:
            # non-linear wavelengths
            wavelen[i, :], wavefields[i] = nonlinearwave(nwave, specstr[i],
                                                         verbose=verbose)
        wavelen *= 1.0 + wparms[i, 6]
        if verbose:
            print ("Correcting for redshift: z=%f" % wparms[i, 6])
    if nspec == 1 and reform:
        # get rid of unity dimensions
        flux = np.squeeze(flux)
        wavelen.shape = (nwave,)
    return {'flux': flux, 'wavelen': wavelen, 'header': header, 'wavefields': wavefields}

#	   0   1    2    3    4    5    6    7     8     9
ccds=['1','2','3b','3r','4b','2s','3rs','4r','3bs','4rs']
reb= [23 , 23,  40,  40,  40,  23,   40,  40,   40,   40]
pixeles=[1500,1500,2048,2048,2048,1500,2048,2048,2048,2048]

star=[19.106,20.2,11,11,9.1 ,20.2,11   ,9.1 ,11   ,9.1  ]   #coord python 
#iraf=[20.13,21.945,10.604,10.883,10.046,10.325,12.5,21.209,21.442,11]   #coord iraf
resol=[0.5,0.5,0.36,0.36,0.36,0.36,0.5,0.36,0.36,0.36]
orienta=[0,0,1,1,1,1,0,1,1,1]

abajo=[]
arriba=[]
for k in [0,1,2,3,4,7]: #de acuerdo al orden de los ccds 0 es ccd1 y 1 es ccd2
   down=resol[k]*(star[k]+1)
   up=(reb[k]-(star[k]+1))*resol[k]
   if orienta[k]:
      abajo.append(down)
      arriba.append(up)
   else:
      abajo.append(up)
      arriba.append(down)

upg = max(arriba)
downg = max(abajo)


c = 2.997925e5
resesp = 0.36         #resolución final
npv = 131   #dimension en velocidad (1 km/s)
npe = int((upg+downg)/resesp)   #dimension espacial
vblue = -30   #limite azul de velocidad
vred = vblue+(npv-1)
npixdown= int(downg/resesp)          #posición final de la estrella o referencia

print('rebanadas finales = '+str(npe))
print('posición de la estrella de referencia = '+str(npixdown))

file=open('lineas3b.dat','r')
lineas=file.readlines()
file.close()

for nlin in range(0,295):
  row=lineas[nlin].split()
  dn=ccds.index(row[0])
  label = row[1]
  lc = float(row[2])
  nol = int(row[3])-1
  ps = star[dn]
  win=[]
  win.append(int(row[4])) 
  win.append(int(row[5]))
  win.append(int(row[6]))
  win.append(int(row[7]))
  pri=row[8]
  nrb = reb[dn]   #numero de rebanadas
  npix= pixeles[dn]
  
  

  mapa = np.zeros((nrb,npix), dtype=float) #mapa original
  mapac = np.zeros((nrb,npix), dtype=float) #mapa sin continuo
  mapabv = np.zeros((nrb,npv), dtype=float) #cortado con resolucion en v de 1 km/s
  mapabr = np.zeros((npe,npv), dtype=float) # sampleado a 0.36 arcsec/px
  mapaflux = np.zeros((npe,npv), dtype=float) # correccion en flujo arcsec/px
  cont = np.zeros(npix, dtype=float)
  f2b = np.zeros(npe, dtype=float)

  for nr in range(nrb):
    if dn==0:  name='/Users/leslycorina/iraf/archive/hf22-nuevo/cd1/hf1r'+str(nr+1)+'_fc.fits'  #1
    if dn==1:  name='/Users/leslycorina/iraf/archive/hf22-nuevo/cd2/hf2r'+str(nr+1)+'_fc.fits' #2
    if dn==2:  name='/Users/leslycorina/iraf/archive/hf22-nuevo/cd3/cd3a/hf3br'+str(nr+1)+'_fc.fits'  #3b
    if dn==3:  name='/Users/leslycorina/iraf/archive/hf22-nuevo/cd3/cd3r/hf3rr'+str(nr+1)+'_fc.fits'  #3r
    if dn==4:  name='/Users/leslycorina/iraf/archive/hf22-nuevo/cd4/cd4a/hf4br'+str(nr+1)+'_fc.fits' #4b
    #if dn==5:  name='/Users/leslycorina/iraf/archive/hf22-nuevo/cd2/hf2r'+str(nr+1)+'_sfc.fits'  #2ns
    #if dn==6:  name='/Users/leslycorina/iraf/archive/hf22-nuevo/cd3/cd3r/hf3rr'+str(nr+1)+'_sfc.fits'  #3rns
    if dn==7:  name='/Users/leslycorina/iraf/archive/hf22-nuevo/cd4/cd4r/hf4rr'+str(nr+1)+'_fc.fits'   #4r
    #if dn==8:  name='/Users/leslycorina/iraf/archive/hf22-nuevo/cd3/cd3a/hf3br'+str(nr+1)+'_sfc.fits'  #3bns
    #if dn==9:  name='/Users/leslycorina/iraf/archive/hf22-nuevo/cd4/cd4r/hf4rr'+str(nr+1)+'_sfc.fits'   #4rns
    espectro = readmultispec(name, reform=True)
    mapa[nr,:]=espectro['flux'][nol]  #mapa original

  ww=np.arange(npix)
  for nr in range(nrb):
    f=mapa[nr,:]
    cont[:]=1.0
    x=[]
    y=[]
    for i in range(win[0],win[1]):
        x.append(i)
        y.append(mapa[nr,i])
    for i in range(win[2],win[3]):
        x.append(i)
        y.append(mapa[nr,i])
    x=np.array(x)
    y=np.array(y)
    xav=np.mean(ww)
    xnor=x/xav
    yav=np.mean(f)
    ynor=y/yav
    z = np.polyfit(xnor, ynor, 1)
    cont=np.polyval(z,ww/xav)*yav
    imc = f - cont
    mapac[nr][:]=imc    #mapa sin continuo

  w1=espectro['wavelen'][nol]

  v1=(w1-lc)*c/lc
  vb = np.linspace(vblue,vred,num=npv) #resolucion en vel de 1 km/s


  for nr in range(nrb):
    f1b = np.zeros(npv, dtype=float)
    f1=interpolate.interp1d(v1,mapac[nr,:])
    for u in range(npv):
      if vb[u] <= v1[-1]:
         f1b[u]=f1(vb[u])    
    mapabv[nr,:]=f1b  #mapa en velocidad

  r=np.arange(nrb)
  dp=resesp/resol[dn]    #resolucion deseada para unificar	   
  right=orienta[dn]
  
  if right:
    rb=[ps - (npixdown-1)*dp]
  else:
    rb=[ps + (npixdown-1)*dp]   
  for j in range(npe-1):
    if right:
       rb.append(rb[j]+dp)
    else:
       rb.append(rb[j]-dp)

  for nv in range(npv):
    f2=interpolate.interp1d(r,mapabv[:,nv])
    for j in range(npe):
      if rb[j] >= 0.0 and rb[j] <= (nrb-1): 
         f2b[j]=f2(rb[j])
      else:
         f2b[j]=0.0
    mapabr[:,nv]=f2b   # mapa con resolucion final
  
  mapaflux=mapabr/((c/lc)*(1./dp)) #factores de correccion por la interpolacion
  
  filename = label+pri+'v4.fits'  
  imf = pyfits.PrimaryHDU()
  imf.data = np.arange(npe,npv)
  imf.data = mapaflux
  imf.writeto(filename)
  print (nlin)


