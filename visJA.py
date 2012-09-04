from visual import *
import time
import sys
import povexport

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
    scene.center = vector(0.5*lx,0.5*ly,0.5*lz)
    rod = cylinder(pos=(0,0,0),axis=(lx,0,0), radius=rad)
    rod = cylinder(pos=(0,0,0),axis=(0,ly,0), radius=rad)
    rod = cylinder(pos=(0,0,0),axis=(0,0,lz), radius=rad)
    rod = cylinder(pos=(lx,0,0),axis=(0,ly,0), radius=rad)
    rod = cylinder(pos=(lx,0,0),axis=(0,0,lz), radius=rad)
    rod = cylinder(pos=(0,ly,0),axis=(0,0,lz), radius=rad)
    rod = cylinder(pos=(0,ly,0),axis=(lx,0,0), radius=rad)
    
    rod = cylinder(pos=(0,0,lz),axis=(lx,0,0), radius=rad)
    rod = cylinder(pos=(0,0,lz),axis=(0,ly,0), radius=rad)
    
    rod = cylinder(pos=(lx,ly,0),axis=(0,0,lz), radius=rad)
    rod = cylinder(pos=(lx,0,lz),axis=(0,ly,0), radius=rad)
    rod = cylinder(pos=(0,ly,lz),axis=(lx,0,0), radius=rad)

def animate(name):
    count=0
    f = open(name,'r')
    tnext=tstep
    tx = f.readline()
    tx = tx.replace('\n','')
    val = tx.split(' ')
    aux=[]
    for v in val:
        if v!='':
            aux.append(v)
    t=float(aux[0])
   # tcorr=float(aux[1])
    npart=600
    #printBox([lx,ly,lz],0.1)
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
    
        xpos=[float(aux[1]),float(aux[2]),float(aux[3])]
        pos.append(xpos)
        diameter.append(float(aux[4]))
        #diameter.append(1.0)
    
    sistema = showSystem(pos,diameter)
    
    tx =f.readline()
    #print tx
            
    while tx!='':
        try:
            tx = tx.replace('\n','')
            val = tx.split(' ')
            aux=[]
            for v in val:
                if v!='':
                    aux.append(v)
            t=float(aux[0])
          #  tcorr=float(aux[1])
            npart=600
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
            
                xpos=[float(aux[1]),float(aux[2]),float(aux[3])]
                pos.append(xpos)
                diameter.append(float(aux[4]))
                    #diameter.append(1.0)
            #time.sleep(0.05)
            updateSystem(pos, sistema)
            tx =f.readline()
        except:
            print 'FIN ',sys.exc_info()[0]
            tx=''
#
name ='/home/jonk/josetxo/josean/Polidispersidad/squeeze/0p5/run5/salida.dat'
#name=sys.argv[1]
tstep=1.0
animate(name)

