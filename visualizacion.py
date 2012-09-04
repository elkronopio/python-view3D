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

def animate(name, tstep):
    f = open(name,'r')
    tnext=tstep
    tx = f.readline()
    tx = tx.replace('\n','')
    val = tx.split(' ')
    aux=[]
    for v in val:
        if v!='':
            aux.append(v)
    print aux
    t=float(aux[1])
    icorr=(aux[3])
    npart=int(aux[5])
    lx=float(aux[7])
    ly=float(aux[8])
    lz=float(aux[9])
    ###############################
#    npart=int(aux[7])
#    lx=float(aux[9])
#    ly=float(aux[10])
#    lz=float(aux[11])
#    tx =f.readline()
    ###############################
    printBox([lx,ly,lz],0.1)
    pos=[]
    vel=[]
    force=[]
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
        #xpos=[float(aux[0]),float(aux[1]),float(aux[2])]
        pos.append(xpos)
        vel.append([float(aux[3]),float(aux[4]),float(aux[5])])
        force.append([float(aux[6]),float(aux[7]),float(aux[8])])
        try:
            diameter.append(float(aux[9]))
        except:
            diameter.append(1.0)
    
    sistema = showSystem(pos,diameter)
    
    tx =f.readline()
            
    while tx!='':
        try:
            tx = tx.replace('\n','')
            val = tx.split(' ')
            aux=[]
            for v in val:
                if v!='':
                    aux.append(v)
            t=float(aux[1])
            icorr=(aux[3])
            npart=int(aux[5])
            lx=float(aux[7])
            ly=float(aux[8])
            lz=float(aux[9])
            ###############################
#            npart=int(aux[7])
#            lx=float(aux[9])
#            ly=float(aux[10])
#            lz=float(aux[11])
#            tx =f.readline()
            ###############################
            
            pos=[]
            vel=[]
            force=[]
            diameter=[]
            if t>=tnext:
                doit=True
                tnext+=tstep
            else:
                doit=False
            
            for i in range(npart):
                tx = f.readline()
                tx = tx.replace('\n','')
                if doit:
                    val = tx.split(' ')
                    aux=[]
                    for v in val:
                        if v!='':
                            aux.append(v)
                
                    xpos=boundary([float(aux[0]),float(aux[1]),float(aux[2])], lx,ly,lz)
                    pos.append(xpos)
                    vel.append([float(aux[3]),float(aux[4]),float(aux[5])])
                    force.append([float(aux[6]),float(aux[7]),float(aux[8])])
                    try:
                        diameter.append(float(aux[9]))
                    except:
                        diameter.append(1.0)
                
            if doit:
                updateSystem(pos, sistema)
            time.sleep(tstep)
            tx =f.readline()
        except:
            print 'FIN ',sys.exc_info()[0]
            tx=''

name ='/home/jonk/eclipse/TCLMagneticTest/config.dat'
name='/home/jonk/remote/cspfsc/jcfernandez/simulaciones/espresso/R-ShiftedLJ/phi0.2/T0.1/system.dat'
name='/home/jonk/remote/cspfsc/jcfernandez/simulaciones/espresso/R-ShiftedLJ/phi0.2/T0.1/u20/system.dat'
name='/home/jcfernandez/resultados/T1.0/KLIN/u200/AMPL/W0.7/lastconfig/systemA100.dat'
#name ='/home/jonk/Videos/phi0.2T0.1.dat'
#name=sys.argv[1]
tstep=0.1
animate(name, tstep)

