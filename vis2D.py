# Sample Python/Pygame Programs
# Simpson College Computer Science
# http://cs.simpson.edu
 
# Import a library of functions called 'pygame'
import pygame
import random

def importData(f):
    ly=500.0
    tx = f.readline()
    tx = tx.replace('\n','')
    val = tx.split(' ')
    aux=[]
    for v in val:
        if v!='':
            aux.append(v)
    npart = int(aux[0])
    conv=ly/float(aux[1])
    lbox=[int(float(aux[1])*conv),int(float(aux[2])*conv)]
    pos=[]
    diametro=[]
    
    for i in range(npart):
        tx = f.readline()
        tx = tx.replace('\n','')
        val = tx.split(' ')
        aux=[]
        for v in val:
            if v!='':
                aux.append(v)
    
        #xpos=boundary([float(aux[0]),float(aux[1]),float(aux[2])], lbox)
        xpos=[int(float(aux[0])*conv),int(lbox[1]-float(aux[1])*conv)]
        pos.append(xpos)
        diametro.append(int(0.5*float(aux[2])*conv))
    return [pos,lbox, diametro]
 
# Initialize the game engine
pygame.init()
 
black = [ 255, 255, 255]
white = [255,0,0]
 



name='/home/jcfernandez/NetBeansProjects/dipolar2D/bidimensional.txt'
f = open(name,'r')
[pos,lbox, diametro] = importData(f)

# Create an empty array
star_list=pos

# Set the height and width of the screen
size=lbox
screen=pygame.display.set_mode(size)
pygame.display.set_caption("Snow Animation")

 
clock = pygame.time.Clock()
 
#Loop until the user clicks the close button.
done=False
okimport=True
while done==False:
 
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done=True # Flag that we are done so we exit this loop
 
    # Set the screen background
    
    while okimport:
        try:
            screen.fill(black)
            clock.tick(1000)
            [pos,lbox, diametro] = importData(f)
        #    # Process each particle in the list
            for i in range(len(pos)):
        #        # Draw the particle
                pygame.draw.circle(screen,white,pos[i],diametro[i])
        
                     
            # Go ahead and update the screen with what we've drawn.
            pygame.display.flip()
            #time.sleep(0.001)
        except:
            okimport = False
            done==True
    clock.tick(50)
             
# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit ()