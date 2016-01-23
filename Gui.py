from Tkinter import *
import calendar
import Classes
import Main


# Gui initilation
master = Tk()

#Create all varables
sM = Entry(master)
sD = Entry(master)
sY = Entry(master)
eM = Entry(master)
eD = Entry(master)
eY = Entry(master)
nT = Entry(master)
t1 = Entry(master)
t2 = Entry(master)
sub = Button(master, text="Submit", command=sampleCalculation)

#Lay down objects

#Start date
Label(master, text="Start Month: ").grid(row=0, column=0)
sM.grid(row=0, column=1)
Label(master, text="Day: ").grid(row=0, column=2)
sD.grid(row=0, column=3)
Label(master, text="Year: ").grid(row=0, column=4)
sY.grid(row=0, column=5)

#End date
Label(master, text="End Month: ").grid(row=1, column=0)
eM.grid(row=1, column=1)
Label(master, text="Day: ").grid(row=1, column=2)
eD.grid(row=1, column=3)
Label(master, text="Year: ").grid(row=1, column=4)
eY.grid(row=1, column=5)

#Teachers
Label(master, text="Number of Teachers: ").grid(row=2)
nT.grid(row=2, column=1)
Label(master, text="Teacher 1: ").grid(row=3)
t1.grid(row=3, column=1)
Label(master, text="Teahcer 2: ").grid(row=4)
t2.grid(row=4, column=1)

#Submit button
sub.grid(row=5, column=2)

#End GUI loop
master.mainloop()




