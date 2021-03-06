from visual import *
import time
import sys


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

def showSystem(xpos,diameter):
    sistema=[]
    scene.background = color.gray(0.7)
    for i in range(len(diameter)):
        ball = sphere (pos=xpos[i], radius=diameter[i]*0.5, color = color.red ,material=materials.rough)
        #ball = sphere (pos=xpos[i], radius=10./18., color = color.red ,material=materials.rough)
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


def importa(f,ok):
    tx = f.readline()
    tx = tx.replace('\n','')
    val = tx.split(' ')
    aux=[]
    for v in val:
        if v!='':
            aux.append(v)
    npart=int(aux[0])
    lx=float(aux[4])
    ly=float(aux[5])
    lz=float(aux[6])
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
        xpos=boundary([float(aux[0]),float(aux[1]),float(aux[2])], lx,ly,lz)
        
        pos.append(xpos)
        try:
            diameter.append(float(aux[9]))
        except:
            diameter.append(1.0)
    return [pos,diameter,[lx,ly,lz]]

def animate(name, tstep):
    f = open(name,'r')
    [pos,diameter,lbox] = importa(f,False)
    printBox(lbox,0.1)
    sistema = showSystem(pos,diameter)
    count=1
    ok=True
    while ok:
        try:
            [pos,diameter,lbox] = importa(f,True)
            updateSystem(pos, sistema)
            time.sleep(0.01)
            count+=1
        except:
            print 'FIN '
            ok=False
            f.close()


name='/home/jcfernandez/NetBeansProjects/dinamicamolecular/system_bk.dat'
tstep=0.1
animate(name, tstep)

