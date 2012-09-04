import struct
from visual import *
import time
import sys

def binaryExtract(f, id=True):
    labels=[]
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
    nbytes=8+4+4+8*3
    print 'time: ',t, nacc,npart
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
        if id:
            #Extraemos la id de particula
            s = f.read(4)
            identity= struct.unpack("i", s)[0]
            labels.append(identity)
        posiciones.append(pos)
        velocidades.append(vel)
        fuerzas.append(force)
        diametros.append(diam)
        nbytes+=8*3*3+8
        if id:
            nbytes+=4
    
    if id:
        xf=[]
        xp=[]
        xv=[]
        xd=[]
        for i in range(len(posiciones)):
            donde=labels.index(i)
            xf.append(fuerzas[donde])
            xp.append(posiciones[donde])
            xv.append(velocidades[donde])
            xd.append(diametros[donde])
        posiciones=xp
        velocidades=xv
        fuerzas=xf
        diametros=xd
    return [nbytes,npart, nacc, lbox, posiciones,velocidades,fuerzas,diametros]

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
        if i==193 or i==193:
            ball = sphere (pos=xpos[i], radius=diameter[i]*0.5, color = color.blue ,material=materials.rough)
        else:
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
    print 'aaa',lbox
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

def animate(name, offset, cada, id=True):
    f = open(name,'r')
    [nbytes,npart, nacc, lbox, posiciones,velocidades,fuerzas,diametros]=binaryExtract(f,id)
    lx=lbox[0]
    ly=lbox[1]
    lz=lbox[2]
    nnn=0
    #for p in posiciones:
    #    print nnn,p
    #    nnn+=1
    printBox([lx,ly,lz],0.1)  
    sistema = showSystem(posiciones,diametros)
    #print lbox
    bol =True
    count=0
    while bol:
        try:
            f.seek(nbytes*(offset+count))
            [nbytes,npart, nacc, lbox, posiciones,velocidades,fuerzas,diametros]=binaryExtract(f,id)
            lx=lbox[0]
            ly=lbox[1]
            lz=lbox[2]
            updateSystem(posiciones, sistema)
            time.sleep(0.05)
            count+=cada
            #bol=False
        except:
            print 'FIN ',sys.exc_info()[0]
            bol=False


dir='/home/jcfernandez/remote/josetxo/NetBeansProjects/espresso2'
name=dir+'/config.bin'
#name=sys.argv[1]
offset=0
cada=1
animate(name,offset, cada,True)

