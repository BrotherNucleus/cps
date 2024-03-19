import matplotlib.pyplot as plt
import numpy as np


class graph:
    def __init__(self):
          self.show = True
    def displayGraph(self, result, A, t):
         
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