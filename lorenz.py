# -*- coding: utf-8 -*-

import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits import mplot3d
import subprocess



sigma, beta, rho = 10, 8/3., 28 # parametres
#-------- equations du mouvement flot de Lorenz
def V(y,t,sigma, beta, rho):
  """The Lorenz equations."""
  V0 = -sigma*(y[0] - y[1])
  V1 = rho*y[0] - y[1] - y[0]*y[2]
  V2 = -beta*y[2] + y[0]*y[1]
  return V0,V1,V2

#--------- fonction pour section de Poincare
C=27

def f(y):
    return y[2]-C  # condition y[2] =27 et venant de y[2]>27


#--------------------------------------
"""
entree: y0 : condition initiales
        t : temps initial
        Dt : pas de temps (assez petit)

Utilise la fonction f(y) \in R qui definit la section de Poincare par f(y)=0 et passage de f>0 à f<0
Utilise la fonction dy/dt = V(y) qui definit le champ de vecteur

sortie: y: position suivante qui verifie f(y=0)
        t:  tq y =y(t)
        Ly : liste des valeurs intermediaires y(t(i) avec t(i+1) - t(i) = Dt
            contenant la premiere mais pas  la derniere

rem: t final > t initial + Dt

"""
def Application_de_Poincare(y0,t):
    #----Recherche prochain intervalle ou f change de signe ---------------------
    """
    1ere partie
    entree: y0 : condition initiales
            t : temps initial
            Dt : pas de temps (assez petit)

    sortie: Tt: intervalle en temps [t,t+Dt]
           Ty : intervalle en position [y(t), y(t+Dt)]
           tels que f(y(t))>0 et f(y(t+Dt))<0
    """
    Ty = [y0] #condition initiales encapsulee dans liste
    Ly = np.array(y0) # memorise

    #-- on passe intervalle Dt
    Tt = [t, t+Dt]
    Ty = odeint(V, y0, Tt, args=(sigma, beta, rho))
    y0 = Ty[len(Ty)-1] # coordonnees finales


    t += Dt
    f_old = f(y0)
    f_new = f_old

    while(f_old<0 or f_new >0):
        f_old = f_new
        Tt = [t, t+Dt]
        Ly = np.vstack([Ly, y0])

        Ty = odeint(V, y0, Tt, args=(sigma, beta, rho))
        y0 = Ty[len(Ty)-1] # coordonnees finales
        f_new = f(y0)
        #print ('t=',Tt[1],' y=',y0, ' f=',f_new)
        t +=Dt


    #-- dichotomie ------
    """
    2eme partie
    entree: Tt: intervalle en temps [t,t+Dt]
           Ty : intervalle en position [y(t), y(t+Dt)]
               tels que les points y(t) et y(t+Dt) sont de part et d'autre de la Section de Poincare
    """

    while((Tt[1]-Tt[0])>1e-10): # precision sur t
        tm = (Tt[0]+Tt[1])/2 #point intermediare
        Ty2 = odeint(V, Ty[0], [Tt[0],tm], args=(sigma, beta, rho))
        fm = f(Ty2[1]) # valeur intermediaire
        if(fm>0): # on conserve la 2eme moitié
            Tt[0] = tm
            Ty[0] = Ty2[1]
        else: # on conserve la 1ere moitié
            Tt[1] = tm
            Ty[1] = Ty2[1]
        #print('t0=',Tt[0], 't1=', Tt[1], 'fm=',fm)


    Ly = np.vstack([Ly, Ty[0]]) # rajoute dernier point
    return Ty[0], Tt[0], Ly  # y,t, Ly


#---------  utilisation 1
"""
    entree: y0 : condition initiales
            t : temps initial
            Dt : pas de temps (assez petit)
Sortie:   Dessin 3D des trajectoires et points d'intersection en rouge

rem: prendre Dt assez petit pour joli dessin (pas obligatoire)
"""
def Dessin_3D(y0,t,Dt):
    global tmax
    ax = plt.axes(projection = '3d')

    cpt=0 # compteur
    while(t<tmax):
        y0,t, Ly = Application_de_Poincare(y0,t)

        # ... dessin de la trajectoire intermediaire
        X, Y, Z = Ly[:,0], Ly[:,1], Ly[:,2]
        print('y=',y0, 't=',t)
        ax.plot3D(X,Y,Z, 'blue')
        angle = cpt
        ax.view_init(30, angle)

        #... dessin du point final sur section de poincare
        plt.plot([y0[0]], [y0[1]], [y0[2]],  marker='o', linestyle='none', color='red')

        plt.savefig('image_'+str(cpt).zfill(4)+'.png',dpi=70)
        plt.pause(0.1)
        cpt +=1

    #plt.show()


#--definit l'application sur R2
"""
entree x,y
sortie x2,y2
"""
def fS(x,y):
    y0 = [x,y,C] # point sur la section
    t=0 # arbitraire


    y0,t, Ly = Application_de_Poincare(y0,t)


    x2,y2 = y0[0], y0[1]
    return x2, y2

#---- calcule et dessin de la trajectoire
# entree: x,y,tmax (duree)
def dessin_trajectoire(x,y, tmax):
    Lx,Ly = [x],[y] #listes
    for t in range(tmax):
        x,y = fS(x,y) # iteration
        Lx.append(x)
        Ly.append(y)
    plt.plot(Lx,Ly, linestyle='none', marker='.', color = Lcol[col]) # marker: ',' 'o'
   # plt.show()
    plt.pause(0.001) # montre le dessin sans bloquer
    return x,y



#---- si evenement souris (clik)
def on_click(event):
    #print('click')
    global x,y, col, Lcol
    x, y = event.xdata, event.ydata # coord souris en x,y
    #x, y = event.x, event.y # coord souris en pixels
    col = (col+1) % len(Lcol)
    if event.button == 1:
            tmax = 10 # duree (tps discret)
            x,y = dessin_trajectoire(x,y, tmax)

#----- si evenement clavier
def on_key(event):
    #print('key = ', event.key)
    global x,y
   # print('you pressed', event.key, event.xdata, event.ydata)
    if event.key == ' ': # barre espace
            tmax = 10 # duree
            x,y = dessin_trajectoire(x,y, tmax)


#--------------------------
def Dessin_2D():
    global col,Lcol
    Lcol = ['blue','red', 'green', 'black', 'yellow']

    col = 0 # numero de couleur


    plt.axis([-10,10, -10, 10]) # selectionne la vue
    #plt.axis('equal') # pour avoir meme echelle en x,y
    plt.xlabel('x0')
    plt.ylabel('x1')
    plt.title("Application Poincaré du flot de Lorenz en x2 = %2.f"%C +  ' \n(cliquer pour condition initiale, et barre espace pour continuer)')
    plt.connect('button_press_event', on_click) # associe la fonction aux evenements  souris
    plt.connect('key_press_event', on_key)  # associe la fonction aux evenements clavier


    plt.show()


#--- Dessin 3D -----------

t=0 # temps initial
y0 = [0, 1, 1.05] # Conditions initiales
Dt = 0.01  # temps minimal entre deux sections
tmax = 50
Dessin_3D(y0,t,Dt)
#subprocess.getoutput('convert -delay 10 -loop 0 image_*.png animation.gif')
subprocess.getoutput('convert image_*.png GIF:- | gifsicle --delay=30 --loop --optimize=2 --colors=256 --multifile - > animation_Section_Poincare3D.gif')
subprocess.getoutput('rm image_*.png')

# ---- Dessin 2D
'''
Dt=1
Dessin_2D()
'''