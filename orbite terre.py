import numpy as np
import matplotlib.pyplot as plt

# initialisation des constantes
#ra=rayon aphélie
#rb=rayon périphélie

ra=152093407000
rb=147093407000
a=(ra+rb)/2

#masse de la terre
mt=5.92*10**24

#masse du soleil
ms=1.9884*10**30

#constante gravitationnelle
G=6.6742*10**(-11)

va=28851 #vitesse aphélie

ax=[]
ay=[]
az=[]

vx=[0]
vy=[va]


x=[ra]
y=[0]



d=1

F=G*ms/(d**2)

theta=0

t=np.linspace(0,365*24*3600,365*24)
dt=1/10
for k in range(300000000):
    print(k)



    d=(x[k]**2+y[k]**2)**0.5

    F=G*ms/(d**2)



    theta=np.abs(np.arctan(y[k]/x[k]))


    if x[k]<=0:
        if y[k]>=0:
            ax.append(F*np.cos(theta))
            ay.append(-F*np.sin(theta))

        if y[k]<0:
            ax.append(F*np.cos(theta))
            ay.append(F*np.sin(theta))
    if x[k]>0:
        if y[k]>=0:
            ax.append(-F*np.cos(theta))
            ay.append(-F*np.sin(theta))
        if y[k]<0:
            ax.append(-F*np.cos(theta))
            ay.append(F*np.sin(theta))





    vx.append(vx[k]+dt*ax[k])
    vy.append(vy[k]+dt*ay[k])



    x.append(x[k]+dt*vx[k])
    y.append(y[k]+dt*vy[k])



    plt.scatter(0,0,s=50,c='black',marker='+')
    plt.axis([-2*10**11,2*10**11,-2*10**11,2*10**11])
    plt.plot(x,y)

    plt.pause(0.01)
plt.show()