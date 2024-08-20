import tkinter
import tkinter as ttk
from tkinter import *

root = tkinter.Tk()
root.title("Tk dropdown example")

# Add a grid
mainframe = tkinter.Frame(root)
mainframe.grid(column=0, row=0, sticky=(tkinter.N, tkinter.W, tkinter.E, tkinter.S))
mainframe.columnconfigure(0, weight = 1)
mainframe.rowconfigure(0, weight = 1)
mainframe.pack(pady = 100, padx = 100)

# Create a Tkinter variable
tkvar = tkinter.StringVar(root)

# Dictionary with options
choices = { 'PYTHON','C','C++','PHP','JAVA'}
tkvar.set('PYTHON') # set the default option

popupMenu = tkinter.OptionMenu(mainframe, tkvar, *choices)
tkinter.Label(mainframe, text="Choose Programming Language").grid(row = 1, column = 1)
popupMenu.grid(row = 2, column =1)

# on change dropdown value
def change_dropdown(*args):
    print( tkvar.get() )

# link function to change dropdown
tkvar.trace('w', change_dropdown)

root.mainloop()