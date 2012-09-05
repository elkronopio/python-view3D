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
    line = f.readline()
    aux = getLine(line)
    t=float(aux[0])
    print 'Altura',t
    posiciones=[]
    diametros=[]
    for i in range(npart):
        particulas=[]
        line = f.readline()
        aux = getLine(line)
        pos=[float(aux[1]),float(aux[2]),float(aux[3])]
        diam=float(aux[4])
        posiciones.append(pos)
        diametros.append(diam)
    return [t,posiciones,diametros]

def showSystem(xpos,diameter,zpos):
    sistema=[]
    scene.background = color.gray(0.7)
    pcenter=(0,0,0)
    xxx,yyy,zzz=[],[],[]
    for p in xpos:
        xxx.append(p[0])
        yyy.append(p[1])
        zzz.append(p[2])
    pmax=[max(xxx)+2,max(yyy)+2,max(zzz)]
    pmin=[min(xxx)-2,min(yyy)-2,min(zzz)]
    bottom = box(pos=pcenter,  length=pmax[0]-pmin[0], height=pmax[1]-pmin[1], width=0.01, color = color.blue,opacity = 0.1)
    top = box(pos=(0,0,zpos),  length=pmax[0]-pmin[0], height=pmax[1]-pmin[1], width=0.01, color = color.blue,opacity = 0.1)
    for i in range(len(diameter)):
        ball = sphere (pos=xpos[i], radius=diameter[i]*0.5, color = color.red ,material=materials.rough)
        sistema.append(ball)
    return sistema,bottom,top

def updateSystem(xpos, sistema,top,bottom,zpos):
    sistema2=[]
    xxx,yyy,zzz=[],[],[]
    for p in xpos:
        xxx.append(p[0])
        yyy.append(p[1])
        zzz.append(p[2])
    pmax=[max(xxx)+2,max(yyy)+2,max(zzz)]
    pmin=[min(xxx)-2,min(yyy)-2,min(zzz)]
    bottom.length=pmax[0]-pmin[0]
    bottom.height=pmax[1]-pmin[1]
    
    top.pos=(0,0,zpos)
    top.length=pmax[0]-pmin[0]
    top.height=pmax[1]-pmin[1]

    i=0
    for ball in sistema:
        ball.pos=xpos[i]
        sistema2.append(ball)
        i+=1
    return sistema2,top,bottom

def animate(name,npart,vel):
    f = open(name,'r')
    [zpos,posiciones,diametros]=readData(f,npart)
    sistema,bottom,top = showSystem(posiciones,diametros,zpos)
    bol =True
    count=0
    while bol:
        try:
            [zpos,posiciones,diametros]=readData(f,npart)
            #sistema, top, bottom = 
            updateSystem(posiciones, sistema,top,bottom,zpos)
            time.sleep(vel)
            count+=1
        except:
            print 'FIN ',sys.exc_info()[0]
            bol=False

scene2 = display(title='set Q',width=600, height=600, center=(0,0,5), background=(0.95,0.95,0.95))
name ='/home/jcfernandez/Escritorio/salida.dat'
name=sys.argv[1]
npart=int(sys.argv[2])
vel=float(sys.argv[3])
#npart=50
#vel=0.001
animate(name,npart,vel)

