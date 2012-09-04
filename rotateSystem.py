import struct
from visual import *
import time
import sys

def binaryExtract(f, id=True):
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
        posiciones.append(pos)
        velocidades.append(vel)
        fuerzas.append(force)
        diametros.append(diam)
        nbytes+=8*3*3+8
        if id:
            nbytes+=4
    
    print diametros[5]
    return [nbytes,npart, nacc, lbox, posiciones,velocidades,fuerzas,diametros]

def showSystem(xpos,diameter):
    sistema=[]
    scene.background = color.gray(0.7)
    for i in range(len(diameter)):
        if i==7 or i==43:
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

def simetriaX(pos,lbox):
    sal=[]
    for p in pos:
        sal.append([lbox[0]-p[0],p[1],p[2]])
    return sal

def simetriaY(pos,lbox):
    sal=[]
    for p in pos:
        sal.append([p[0],lbox[1]-p[1],p[2]])
    return sal

def simetriaZ(pos,lbox):
    sal=[]
    for p in pos:
        sal.append([p[0],p[1],lbox[2]-p[2]])
    return sal

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


pos=[[9.5,9.5,9.5],[9.5,9.5,8.5],[9.5,9.5,7.5],[9.5,9.5,6.5],[9.5,9.5,5.5]]
diameter=[1.0,1.0,1.0,1.0,1.0]
lbox=[10.0,10.0,10.0]
printBox(lbox,0.1)
sistema=showSystem(pos,diameter)
pos = simetriaZ(pos,lbox)
time.sleep(1.0)
sistema = updateSystem(pos, sistema)
