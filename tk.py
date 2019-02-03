import tkinter as tk
import wx
import time
from tkinter import messagebox  

# This function will be run every N milliseconds


def showerror(string, root):
    root.geometry("600x300")  
    messagebox.showwarning("Low Blinking Alert","Warning. Please increase blink rate.")
  

def get_text(root,val,name,initial,count):
   # try to open the file and set the value of val to its contents 
   filer = open("demofile.txt", "a")
   try:
       with open(name,"r") as f:
           val.set(str(int(f.read()) - initial))
           filer.write(val.get()+",")
           if((15-int(val.get()))>8):
              count += 1
           initial = int(val.get())

           print("This is the count {}".format(count))
           if(count>4):
              count = 0
              showerror("Blink Low Alert!!!",root)
              print("Show error called")

   except IOError as e:
       print (e)
   else:
       # schedule the function to be run again after 1000 milliseconds  
       root.after(10000,lambda:get_text(root,val,name,initial,count))

root = tk.Tk()
root.minsize(0,0)
root.withdraw()


eins = tk.StringVar()
data1 = tk.Label(root, textvariable=eins)
data1.config(font=('times', 24))
data1.pack()
time.sleep(5)
get_text(root,eins,"shared_output.txt",0,0)
root.mainloop()


