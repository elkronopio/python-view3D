from visual import *

def boundary(pos, lbox):
    for i in range(len(pos)):
        for k in range(3):
            while pos[i][k]>lbox[k]:
                pos[i][k]-=lbox[k]
            while pos[i][k]<0.0:
                pos[i][k]+=lbox[k]
    return pos

def importcm(name):
    datos=[]
    for line in file(name):
        line.replace('\n','')
        val = line.split(' ')
        res=[]
        for v in val:
            if v!='':
                res.append(float(v))
        datos.append(res)
    lbox=datos[0]
    pos=datos[1::];
    #pos = boundary(pos,lbox)
    return [lbox,pos]

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

name = '/home/jonk/projects/sizes/poscm.dat'
[lbox,datos] = importcm(name)
print datos
#printBox(lbox,0.1)
for i in range(len(datos)):
    ball = sphere (pos=datos[i], radius=1.0, color = color.red ,material=materials.rough)