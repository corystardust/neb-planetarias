def a(line):
  if (line==5755): return 2.096
  if (line==6583): return 60.66
  if (line==5680): return 1.462
  if (line==5007): return 6.635

def b(line):
  if (line==5755): return -0.4453
  if (line==6583): return -0.3298
  if (line==5680): return -0.628
  if (line==5007): return -0.5925
  
def c(line):
  if (line==5755): return 7.938
  if (line==6583): return 46.54
  if (line==5680): return 1.683
  if (line==5007): return 0.4324
  
def d(line):
  if (line==5755): return 0.211
  if (line==6583): return 0.2926
  if (line==5680): return 0.667
  if (line==5007): return 0.0854
  
def br(line):
  if (line==5755): return 1.023/(1.023+0.0001315+0.03297)
  if (line==6583): return 0.003005/(0.003005+0.001016+0.0000003554)
  if (line==5680): return 0.337
  if (line==5007): return 0.02046/(0.02046+0.006785+0.000005508+0.000002322)
  
def z(line):
  if (line==5755): return 2.
  if (line==6583): return 2.
  if (line==5680): return 2.
  if (line==5007): return 3.
  

def t(temp,z):
  return (1.e-4*temp/pow(z,2.))
  
def energy(line):
  hc = 6.62607015e-27*3.e10
  if (line==5755): return hc/(5754.57*1.e-8)
  if (line==6583): return hc/(6583.39*1.e-8)
  if (line==5680): return hc/(5679.56*1.e-8)
  if (line==5007): return hc/(5006.85*1.e-8)
  
def alfa(line, temp):
  valor = br(line)*1.e-13*z(line)*a(line)*pow(t(temp,z(line)),b(line))/(1.+c(line)*pow(t(temp,z(line)),d(line)))
  return(valor)
  
def emis(line,temp):
  return alfa(line,temp)*energy(line) 
  
  
def ceros(image):
  for i in range(len(image)):
    for j in range(len(image[0])):
       if (image[i,j]<0):
         image[i,j]= 'NaN'
  
   
  
