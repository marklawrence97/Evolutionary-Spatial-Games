"""
A programme that generates a cellular automaton with a random configuration of variables.

The programme then updates synchronously after each given time interval.

The cellular automaton is updated using a set of rules which are calculated by an arbitrary Payoff matrix.

The User has the option to input values for:

Number of variables,
Starting configuration,
Size of the cell,
Payoff matrix,
Boundary conditions,
Neighbourhood type

The user is also able to model an arbitrary behaviour strategy B "invading" a population of another arbitry strategy A, starting with one B at
center of the population

This programme should allow the user to investigate a large variety of deterministic models for spatial evolutionary games.

"""

from tkinter import *
from backendtidy import spatialGame
import time

class Window(object):
    """"This class creates a GUI using the built in python libary tkinter"""

    def __init__(self, window):
        self.window = window

        self.check = False

        self.animateval = False

        titlel=Label(window,text="Evolutionary Spatial Games", height=3)
        titlel.grid(row=0,column=0,rowspan=2)

        self.cellularAutomata=Canvas(window, height=600,width=600, background='blue')
        self.cellularAutomata.grid(row=2,column=0,rowspan="20")

        l2=Label(window,text="Payoff matrix:", width=16)
        l2.grid(row=3,column=1)

        l3=Label(window,text="Cell size: ", width=16)
        l3.grid(row=6,column=1)

        l8=Label(window,text="Moore Neighbourhood: ", width=22)
        l8.grid(row=7,column=1)

        l9=Label(window,text="Von Nuemann Neighbourhood: ", width=26)
        l9.grid(row=8,column=1)

        l4=Label(window,text="Initial Distribution: ", width=16)
        l4.grid(row=10,column=1)

        l9=Label(window,text="Fixed boundary (A): ", width=26)
        l9.grid(row=11,column=1)

        l9=Label(window,text="Reflective boundary:  ", width=26)
        l9.grid(row=12,column=1)

        l9=Label(window,text="Periodic boundary: ", width=26)
        l9.grid(row=13,column=1)

        la=Label(window,text="Count (A|B|C): ", width=16)
        la.grid(row=16,column=1)

        l5=Label(window,text="Iterations: ", width=16)
        l5.grid(row=17,column=1)

        b1=Button(window,text="Draw", command=self.draw_command)
        b1.grid(row=19,column=1)

        self.b2=Button(window,text="Start", command=self.begin_command)
        self.b2.grid(row=19,column=2)

        self.e1=Scale(window,width=8, orient=HORIZONTAL, from_=2, to=3,label="Strategies")
        self.e1.grid(row=0,column=1)

        self.e1.bind('<ButtonRelease-1>',self.change_entry)

        self.li=Label(window,text="B invades A: ", width=16)
        self.li.grid(row=14,column=1)

        self.ival = IntVar()
        self.iv = Checkbutton(window, variable=self.ival)
        self.iv.grid(row=14,column=2)

        self.ld=Label(window,text="Dynamic", width=16)
        self.ld.grid(row=15,column=1)

        self.dyval = IntVar()
        self.dyval.set(1)
        self.dy = Checkbutton(window, variable=self.dyval)
        self.dy.grid(row=15,column=2)

        self.e2=IntVar()
        self.e2=Entry(window,textvariable=self.e2,width=6)
        self.e2.grid(row=3,column=2)

        self.e3=IntVar()
        self.e3=Entry(window,textvariable=self.e3,width=6)
        self.e3.grid(row=3,column=3)

        self.e4=IntVar()
        self.e4=Entry(window,textvariable=self.e4,width=6)
        self.e4.grid(row=4,column=2)

        self.e5=IntVar()
        self.e5=Entry(window,textvariable=self.e5,width=6)
        self.e5.grid(row=4,column=3)

        self.cellsize=IntVar()
        self.cellsize.set(8)
        self.cellsize=Entry(window,textvariable=self.cellsize,width=6)
        self.cellsize.grid(row=6,column=2)

        self.p1=DoubleVar()
        self.p1=Entry(window,textvariable=self.p1,width=6)
        self.p1.grid(row=10,column=2)

        self.p2=DoubleVar()
        self.p2=Entry(window,textvariable=self.p2,width=6)
        self.p2.grid(row=10,column=3)

        self.neighbourE = IntVar()
        self.neighbourE.set(1)
        self.moore=Radiobutton(window, variable=self.neighbourE, value=1)
        self.moore.grid(row=7,column=2)

        self.nuemann=Radiobutton(window, variable=self.neighbourE, value=2)
        self.nuemann.grid(row=8,column=2)

        self.boundaryvar = IntVar()
        self.boundaryvar.set(2)
        self.fixed=Radiobutton(window, variable=self.boundaryvar, value=1)
        self.fixed.grid(row=11,column=2)

        self.reflective=Radiobutton(window, variable=self.boundaryvar, value=2)
        self.reflective.grid(row=12,column=2)

        self.periodic=Radiobutton(window, variable=self.boundaryvar, value=3)
        self.periodic.grid(row=13,column=2)

        self.a1=Listbox(window, width=4, height=1)
        self.a1.grid(row=16,column=2)

        self.a2=Listbox(window, width=4, height=1)
        self.a2.grid(row=16,column=3)

        self.i1=Listbox(window, width=4, height=1)
        self.i1.grid(row=17,column=2)

    def draw_command(self):
        self.cellularAutomata.delete("all")
        self.count=0
        self.i1.delete(0, END)
        self.i1.insert(END,self.count)
        try:
            self.b3.destroy()
            self.b2=Button(window,text="Start", command=self.begin_command)
            self.b2.grid(row=19,column=2)
        except AttributeError:
            pass
        try:
            if self.e1.get() == 2:
                matrix = [[self.e2.get(),self.e3.get()],
                          [self.e4.get(),self.e5.get()]]
                self.SpatialGame = spatialGame(600,600,
                                               self.cellsize.get(),
                                               [self.p1.get(),self.p2.get()],
                                               self.e1.get(),
                                               matrix,
                                               self.ival.get(),
                                               self.neighbourE.get(),
                                               self.boundaryvar.get(),
                                               self.dyval.get())
            if self.e1.get() == 3:
                matrix = [[self.e2.get(),self.e3.get(),self.e6.get()],
                          [self.e4.get(),self.e5.get(),self.e7.get()],
                          [self.e8.get(),self.e9.get(),self.e10.get()]]
                self.SpatialGame = spatialGame(600,600,
                                               self.cellsize.get(),
                                               [self.p1.get(),self.p2.get(),self.p3.get()],
                                               self.e1.get(),
                                               matrix,
                                               self.ival.get(),
                                               self.neighbourE.get(),
                                               self.boundaryvar.get(),
                                               self.dyval.get())
            self.cells = self.SpatialGame.cells
            for x in range(0,self.SpatialGame.width):
                for y in range(0,self.SpatialGame.height):
                    if self.cells[x][y] == 2:
                        square_coords = (x*self.SpatialGame.cell_size,
                                         y*self.SpatialGame.cell_size,
                                         x*self.SpatialGame.cell_size + self.SpatialGame.cell_size,
                                         y*self.SpatialGame.cell_size + self.SpatialGame.cell_size)
                        self.cellularAutomata.create_rectangle(square_coords, fill="red", outline="red")
                    if self.SpatialGame.cells[x][y] == 3:
                        square_coords = (x*self.SpatialGame.cell_size,
                                         y*self.SpatialGame.cell_size,
                                         x*self.SpatialGame.cell_size + self.SpatialGame.cell_size,
                                         y*self.SpatialGame.cell_size + self.SpatialGame.cell_size)
                        self.cellularAutomata.create_rectangle(square_coords, fill="pink", outline="pink")
        except ValueError:
            self.cellularAutomata.create_text(300,300,fill="White",font="Times 20 bold",
                    text="Your probability distribution must add to 1.")


    def begin_command(self):
        self.animateval = True
        self.animate()

    def next(self):
        self.cellularAutomata.delete("all")
        self.SpatialGame.run_rules()
        self.cells = self.SpatialGame.cells
        self.count = self.count + 1
        self.i1.delete(0, END)
        self.i1.insert(END,self.count)
        self.b2.destroy()
        self.b3=Button(window,text="Stop", command=self.stop_command)
        self.b3.grid(row=19,column=2)
        self.animateval = True
        for x in range(0,self.SpatialGame.width):
            for y in range(0,self.SpatialGame.height):
                if self.cells[x][y] == 2:
                    square_coords = (x*self.SpatialGame.cell_size,
                                     y*self.SpatialGame.cell_size,
                                     x*self.SpatialGame.cell_size + self.SpatialGame.cell_size,
                                     y*self.SpatialGame.cell_size + self.SpatialGame.cell_size)
                    self.cellularAutomata.create_rectangle(square_coords, fill="red", outline="red")
                if self.cells[x][y] == 4:
                    square_coords = (x*self.SpatialGame.cell_size,
                                     y*self.SpatialGame.cell_size,
                                     x*self.SpatialGame.cell_size + self.SpatialGame.cell_size,
                                     y*self.SpatialGame.cell_size + self.SpatialGame.cell_size)
                    self.cellularAutomata.create_rectangle(square_coords, fill="green", outline="green")
                if self.cells[x][y] == 5:
                    square_coords = (x*self.SpatialGame.cell_size,
                                     y*self.SpatialGame.cell_size,
                                     x*self.SpatialGame.cell_size + self.SpatialGame.cell_size,
                                     y*self.SpatialGame.cell_size + self.SpatialGame.cell_size)
                    self.cellularAutomata.create_rectangle(square_coords, fill="yellow", outline="yellow")
                if self.cells[x][y] == 3:
                    square_coords = (x*self.SpatialGame.cell_size,
                                     y*self.SpatialGame.cell_size,
                                     x*self.SpatialGame.cell_size + self.SpatialGame.cell_size,
                                     y*self.SpatialGame.cell_size + self.SpatialGame.cell_size)
                    self.cellularAutomata.create_rectangle(square_coords, fill="pink", outline="pink")
                if self.cells[x][y] == 6:
                    square_coords = (x*self.SpatialGame.cell_size,
                                     y*self.SpatialGame.cell_size,
                                     x*self.SpatialGame.cell_size + self.SpatialGame.cell_size,
                                     y*self.SpatialGame.cell_size + self.SpatialGame.cell_size)
                    self.cellularAutomata.create_rectangle(square_coords, fill="purple", outline="purple")
        self.a1.delete(0, END)
        self.a1.insert(END,self.SpatialGame.stratA)
        self.a2.delete(0, END)
        self.a2.insert(END,self.SpatialGame.stratB)
        try:
            self.a3.delete(0, END)
            self.a3.insert(END,self.SpatialGame.stratC)
        except:
            pass

    def change_entry(self, event):
        if self.e1.get() == 3 and self.check == False:
            self.check = True
            self.e6=IntVar()
            self.e6=Entry(window,textvariable=self.e6,width=6)
            self.e6.grid(row=3,column=4)
            self.e7=IntVar()
            self.e7=Entry(window,textvariable=self.e7,width=6)
            self.e7.grid(row=4,column=4)
            self.e8=IntVar()
            self.e8=Entry(window,textvariable=self.e8,width=6)
            self.e8.grid(row=5,column=2)
            self.e9=IntVar()
            self.e9=Entry(window,textvariable=self.e9,width=6)
            self.e9.grid(row=5,column=3)
            self.e10=IntVar()
            self.e10=Entry(window,textvariable=self.e10,width=6)
            self.e10.grid(row=5,column=4)
            self.p3=DoubleVar()
            self.p3=Entry(window,textvariable=self.p3,width=6)
            self.p3.grid(row=10,column=4)
            self.li.destroy()
            self.iv.destroy()
            self.ival = IntVar()
            self.ival.set(0)
            self.a3=Listbox(window, width=4, height=1)
            self.a3.grid(row=16,column=4)
        elif self.e1.get() ==2 and self.check == True:
            self.li=Label(window,text="B invades A: ", width=16)
            self.li.grid(row=14,column=1)
            self.ival = IntVar()
            self.iv = Checkbutton(window, variable=self.ival)
            self.iv.grid(row=14,column=2)
            self.check = False
            self.e6.destroy()
            self.e7.destroy()
            self.e8.destroy()
            self.e9.destroy()
            self.e10.destroy()
            self.p3.destroy()
            self.a3.destroy()

    def stop_command(self):
        self.animateval = False
        self.b3.destroy()
        self.b2=Button(window,text="Start", command=self.begin_command)
        self.b2.grid(row=19,column=2)

    def animate(self):
        while self.animateval == True:
            self.next()
            self.window.update()
            time.sleep(0.5)

window=Tk()
Window(window)
window.mainloop()
