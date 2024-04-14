import tkinter as tk
from tkinter import Canvas
from tkinter import Label
from tkinter import Entry
from tkinter import Button

window = tk.Tk()

# label = tk.Label(text="Imagine Stacker")
window.title("Image Stacking")
# window_dim = Canvas(window, width=40, height=60)
# window_dim.pack()

#window.geometry("600x400")
l1 = Label(window, text="Input Folder").grid(row=0, column=0)
e1 = Entry(window).grid(row=0, column=1)

l2 = Label(window, text="Output Folder").grid(row=1, column=0)
e2 = Entry(window).grid(row=1, column=1)
# e1.grid(row=0, column=1)
# e2.grid(row=1, column=1)
button = Button(window, text ="stack", command=print(e1.get()+str(" ")+e2.get()))
button.grid(row=2, column=1, sticky=tk.W)

# button.place(x=50,y=50)
# l1.pack()
# l2.pack()


# button = Button(window, text="stack", width = 25,  command = "python3 fits_input.py")
# button.pack()

window.mainloop()