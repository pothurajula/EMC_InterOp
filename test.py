#from tkinter import *
import tkinter as tk
from tkinter import filedialog
import test2

def show():
    label.config(text=values_inside.get())


def browseFiles():
    filename = filedialog.askopenfilename(initialdir="/", title="Select a File", filetypes=(("Text files","*.txt*"),("all files","*.*")))
    label_file_explorer.configure(text="File Opened: " + filename)
    return (filename)

def getOS(selection):
    print ("OS selected is: ", selection)

def callback(selection):
    print(topologies.get())
    return (topologies.get())

window = tk.Tk()
window.title ("InterOp Automation Suite")
window.geometry("1000x1000")

#this is dropdown menu's
os_options = ["Windows","VMWare"]
values_inside = tk.StringVar(window)
values_inside.set("Choose the OS Platform")
os_drop_down = tk.OptionMenu (window,values_inside, *os_options, command=callback)
os_drop_down.pack()
print ("output from method: ", callback)

topology_options = ["FC","iSCSI","SAS"]
topologies= tk.StringVar(window)
topologies.set("Choose the topology")
top_drop_down = tk.OptionMenu (window,topologies, *topology_options)
print (topologies.get())

top_drop_down.pack()

label_file_explorer = tk.Label(window,text="File Explorer using Tkinter",width=100, height=4,fg="blue")
button_explore = tk.Button(window,text="Host Details",command=browseFiles)
button_exit = tk.Button(window,text="Exit",command=exit)
label_file_explorer.pack()
button_explore.pack()
button_exit.pack()

button = tk.Button(window,text ="Start the Run",command=show).pack()

"""label = tk.Label( window,text = " " )
label.pack()"""


def print_answers():
    print("Selected Option: {}".format(values_inside.get()))
    return None

test2.printDetails(values_inside.get())
submit_button = tk.Button(window, text='Submit', command=print_answers)
submit_button.pack()

window.mainloop()