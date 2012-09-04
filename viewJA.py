from visual import *
import time
import sys

def getLine(line):
    line = line.replace('\n','')
    val = line.split(' ')
    aux=[]
    for v in val:
        if v!='':
            aux.append(v)
    return aux

def readData(f,npart):
    #Leemos el numero total de clusters
    line = f.readline()
    aux = getLine(line)
    t=float(aux[0])
    print t
    posiciones=[]
    diametros=[]
    #print line
    for i in range(npart):
        #Recorremos todos los clusters
        particulas=[]
        line = f.readline()
     #   print i,line
        aux = getLine(line)
        pos=[float(aux[1]),float(aux[2]),float(aux[3])]
        diam=float(aux[4])
        posiciones.append(pos)
        diametros.append(diam)
    return [t,posiciones,diametros]

def readTONTO(f,cada):
    #Leemos el numero total de clusters
    for k in range(cada):
        line = f.readline()
        for i in range(600):
            line = f.readline()

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
    print 'aaa',rad
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

def animate(name):
    f = open(name,'r')
    #line = f.readline()
    #aux = getLine(line)
    npart = 600#int(aux[0])
    #lbox=[float(aux[1]),float(aux[2]),float(aux[3])]
    [t,posiciones,diametros]=readData(f,npart)
    #lx=lbox[0]
    #ly=lbox[1]
    #lz=lbox[2]
    #printBox([lx,ly,lz],0.1)   
    sistema = showSystem(posiciones,diametros)
    bol =True
    count=0
    while bol:
        try:
            #readTONTO(f,1)
            [t,posiciones,diametros]=readData(f,npart)
            updateSystem(posiciones, sistema)
            time.sleep(0.1)
            count+=1
        except:
            print 'FIN ',sys.exc_info()[0]
            bol=False

scene2 = display(title='set Q',width=600, height=600, center=(20,20,5), background=(0.95,0.95,0.95))
name ='/home/jcfernandez/salida.dat'
#name=sys.argv[1]
animate(name)

