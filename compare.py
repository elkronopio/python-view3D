import struct
from visual import *
import time
import sys

def binaryExtractESPRESSO(f):
    id=True
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
    return [t,nbytes,npart, nacc, lbox, posiciones,velocidades,fuerzas,diametros]

def binaryExtractC(f):
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
        posiciones.append(pos)
        velocidades.append(vel)
        fuerzas.append(force)
        diametros.append(diam)
        nbytes+=8*3*3+8
    return [t,nbytes,npart, nacc, lbox, posiciones,velocidades,fuerzas,diametros]

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
    ddd=0.5*len(xpos)
    sistema=[]
    scene.background = color.gray(0.7)
    for i in range(len(diameter)):
        if i<ddd:
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

def animate(nameE,nameC, offset, cada):
    f1 = open(nameE,'r')
    [t1,nbytes1,npart1, nacc1, lbox1, posiciones1,velocidades1,fuerzas1,diametros1]=binaryExtractESPRESSO(f1)
    f2 = open(nameC,'r')
    [t2,nbytes2,npart2, nacc2, lbox2, posiciones2,velocidades2,fuerzas2,diametros2]=binaryExtractC(f2)
    lx=lbox1[0]
    ly=lbox1[1]
    lz=lbox1[2]
    printBox([lx,ly,lz],0.1)   
    sistema = showSystem(posiciones1+posiciones2,diametros1+diametros2)
    bol =True
    count=0
    while bol:
        try:
            f1.seek(nbytes1*(offset+count))
            [t1,nbytes1,npart1, nacc1, lbox1, posiciones1,velocidades1,fuerzas1,diametros1]=binaryExtractESPRESSO(f1)
            f2.seek(nbytes2*(offset+count))
            [t2,nbytes2,npart2, nacc2, lbox2, posiciones2,velocidades2,fuerzas2,diametros2]=binaryExtractC(f2)
            lx=lbox1[0]
            ly=lbox1[1]
            lz=lbox1[2]
            print t1,t2
            updateSystem(posiciones1+posiciones2, sistema)
            time.sleep(0.005)
            count+=cada
        except:
            print 'FIN ',sys.exc_info()[0]
            bol=False
            
def animate2(nameE,nameC, offset, cada):
    f1 = open(nameE,'r')
    [t1,nbytes1,npart1, nacc1, lbox1, posiciones1,velocidades1,fuerzas1,diametros1]=binaryExtractESPRESSO(f1)
    f2 = open(nameC,'r')
    [t2,nbytes2,npart2, nacc2, lbox2, posiciones2,velocidades2,fuerzas2,diametros2]=binaryExtractESPRESSO(f2)
    lx=lbox1[0]
    ly=lbox1[1]
    lz=lbox1[2]
    printBox([lx,ly,lz],0.1)   
    sistema = showSystem(posiciones1+posiciones2,diametros1+diametros2)
    bol =True
    count=0
    while bol:
        try:
            f1.seek(nbytes1*(offset+count))
            [t1,nbytes1,npart1, nacc1, lbox1, posiciones1,velocidades1,fuerzas1,diametros1]=binaryExtractESPRESSO(f1)
            f2.seek(nbytes2*(offset+count))
            [t2,nbytes2,npart2, nacc2, lbox2, posiciones2,velocidades2,fuerzas2,diametros2]=binaryExtractESPRESSO(f2)
            lx=lbox1[0]
            ly=lbox1[1]
            lz=lbox1[2]
            print t1,t2
            updateSystem(posiciones1+posiciones2, sistema)
            time.sleep(0.0005)
            count+=cada
        except:
            print 'FIN ',sys.exc_info()[0]
            bol=False


nameC="/home/jcfernandez/eclipse/espresso/config.bin"
nameE='/home/jcfernandez/eclipse/espresso/configN0.bin'
nameC='/home/jcfernandez/remote/almacen02/jcfernandez/espresso/phi0.15/KLIN/T0.01/AMPL/W0.1/A0.5/config.bin'
nameE='/home/jcfernandez/remote/almacen02/jcfernandez/espresso/phi0.15/KLIN/T0.001/AMPL/W0.1/A0.5/config.bin'



#omega=0.5
#nconfcicloSave=100
#dt=0.0005
#periodo=(2.0*math.pi)/omega
#nconfciclo = int(periodo/dt)
#nsave=int(nconfciclo/nconfcicloSave);
#nfin=2000*nsave;
#print 'periodo:',periodo
#print nconfciclo
#print 'Salvado cada ',nsave,' configuraciones'
#print "tfinal: ",nfin*dt

offset=0
cada=3
animate2(nameE,nameC,offset, cada)

