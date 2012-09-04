from visual import *
import time
import sys
import numpy as np
from matplotlib import pyplot

def histogram(values, nhist):
    maxValue=max(values)
    minValue=min(values)
    suma=0.0
    
    dist = np.zeros((nhist+1))
    count = np.zeros((nhist+1))
    step=(maxValue-minValue)/float(nhist)
    for val in values:
        dnd=int(math.floor((val-minValue)/step))
        dist[dnd]+=val
        count[dnd]+=1.0
    
    #Normalizacion
    for i in range(1,len(count)):
        suma+=step*(count[i]+count[i-1])*0.5
    x=[]
    y=[]
    for i in range(len(count)):
        x.append(minValue+float(i)*step)
        y.append(count[i]/suma)
    return [x,y]

def showSystem(xpos,diameter):
    tonto =[diameter,xpos]
    tonto.sort()
    print "tonto:",tonto
    [diameter, xpos]=tonto
    
    sistema=[]
    scene.background = color.gray(0.7)
    for i in range(len(diameter)):
        ball = sphere (pos=xpos[i], radius=0.5*diameter[i], color = color.red ,material=materials.rough)
        time.sleep(1)
        sistema.append(ball)
    
    print tonto
    return sistema

def showOrder(xpos,diameter):
    tonto=[]
    for i in range(len(diameter)):
        tonto.append([diameter[i],i])
    tonto.sort()  
    tonto2=[]
    for i in range(len(tonto)):
        tonto2.append([tonto[i][0],xpos[tonto[i][1]]])
    tonto2.reverse()
    print 'tonto2',tonto2
    sistema=[]
    scene.background = color.gray(0.7)
    for i in range(len(tonto2)):
        ball = sphere (pos=tonto2[i][1], radius=0.5*tonto2[i][0], color = color.red ,material=materials.rough)
        time.sleep(0.5)
        sistema.append(ball)
    return sistema

def maxmin(pos,radio):
    x=[]
    y=[]
    z=[]
    for i in range(len(pos)):
        x.append(pos[i][0]+radio[i])
        x.append(pos[i][0]-radio[i])
        y.append(pos[i][1]+radio[i])
        y.append(pos[i][1]-radio[i])
        z.append(pos[i][2]+radio[i])
        z.append(pos[i][2]-radio[i])
    valmax=[max(x),max(y),max(z)]
    valmin=[min(x),min(y),min(z)]
    return [valmin,valmax]


def importCluster(name):
    f = open(name,'r')
    tx = f.readline()
    tx = tx.replace('\n','')
    val = tx.split(' ')
    res=[]
    for v in val:
        if v!='':
            res.append(float(v))
    npart = int(res[0])
    pos=[]
    diameter=[]
    for i in range(npart):
        tx = f.readline()
        tx = tx.replace('\n','')
        val = tx.split(' ')
        aux=[]
        for v in val:
            if v!='':
                aux.append(v)
    
        xpos=[float(aux[0]),float(aux[1]),float(aux[2])]
        pos.append(xpos)
        diameter.append(float(aux[3]))
    return [pos,diameter]


name='/home/jonk/projects/sizes/cluster.dat'
[pos,radio]=importCluster(name)
nbin=int(len(pos)/7.0)
[valmin,valmax]=maxmin(pos,radio)
print "xmin: ",valmin[0],"ymin:",valmin[1],"zmin:",valmin[2]
print "xmax: ",valmax[0],"ymax:",valmax[1],"zmax:",valmax[2]
[dx,dy,dz]= np.array(valmax)-np.array(valmin)
print "Dx:",dx,"Dy:",dy,"Dz:",dz
print np.array(valmax)-np.array(valmin)
[x,y] = histogram(radio, nbin)
#pyplot.plot(x,y,'r-')
#pyplot.show()
showOrder(pos,radio)
