import struct
from visual import *
import time
import sys

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

def binaryExtract(f):
    s = f.read(8)
    t= struct.unpack("d", s)[0]
    s = f.read(4)
    nacc = struct.unpack("i", s)[0]
    s = f.read(4)
    npart = struct.unpack("i", s)[0]
    s = f.read(8*3)
    lbox= struct.unpack("ddd", s)
    posiciones=[]
    velocidades=[]
    fuerzas=[]
    diametros=[]
    #Comienza el bucle sobre el numero de particulas
    for i in range(npart):
        #Extraemos las posiciones
        s = f.read(8*3)
        pos= struct.unpack("ddd", s)
        #Extraemos las velocidades
        s = f.read(8*3)
        vel= struct.unpack("ddd", s)
        #Extraemos las fuerzas
        s = f.read(8*3)
        force= struct.unpack("ddd", s)
        #Extraemos el diametro
        s = f.read(8)
        diam= struct.unpack("d", s)[0]
        s = f.read(4)
        posiciones.append(pos)
        velocidades.append(vel)
        fuerzas.append(force)
        diametros.append(diam)
    return [npart, nacc, lbox, posiciones,velocidades,fuerzas,diametros]

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
    return scene2

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
    if (theta<=10.0) or (theta>=170.0):
        return (1,0,0)
    if (theta>10.0 and theta<=30.0) or (theta >=150.0 and theta<170.0):
        return (0,1,0)
    if (theta>30.0 and theta<=50.0) or (theta >=130.0 and theta<150.0):
        return (1,1,0)
    if (theta>50.0 and theta<=90.0) or (theta >=90.0 and theta<130.0):
        return (0,0,1)

name ='/home/jonk/remote/cspfsc/jcfernandez/simulaciones/espresso/R-ShiftedLJ/phi0.2/T0.1/u20/AMPL/W30.0/G10.0/config.bin'
name='/home/jcfernandez/remote/rperi76/simulaciones/eps1T0.1/u0/AMPL/W2.0/A200.0/config.bin'
name='/home/jcfernandez/remote/cspfsc/simulaciones/espresso/R-ShiftedLJ/phi0.2/T0.1/u70/AMPL/W2.0/A100.0/config.bin'
name='/home/jcfernandez/remote/rperi76/simulaciones/eps1T0.1/u100/AMPL/W2.0/A200.0/config.bin'
name='/home/jcfernandez/remote/almacen01/jcfernandez/simulaciones/espresso/R-ShiftedLJ/phi0.2/T0.1/u50/AMPL/W2.0/A40.0/config.bin'
name='/home/jcfernandez/remote/rperi76/simulaciones/eps1T0.1/u100/AMPL/W2.0/A10.0/config.bin'
name='/home/jcfernandez/remote/almacen02/jcfernandez/espresso/phi0.15/KLIN/T0.0/config.bin'
f = open(name,'r')
cosas=[]
[npart, nacc, lbox, pos,velocidades,fuerzas,diametros]=binaryExtract(f)
scene = printBox([lbox[0],lbox[1],lbox[2]],0.1)  
for kkk in range(1):
    print kkk
    if kkk>-1:
        [npart, nacc, lbox, pos,velocidades,fuerzas,diametros]=binaryExtract(f)  
        for i in range(npart-1):
            for j in range(i+1,npart):
                [dis,dx,dy,dz] = distancia(lbox,pos[i],pos[j])
                if dis<1.05:
                    theta = math.acos(dz/dis)*180.0/math.pi
                    col = colorAngle(theta)
                    rod = cylinder(pos=tuple(pos[i]), axis=(dx,dy,dz), radius=0.1)
                    rod.color = col
                    cosas.append(rod)
        time.sleep(5)
#        for dt in cosas:
#            dt.visible = False
#            del dt
f.close()

#time.sleep(5)
#for f in cosas:
#    f.visible = False
#    del f

