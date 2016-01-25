from Tkinter import *
from tkMessageBox import *
import calendar
import Classes

def sampleCalculation():
	#Pull in Start date
	startMonth = sM.get()
	startDay = sD.get()
	startYear = sY.get()
	#Pull in Start date
	endMonth = eM.get()
	endDay = eD.get()
	endYear = eY.get()
	#Pull in amount of teachers
	numT = int(nT.get())
	#Add all posable teahers to a list
	teacherListTemp = [t1.get(),t2.get()];
	teacherList = [];
	#Create a list of actual teachers (due to limitations of gui)
	for num in range(0,numT):
		if len(teacherListTemp[num]) > 0:
			teacherList.append(teacherListTemp[num])
			
			
			
			
	##TODO
	#	Generate all weeks
	#	Week class contain day 'opbects'. Each day will need a value of if it is a day in which school is held. (default = yes)
	#	( Seperate these weeks into the 2 seperate simester lists || Add simester as a value inside of Week class )	
	#
	#	(Do needs between simesters change?)
	#
	#  	Calucate week configuration(s) for a given week of school
	#	( Calc week as normal and ignore "off days"  || Rebalance work load )
	#
	#	


	#TEST OUPUT
	print "Scheduling from ", startMonth, "/", startDay, "/", startYear, " to ", endMonth, "/", endDay, "/", endYear, "..."
	for teacher in teacherList:
		print teacher

	output = "Scheduling " + startMonth + "/" + startDay + "/" + startYear + " - " + endMonth + "/" + endDay + "/" + endYear + "..."
	showinfo("Working...", output)
	
	

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
Label(master, text="Teacher 2: ").grid(row=4)
t2.grid(row=4, column=1)

#Submit button
sub.grid(row=5, column=2)

#End GUI loop
master.mainloop()




