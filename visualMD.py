# general imports
import random, time
from multiprocessing import Process, Queue

# for matplotlib
import random
import numpy as np
import matplotlib
matplotlib.use('GTKAgg') # do this before importing pylab

import matplotlib.pyplot as plt
from matplotlib.patches import Circle


def matplotLibAnimate(q,points):

    # set up initial plot
    fig = plt.figure()
    ax = fig.add_subplot(111)


    circles = []
    for point in points:
        ax.add_patch(Circle(point,0.1))

    a_line, = ax.plot(*zip(*points))
    a_line.set_color('g')
    a_line.set_lw(2)

    currentNode = None  
    def animate(currentNode = currentNode):
        while 1:
            newNode = q.get()
            if currentNode: currentNode.remove()
            circle = Circle(newNode,0.1)
            currentNode = ax.add_patch(circle)
            circle.set_fc('r')
            fig.canvas.draw()

    # start the animation
    import gobject
    gobject.idle_add(animate)
    plt.show()

#initial points
points = ((-0.25, -1.0),(0.7, -0.7),(1,0),(0.7,1),(-0.25,1.2),(-1,0.5),(-1,-0.5),(-0.25, -1.0))
points2 = ((1,1),(2,2),(3,3),(4,4))
q = Queue()
p = Process(target = matplotLibAnimate, args=(q,points,))
p.start()

# feed animation data
n=0
while 1:
    time.sleep(0.5)
    if(n%10):
        q.put(random.sample(points2,1)[0])
    else:
        q.put(random.sample(points,1)[0])
    n+=1
    

