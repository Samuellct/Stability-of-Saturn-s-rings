# -*- coding: utf-8 -*-

import  numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
#from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits import mplot3d
import subprocess

a,b,c = 0.2, 0.2, 5.7 # parametres
y_in = [0, 1, 1.05] # Conditions initiales
tmax= 1000 # intervalle de temps
N = 100000 # nombre de points en temps

def V(y, t, a, b, c):
  """The Rossler equations."""
  V0 = -y[1] - y[2]
  V1 = y[0] + a*y[1]
  V2 = b + (y[0] -c)*y[2]
  return V0,V1,V2

t = np.linspace(0, tmax, N) # tableau de t = 0->tmax avec N valeurs
y = odeint(V, y_in, t, args=(a,b,c))


ax = plt.axes(projection = '3d')
X,Y,Z = y.T[0], y.T[1], y.T[2] # liste de points
ax.plot3D(X,Y,Z, 'blue')


# fixed points x, xp
D = c**2-4*a*b
x0 = (c + np.sqrt(D))/2
x1 = -x0/a
x2 = x0/a
print('x=',x0,x1,x2)

xp0 = (c - np.sqrt(D))/2
xp1 = -xp0/a
xp2 = xp0/a
print('xp=',xp0,xp1,xp2)

plt.plot([xp0], [xp1], [xp2],  marker='o', linestyle='none', color='red')
# rotate the axes and update

for angle in range(0, 360):
  ax.view_init(30, angle)
  plt.draw()
  plt.pause(.001) # montre image
  # plt.save('image_'+str(angle).zfill(4)+'.png',dpi=50)

#subprocess.getoutput('convert -delay 10 -loop 0 image_*.png animation.gif')
subprocess.getoutput('convert image_*.png GIF:- | gifsicle --delay=3 --loop --optimize=2 --colors=256 --multifile - > animation.gif')
subprocess.getoutput('rm image_*.png')