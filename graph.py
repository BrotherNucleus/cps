import matplotlib.pyplot as plt
import numpy as np


class graph:
    def __init__(self):
          self.show = True
    def displayGraph(self, result, A, t):
         
        if(A < 1.0):
            A = 1.0

        plt.style.use('default')

        # make data
        x = result[:, [0]]
        y = result[:, [1]]

        # plot
        fig, ax = plt.subplots()

        ax.plot(x, y, linewidth=2.0)

        ax.set(xlim=(0, t), xticks=np.arange(0, t),
        ylim=(-1.2*A, 1.2*A), yticks=np.arange(-1.2*A, 1.2*A))

        plt.show()
    
    def displayHist(self, result, n):
        plt.style.use('default')

        # make data
        max = 0
        min = 0
        for check in result:
            if(check[1] >= max):
                max = check[1]
            if(check[1] <= min):
                min = check[1]
        
        len = max - min
        seg = len / (n - 1)

        values = np.zeros(n)

        for k in range(n):
            for check in result:
                if(check[1] <= min + seg*k and check[1] > min + seg*(k+1)):
                    values[k] += 1
        print(min)
        print(max)
        print(values)