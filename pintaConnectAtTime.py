#Calculamos la densidad media de conexiones 
# =1 si densidad isotropa
# >1 mas probabilidad que la esperada
# <1 menos probabilidad que la esperada

import math
from pylab import *

dir='/home/jcfernandez/resultados/eps1/u100/AMPL/W2.0/CONNECT/NEO/'
name='dis-densidadconnectA'+'0.05'+'.dat'

print 'Fichero: ',name
#Importamos los datos
for line in file(dir+name):
    line=line.replace('\n','')
    val=line.split(' ')
    res=[]
    n=0
    for v in val:
        if v!='':
            res.append(float(v))
    t=res[0]
    densi=res[1::]
    x=[]
    y=[]
    #Discretizacion angular
    step=180./(len(densi))
    for i in range(len(densi)):
        media[i]+=densi[i]
        media2[i]+=densi[i]*densi[i]
        count[i]+=1.0

x=[]
y=[]
erry=[]
#Calculamos los valores  medios y el error
print len(densi),len(count)
for i in range(len(media)):
    x.append((i)*step+0.5*step)
    if count[i]>0.0:
        valmedio=media[i]/count[i]
        error=math.sqrt(abs(media2[i]/count[i]-valmedio*valmedio))
        erry.append(error)
        y.append(valmedio)
    else:
        y.append(0.0)

f = open(dir+'dis-'+name,'w')
for i in range(len(x)):
    f.write(str(x[i])+' '+str(y[i])+' '+str(erry[i])+'\n')
#        f.write(str(x[i])+' '+str(y[i])+'\n')
f.close()

#plot(x,y,'ro')
errorbar(x, y, yerr=erry, fmt='o-')
show()
