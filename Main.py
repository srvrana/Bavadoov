from Tkinter import *
from tkMessageBox import *
import tkSimpleDialog
import tkFileDialog
#import Classes
from Classes import *
import xlwt
from xlrd import open_workbook
from MiddleSchool import *
from EarlyDev import *

def impSchedual():
	"""
	Calls the correct import method bassed upon the type of schedual, which is extracted from the input file

	:return: Nothing
	"""
	filename = tkFileDialog.askopenfilename(parent=master,title='Chose file to open')

	book = open_workbook(filename)
	sheet = book.sheet_by_name("User Input")
	ScheduleType = sheet.cell(0,1).value

	if ScheduleType == 'Middle':
		importMiddleSchoolSettings(sheet, master)
	else:
		importEarlyDevSettings(sheet)



"""
	MAIN METHOD STARTS HERE
	Button selection will set Schedual type to a string
"""

if __name__ == "__main__":

	master = Tk()
	master.minsize(width=250, height=220)
	early = Button (master, text="Early Development", command=lambda: setEarly())
	middle = Button (master, text="Middle School", command=lambda: setMiddleTest(master))
	imp = Button(master, text="Import from Exsisting", command=impSchedual)
	early.grid(row=0, column=0, ipady = 15, ipadx=75)
	middle.grid(row=1, column=0, ipady = 15, ipadx=86)
	imp.grid(row=2, column = 0, ipady = 15, ipadx=68)

	master.mainloop()
