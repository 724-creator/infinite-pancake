import numpy as np
import matplotlib.pyplot as plt

X=np.linspace(0,10,100)
Y=np.sin(X)

fig,ax=plt.subplots()
ax.plot(X,Y,linewidth=2,color='red',label='sin(x)')
plt.show()
