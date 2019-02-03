import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from pandas import DataFrame
import numpy as np
import time

root= tk.Tk()


fileInstance = open('demofile.txt', 'r')
text = fileInstance.read().split(",")

text_int = []
minute = []
text = text[:-1]
for i in text:
    text_int.append(int(float(i)))

for i in range(1,len(text_int)+1):
    minute.append(i)


df2 = DataFrame({'Minute':minute,'Blinks rate':text_int})

#df2.columns = ['Blink Rates']

#df2['Minute'] = [i for i in range(1,len(df2)+1)]

figure3 = plt.Figure(figsize=(5,4), dpi=100)
ax3 = figure3.add_subplot(111)
ax3.scatter(df2['Minute'],df2['Blinks rate'], color = 'g')
scatter3 = FigureCanvasTkAgg(figure3, root) 
scatter3.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
ax3.legend() 
ax3.set_xlabel('Minutes')
ax3.set_title('Your blinks per minute')


print(text_int[:])
'''
def plt_dynamic(x, y, ax, colors=['b']):
    for color in colors:
        ax.plot(x, y, color)
    fig.canvas.draw()
    
fig,ax = plt.subplots(1,1)
ax.set_xlabel('X') ; ax.set_ylabel('Y')
ax.set_xlim(0,360) ; ax.set_ylim(-1,1)
xs, ys = [], []

# this is any loop for which you want to plot dynamic updates.
# in my case, I'm plotting loss functions for neural nets
for x in range(360):
    y = np.sin(x*np.pi/180)
    xs.append(x)
    ys.append(y)
    if x % 30 == 0:
        plt_dynamic(xs, ys, ax)
        time.sleep(.2)
plt_dynamic(xs, ys, ax)
'''
root.mainloop()
