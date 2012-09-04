import struct
from visual import *
import time
import sys
import numpy as np

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
    momentos=[]
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
        #Extraemos los momentos
        s = f.read(8*3)
        mom= struct.unpack("ddd", s)
        
        #Extraemos el diametro
        s = f.read(8)
        diam= struct.unpack("d", s)[0]
        if id:
            #Extraemos la id de particula
            s = f.read(4)
            identity= struct.unpack("i", s)[0]
            labels.append(identity)
        posiciones.append(pos)
        momentos.append(mom)
        diametros.append(diam)
        nbytes+=8*3*3+8
        if id:
            nbytes+=4
    
    if id:
        xm=[]
        xp=[]
        xd=[]
        for i in range(len(posiciones)):
            donde=labels.index(i)
            xm.append(momentos[donde])
            xp.append(posiciones[donde])
            xd.append(diametros[donde])
        posiciones=xp
        momentos=xm
        diametros=xd
    return [nbytes,npart, nacc, lbox, posiciones,momentos,diametros]

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

def showSystem(vscale, xpos,momentos,diameter):
    sistema=[]
    scene.background = color.gray(0.7)
    for i in range(len(diameter)):
            ball = sphere (pos=xpos[i], radius=diameter[i]*0.5, color = color.red ,material=materials.rough)
            varr = arrow(pos=ball.pos, axis=vscale*np.array(momentos[i]), color=color.blue)
            sistema.append([ball,varr])
    return sistema

def updateSystem(vscale, xpos, momentos,sistema):
    sistema2=[]
    i=0
    for [ball,varr] in sistema:
        ball.pos=xpos[i]
        varr.pos=xpos[i]
        varr.axis=vscale*np.array(momentos[i])
        sistema2.append([ball,varr])
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

def animate(name, offset, cada, id=True,vscale=1):
    f = open(name,'r')
    [nbytes,npart, nacc, lbox, posiciones,momentos,diametros]=binaryExtract(f,id)
    lx=lbox[0]
    ly=lbox[1]
    lz=lbox[2]
    nnn=0
    #for p in posiciones:
    #    print nnn,p
    #    nnn+=1
    printBox([lx,ly,lz],0.1)  
    sistema = showSystem(vscale,posiciones,momentos,diametros)
    #print lbox
    bol =True
    count=0
    while bol:
        try:
            f.seek(nbytes*(offset+count))
            [nbytes,npart, nacc, lbox, posiciones,momentos,diametros]=binaryExtract(f,id)
            lx=lbox[0]
            ly=lbox[1]
            lz=lbox[2]
            updateSystem(vscale,posiciones, momentos,sistema)
            time.sleep(0.00008)
            count+=cada
            #bol=False
        except:
            print 'FIN ',sys.exc_info()[0]
            bol=False


dir='/home/jcfernandez/NetBeansProjects/espresso2'
name=dir+'/config.bin'
#name=sys.argv[1]
offset=0
cada=1
animate(name,offset, cada,True,0.01)

#f = open(name,'r')
#[nbytes,npart, nacc, lbox, posiciones,momentos,diametros] = binaryExtract(f, id=True)
#print momentos[0]
#f.close()