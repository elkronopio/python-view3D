import struct
import povexport
from visual import *
import time
import sys
import math
from pylab import *
import numpy as np

def histogram(minValue,maxValue,values, nhist):
    #maxValue=2.5#max(values)
    #minValue=-1.0#min(values)
    suma=0.0
    
    dist = np.zeros((nhist+1))
    count = np.zeros((nhist+1))
    step=(maxValue-minValue)/float(nhist)
    for val in values:
        if val>=minValue and val<=maxValue:
            dnd=int(math.floor((val-minValue)/step))
            dist[dnd]+=val
            count[dnd]+=1.0
    
    #Normalizacion
    for i in range(1,len(count)):
        suma+=step*(count[i]+count[i-1])*0.5
    x=[]
    y=[]
    for i in range(len(count)):
        x.append(minValue+float(i+0.5)*step)
        #y.append(count[i]/suma)
        y.append(count[i])
    return [x,y]

def anint(x, lx):
    lhx=0.5*lx;
    while x>lhx:
        x-=lx
    while x<-lhx:
        x+=lx
    return x

def distancia(lbox,pos1,pos2):
    dis2=0
    drx=pos2[0]-pos1[0]
    drx=anint(drx,lbox[0])
    dry=pos2[1]-pos1[1]
    dry=anint(dry,lbox[1])
    drz=pos2[2]-pos1[2]
    drz=anint(drz,lbox[2])
    dis2=drx*drx+dry*dry+drz*drz
    return  [math.sqrt(dis2),drx,dry,drz]

def binaryExtract(f,nenlaces):
    s = f.read(4)
    npart = struct.unpack("i", s)[0]
    s = f.read(8*3)
    lbox= struct.unpack("ddd", s)
    posiciones=[]
    distancias=[]
    theta=[]
    RGB=[]
    #Comienza el bucle sobre el numero de particulas
    for i in range(nenlaces):
        #Extraemos las posiciones
        s = f.read(8*3)
        pos= struct.unpack("ddd", s)
        #Extraemos las distancias
        s = f.read(8*3)
        dis= struct.unpack("ddd", s)
        #Extraemos el angulo theta
        s = f.read(8)
        zeta= struct.unpack("d", s)[0]
        #Extraemos los colores
        s = f.read(8*3)
        color= struct.unpack("ddd", s)
        posiciones.append(pos)
        distancias.append(dis)
        RGB.append(color)
        theta.append(zeta)
    return [npart, lbox, posiciones,distancias,theta,RGB]

def numeroEnlaces(f):
    nenlaces = int(f.readline())
    return nenlaces

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
    #pos[2]=Lboundary(pos[2],lz)
    return pos

def showSystem(xpos,diameter):
    sistema=[]
    scene.background = color.gray(0.7)
    for i in range(len(diameter)):
        ball = sphere (pos=xpos[i], radius=diameter[i]*0.5, color = color.red ,material=materials.rough)
        sistema.append(ball)
    return sistema

def updateSystem(xpos, sistema):
    sistema2=[]
    i=0
    for ball in sistema:
        ball.pos=xpos[i]
        sistema2.append(ball)
        i+=1
    return sistema2

def printBox(lbox,rad):
    lx=lbox[0]
    ly=lbox[1]
    lz=lbox[2]

    
    scene2 = display(title='set Q',width=600, height=600, center=(0.5*lx,0.5*ly,0.5*lz), background=(0.95,0.95,0.95))
    scene2.range = 2
    L0 = scene.lights[0]
    L0.color = 0.9*vector(L0.color)
    scene2.lights = [L0]
    d = L0.direction
    L1 = distant_light(direction=(lx,-ly,0),       color=L0.color)
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
    
    right = scene2.forward.cross(scene2.up).norm() # unit vector to the right
    newforward = vector(scene2.forward)
    newforward = rotate(newforward, angle=math.pi/4.0, axis=right)
    #newforward = rotate(newforward, angle=math.pi/4.0, axis=scene.up)
    scene2.forward = newforward
    
    scene.range = 2
    scaling = 6.5
    newrange = scaling*scene2.range.y
    scene2.range = newrange
    return scene2

def putzeros(num):
    if num<10:
        xxx='0000'+str(num)
    elif num>=10 and num<100:
        xxx='000'+str(num)
    elif num>=100 and num<1000:
        xxx='00'+str(num)
    elif num>=1000 and num<10000:
        xxx='0'+str(num)
    elif num>=10000:
        xxx=''+str(num)
    return xxx

def animate(name):
    f = open(name,'r')
    [npart, nacc, lbox, posiciones,velocidades,fuerzas,diametros]=binaryExtract(f)
    lx=lbox[0]
    ly=lbox[1]
    lz=lbox[2]
    printBox([lx,ly,lz],0.1)   
    sistema = showSystem(posiciones,diametros)
    bol =True
    while bol:
        try:
            [npart, nacc, lbox, posiciones,velocidades,fuerzas,diametros]=binaryExtract(f)
            lx=lbox[0]
            ly=lbox[1]
            lz=lbox[2]
            updateSystem(posiciones, sistema)
            #time.sleep(0.05)
        except:
            print 'FIN ',sys.exc_info()[0]
            bol=False

def colorAngle(theta):
    if (theta<=20.0) or (theta>=160.0):
        return (1,0,0)
    if (theta>20.0 and theta<=50.0) or (theta >=130.0 and theta<160.0):
        return (0,1,0)
    if (theta>50.0 and theta<=80.0) or (theta >=100.0 and theta<130.0):
        return (0,0,1)
    if (theta>80.0 and theta<100.0):
        return (1,0,1)

viewHistogram=False
viewRepre=True
bins=180
dir='/home/jcfernandez/remote/almacen01/jcfernandez/simulaciones/espresso/R-ShiftedLJ/phi0.2/T1.0/KLIN/u200/AMPL/W0.7/A100.0/'
nomeEnlace='enlaces.dat'
nomeBin='enlaces.bin'
fenlace = open(dir+nomeEnlace,'r')
fbin = open(dir+nomeBin,'r')
cosas=[]
nenlaces=numeroEnlaces(fenlace)
[npart, lbox, pos,dis,theta,RGB]=binaryExtract(fbin,nenlaces)
if viewRepre:
    scene = printBox([lbox[0],lbox[1],lbox[2]],0.1) 
if viewHistogram:
    ion()
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
Nold=0


count=0
for kkk in range(1000):
    
    nenlaces=numeroEnlaces(fenlace)
    [npart, lbox, pos,dis,theta,RGB]=binaryExtract(fbin,nenlaces)  
    angulos=[]
    for ang in theta:
        angulos.append(ang*180.0/math.pi)
        angulos.append(180.0-ang*180.0/math.pi)
    if kkk==0:
        if viewRepre:
            for i in range(len(pos)):
                rod = cylinder(pos=tuple(pos[i]), axis=tuple(dis[i]), radius=0.1)
                rod.color = tuple(RGB[i])
                cosas.append(rod)
        if viewHistogram:
            [x,y]=histogram(0.0,180.0,angulos, bins)
            ax.bar(x,y)
            x1=x[:]
            y1=y[:]
            ax.plot(x1,y1,'r-')
            draw()
            
    else:
        if viewRepre:
#            right = scene.forward.cross(scene.up).norm() # unit vector to the right
#            newforward = vector(scene.forward)
#            newforward = rotate(newforward, angle=0.05, axis=right)
#            newforward = rotate(newforward, angle=0.05, axis=scene.up)
#            scene.forward = newforward
            for dt in cosas:
                dt.visible=False
                del dt
            for i in range(len(pos)):
                ttt=theta[i]*180.0/math.pi
                rod = cylinder(pos=tuple(pos[i]), axis=tuple(dis[i]), radius=0.1)
                rod.color =colorAngle(ttt)
                cosas.append(rod)
            count+=1
            
            povexport.export(display=scene, filename=dir+"images/image"+putzeros(count)+".pov")
            
        if viewHistogram:
            angulos=[]
            for ang in theta:
                angulos.append(ang*180.0/math.pi)
                angulos.append(180.0-ang*180.0/math.pi)
            [x,y]=histogram(0.0,180.0,angulos, bins)
            ax.clear()
            ax.bar(x,y)
            ax.plot(x1,y1,'r-')
            draw()
                    
            
    #print count
#            if i < len(cosas):
#                cosas[i].pos=tuple(pos[i])
#                cosas[i].axis=tuple(dis[i])
#                cosas[i].color=tuple(RGB[i])
#                cosas[i].visible=True
#            else:
#                rod = cylinder(pos=tuple(pos[i]), axis=tuple(dis[i]), radius=0.1)
#                rod.color = tuple(RGB[i])
#                cosas.append(rod)
#            count+=1
#            if count <Nold:
#                for i in range(count,Nold):
#                    cosas[i].visible=False
                
    time.sleep(0.2)
fenlace.close()
fbin.close()

