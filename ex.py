import matplotlib.pyplot as plt
import numpy as np
t=np.arange(0, 5, 0.2)
 
plt.subplot(121)
plt.plot(t, "r--")
plt.xlabel("Graph 1")
 
plt.subplot(122)
plt.plot(t, "r--", t**2, "b+", t**3, "g-o")
plt.xlabel("Graph 1")
 
plt.suptitle("Plotting Multiple Graphs")
plt.show()