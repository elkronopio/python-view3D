import math
from visual import *

def esInt(val):
    if int(abs(val))-val == 0.0:
        return 1
    else:
        return 0

def updateSystem(xpos, sistema):
    sistema2=[]
    i=0
    for i in range(min(len(xpos),len(sistema))): 
        sistema[i].pos=xpos[i]
        sistema[i].trail.append(pos=sistema[i].pos)
        sistema2.append(sistema[i])
    return sistema2

def showSystem(xpos, sistema):
    system=[]
    for i in range(len(xpos)):
        #print xpos[i]
        sistema[i].pos=xpos[i]
        sistema[i].visible = True
        system.append( sistema[i])
    for i in range(len(xpos),len(sistema)):
        sistema[i].visible = False
        system.append( sistema[i])
    return system

def createSystem(npart):
    system=[]
    for i in range(npart):
        ball = sphere (pos=(0,0,0), radius=1.0, color = color.red ,material=materials.rough)
        ball.visible=False
        system.append(ball)
    return system


name='/home/jonk/simulaciones/DO/confinado/monodispersa/L1.0/poscm.dat'
name='/home/jonk/simulaciones/Espresso/confinado/polydisperse/u100/L0.2/poscm.dat'
datos=[]
pos=0
count=0
firstline=1
count=0
nconfig=1
sistema=[]
cm=[]
nconf=0
sistema = createSystem(500)
for line in file(name):
    #print nconf
    if pos<2:
        #Pasamos de las dos primeras lineas
        pass
    else:
        #Descomponemos la linea en partes
        line.replace('\n','')
        val=line.split(' ')
        res=[]
        for v in val:
            if v !='':
                res.append(float(v))
        if firstline==1:
            #Leemos la cabecera del sistema
            #tiempo, Numero de clusters, lx, ly, lz
            t=res[0]
            ncluster=int(res[1])
            lbox=[res[2],res[3],res[4]]
            cmSystem=[]
            firstline=0
            count=0
        else:
            #Leemos las propiedades de cada cluster
            #id,size,mass,xcm,ycm,zcm,percola,Dx,Dy,Dz,Dx/Dy,diammedio
            id=int(res[0])
            size=int(res[1])
            mass=res[2]
            cm=[res[3],res[4],res[5]]
            percola=int(res[6])
            Dr=[res[7],res[8],res[9]]
            ratio=res[10]
            diammedio=res[11]
            rad=(Dr[0]+Dr[1])*0.5
            if percola==1:
                cmSystem.append(cm)
            count+=1
            if count==ncluster:
                #Pintamos los centros de masa
                 sistema=showSystem(cmSystem, sistema)
                 #En el siguiente paso leemos la cabecera del sistema
                 firstline=1
                 nconf+=1
    pos+=1

print "FIN"
