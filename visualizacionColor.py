import struct
from visual import *
from pylab import *
import time
import sys
import os
    
class particula:
    """Abstraccion de los objetos coche."""
    def __init__(self, pos, diam,id):
        self.pos = pos
        self.diam=diam
        self.cluster=id

class cluster:
    def __init__(self,part,size):
        self.part=part
        self.size=size

def rgb(c):
    split = (c[0:2], c[2:4], c[4:6])
    vvv = [int(x, 16) for x in split]
    fin = tuple([vvv[0]/255.0,vvv[1]/255.0,vvv[2]/255.0])
    return fin

def colorSize2(size):
    if size <=60:
        return color.blue
    elif size>60 and size<=100:
        return color.green
    elif size>100 and size <=120:
        return color.orange
    elif size>120 and size<=150:
        return color.red
    else:
        return color.yellow;


def colorSize(size):
    ccc = ["FFFFFF","CCCCCC","99FF99","FFCC99","00FFFF","FF99FF","FFFF00","33CCCC","CCCC99","FF9966","00FA9A","FFCC00","00FF99","FF66CC","FF9966","00CCCC","66FF00","9966CC","3399FF","99CC33","FF6666","339999","FF9900","FF00FF","33CC66","6666CC","00FF00","CC6666","9933FF","CC9900","CC6633","009999","339966","009999","FF3300","996633","333399","CC0033","0000FF","336666","993333","990099","009900","FF0000","0000CC","330099","006600","000099","990000","0000CC"]
    
    #ccc = ["FFFFFF","CCCCCC","99FF99","FFCC99","00FA9A","FFCC00","00FF99","FF66CC","FF9966","00CCCC","66FF00","9966CC","3399FF","99CC33","FF6666","339999","FF9900","FF00FF","33CC66","6666CC","00FF00","CC6666","9933FF","CC9900","CC6633","009999","339966","009999","FF3300","996633","333399","CC0033","0000FF","336666","993333","990099","009900","FF0000","0000CC","330099","006600","000099","990000","0000CC"]
#    v1=v2=0
#    if size>100:
#        v1 = int(size/100*255.0/9.0)
#    if size>10:
#        v2 = int((size-v1*100)/10*255.0/9.0)
#    v3 = int((size-v1*100-v2*10)*255.0/9.0)
    id = int(float(size)/100.0)
    #print 'aaaaaaaaaaaaaaaaa',size,id
    #time.sleep(0.5)
    return rgb(ccc[len(ccc)-1-id])

    return (int(v1*25.5),int(v2*25.5),int(v3*25.5))
    if size <=5:
        return color.white
    elif size >5 and size <=10:
        return color.blue
    elif size>10 and size<=100:
        return color.green
    elif size>100 and size <=300:
        return color.orange
    elif size>300 and size<=500:
        return color.red
    elif size>500 and size<=700:
        return color.black
    else:
        return color.yellow;

def colorCluster(clusters):
    colores=[]
    for i in range(len(clusters)):
        size = clusters[i].size
        col = colorSize(size)
        colores.append(col)
    return colores


def Lboundary(x, lx):
    res=x
    while x>=lx:
        x-=lx
    while x<0:
        x+=lx
    return x

def boundary(pos, lx,ly,lz):
    pos[0]=Lboundary(pos[0],lx)
    pos[1]=Lboundary(pos[1],ly)
    pos[2]=Lboundary(pos[2],lz)
    return pos

def showSystem(clusters):
    nnn=0
    sistema=[]
    scene.background = color.gray(0.7)
    colores = colorCluster(clusters)
    #print colores
    for i in range(len(clusters)):
        col = colores[i]
        for j in range(clusters[i].size):
            ball = sphere (pos=clusters[i].part[j].pos, radius=clusters[i].part[j].diam*0.5, color = col ,material=materials.rough)
            #ball = sphere (pos=xpos[i], radius=10./18., color = color.red ,material=materials.rough)
            sistema.append(ball)
            nnn+=1
    return sistema

def updateSystem(clusters, sistema):
    sistema2=[]
    nnn=0
    colores = colorCluster(clusters)
    for i in range(len(clusters)):
        col = colores[i]
        for j in range(clusters[i].size):
           sistema[nnn].pos= clusters[i].part[j].pos
           sistema[nnn].color=col
           sistema2.append(sistema[nnn])
           nnn+=1
    return sistema2

def printBox(lbox,rad):
    lx=lbox[0]
    ly=lbox[1]
    lz=lbox[2]

    
    scene2 = display(title='set Q',width=600, height=600, center=(0.5*lx,0.5*ly,0.5*lz), background=(0.95,0.95,0.95))
    L0 = scene.lights[0]
    L0.color = 0.9*vector(L0.color)
    scene2.lights = [L0]
    d = L0.direction
    L1 = distant_light(direction=(lx,0,0),       color=L0.color)
    rod = cylinder(pos=(0,0,0),axis=(lx,0,0), radius=rad, color = color.black)
    rod = cylinder(pos=(0,0,0),axis=(0,ly,0), radius=rad, color = color.black)
    rod = cylinder(pos=(0,0,0),axis=(0,0,lz), radius=rad, color = color.black)
    rod = cylinder(pos=(lx,0,0),axis=(0,ly,0), radius=rad, color = color.black)
    rod = cylinder(pos=(lx,0,0),axis=(0,0,lz), radius=rad, color = color.black)
    rod = cylinder(pos=(0,ly,0),axis=(0,0,lz), radius=rad, color = color.black)
    rod = cylinder(pos=(0,ly,0),axis=(lx,0,0), radius=rad, color = color.black)
    
    rod = cylinder(pos=(0,0,lz),axis=(lx,0,0), radius=rad, color = color.black)
    rod = cylinder(pos=(0,0,lz),axis=(0,ly,0), radius=rad, color = color.black)
    
    rod = cylinder(pos=(lx,ly,0),axis=(0,0,lz), radius=rad, color = color.black)
    rod = cylinder(pos=(lx,0,lz),axis=(0,ly,0), radius=rad, color = color.black)
    rod = cylinder(pos=(0,ly,lz),axis=(lx,0,0), radius=rad, color = color.black)

def readData(f):
    #Leemos el numero total de clusters
    tx = f.readline()
    tx = tx.replace('\n','')
    val = tx.split(' ')
    aux=[]
    for v in val:
        if v!='':
            aux.append(v)
    nclusters = int(aux[0])
    lbox = [float(aux[1]),float(aux[2]),float(aux[3])]
    clusters=[]
    for i in range(nclusters):
        #Recorremos todos los clusters
        particulas=[]
        tx = f.readline()
        tx = tx.replace('\n','')
        val = tx.split(' ')
        aux=[]
        for v in val:
            if v!='':
                aux.append(v)
        id = int(aux[0])
        npart=int(aux[1])
        for j in range(npart):
            #Recorremos todas las particulas del cluster i
            tx = f.readline()
            tx = tx.replace('\n','')
            val = tx.split(' ')
            aux=[]
            for v in val:
                if v!='':
                    aux.append(v)
            pos=[float(aux[0]),float(aux[1]),float(aux[2])]
            diam=float(aux[3])
            particulas.append(particula(pos,diam,i))
        clusters.append(cluster(particulas,npart))
    return [lbox,nclusters,clusters]

def readDataBinary(f):
    #Leemos el numero total de clusters
    s = f.read(4)
    nclusters = struct.unpack("i", s)[0]
    s = f.read(8*3)
    lbox= struct.unpack("ddd", s)
    clusters=[]
    for i in range(nclusters):
        #Recorremos todos los clusters
        particulas=[]
        s = f.read(4)
        id = struct.unpack("i", s)[0]
        s = f.read(4)
        npart = struct.unpack("i", s)[0]       
        for j in range(npart):
            #Recorremos todas las particulas del cluster i
            s = f.read(8*3)
            pos= struct.unpack("ddd", s)
            s = f.read(8)
            diam= struct.unpack("d", s)[0]
            s = f.read(8)
            print pos
            particulas.append(particula(pos,diam,i))
        clusters.append(cluster(particulas,npart))
    return [lbox,nclusters,clusters]


def printClusters(lbox,clusters):
    printBox(lbox,0.1)    
    sistema = showSystem(clusters)
    return sistema


def sizeDistribution(clusters):
    distribu=[0.00]*1001
    for cl in clusters:
        size = cl.size
        distribu[size]+=1.0
#    for i in range(len(distribu)):
#        distribu[i]/=float(len(clusters))
    distr2=[]
    for i in range(len(distribu)):
        if distribu[i]!=0:
            distr2.append([i,distribu[i]])
    return distr2



def setColors(clusters):
    colores=[]
    for i in range(len(clusters)):
        size = range(clusters[i].size)
        col = colorSize(size)
        for j in range(size):
            colores.append(col)
    return colores
    
def Habitual(name,n,sistema,nsalida):
    file = open(name,'r')
    [lbox,nclusters,clusters] = readDataBinary(file)
    if n==0:
        sistema = printClusters(lbox,clusters)
    else:
        sistema=updateSystem(clusters, sistema)
    
    os.system("import -window root -pause 1 -crop 590x590-0+50 -quality 100 "+nsalida)
    time.sleep(0.5)
    file.close()
    return sistema
#    for i in range(1):
#        [lbox,nclusters,clusters] = readDataBinary(file)
#        distribu = sizeDistribution(clusters)
#        sistema = updateSystem(clusters, sistema)


def plotAgregados(agregados,lbox):
    sistema = printClusters(lbox,agregados)
    
    
phi1='0.20'
phi2='0.2'
temp='0.0'


#dirout='/home/jcfernandez/resultados/espresso/phi'+phi1+'/T'+temp+'/RLJ/E0.1/AMPL/W0.1/CONF/'
#cuales=["0.0001","0.001","0.05",'0.20','0.50','0.70','1.0','2.0']
##cuales=["0.0001"]
#n=0
#sistema=None
#for c in cuales:
#    #name = '/home/jcfernandez/almacen02/jcfernandez/espresso/phi0.4/KLIN/T0.0/AMPL/W0.1/A'+c+'/config.bin'
#    name = '/home/jcfernandez/remote/almacen02/jcfernandez/espresso/phi'+phi2+'/RLJ/T'+temp+'/E0.1/MAG/AMPL/W0.1/A'+c+'/config.bin'
#    os.system('/home/jcfernandez/NetBeansProjects/CB/clusters/bin/Debug/clusters '+name)
#    name = 'configClusters.bin'
#    sistema=Habitual(name,n,sistema,dirout+'conf'+c+'.jpg')
#    n+=1

dirout='/home/jcfernandez/resultados/espresso/phi0.15/T0.001/KLIN/'
cuales=["0.05",'0.2','0.5','0.7','1.0','2.0']
#cuales=["2.0"]
n=0
sistema=None
name='/home/jcfernandez/remote/almacen02/jcfernandez/espresso/phi0.15/KLIN/T0.001/AMPL/W0.1/A0.0001/config.bin'
name='/home/jcfernandez/remote/cspfsc/simu/phi0.3/KLIN/MAG/AMPL/config.bin'
os.system('/home/jcfernandez/NetBeansProjects/CB/clusters/bin/Debug/clusters '+name)
name = 'configClusters.bin'
sistema=Habitual(name,n,sistema,dirout+'configuracion.jpg')
n+=1
