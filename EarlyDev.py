from Tkinter import *
from tkMessageBox import *
import tkSimpleDialog
import tkFileDialog
from Classes import *
import xlwt
import tkMessageBox



"""Global Variables"""
SAVELOCATION = ""
ScheduleType = ""
NumTeachers = ""
Teachers = []
BlockCount = ""
BlockTimes = []
BlockDoW = []
LunchBlock = ""
SubCount = ""
Subjects = []
"""End Variables """


def printSchedule(sheet):
	"""
	Prints schedule to an xls file.1
	:param sheet: xls being written to
	:return: Nothing
	"""
	style = xlwt.easyxf("font: bold 1")
	style2 = xlwt.XFStyle()
	style2.alignment.wrap = 1
	#Fill times
	for x in range(0,BlockCount):
		if x == LunchBlock -1:
			sheet.write(x+1,0, "Lunch: " + str(BlockTimes[x]), style)
		else:
			sheet.write(x+1,0, BlockTimes[x], style)
	#Teacher
	for x in range(0,NumTeachers):
		#Write name x
		sheet.write(0,x+1, Teachers[x].name, style)
		#Write Block y for Teacher X
		for y in range(0,BlockCount):
			tempString = ""
			#build parts of day Z
			for z in Teachers[x].schedule[y].part:
				tempString += str(z.doW + "  :  " + z.subject + "\n")

			#print (tempString)
			sheet.write(y+1,x+1, tempString, style2)


def saveSettings(workbook):
	"""
	Save schedule settings to xls file
	:param workbook: xls. file
	:return: nothing
	"""

	dataInput = workbook.add_sheet("User Input")
	dataInput.col(0).width = 256*25
	dataInput.col(1).width = 256*20
	dataInput.col(3).width = 256*15
	#FrameWork
	style = xlwt.easyxf('font:bold 1')
	dataInput.write(0,0,"Type Of Schedule:", style)
	dataInput.write(1,0,"Number Of Teachers:", style)
	dataInput.write(2,0,"Number Of Blocks:", style)
	dataInput.write(3,0,"Lunch Block:", style)
	dataInput.write(4,0,"Subject Count:", style)
	dataInput.write(5,0,"Block Times:", style)
	dataInput.write(0,3,"Teachers", style)
	dataInput.write(1,3,"Name:", style)
	dataInput.write(2,3,"Type", style)
	dataInput.write(3,3,"Designation", style)
	dataInput.write(4,3,"Start Time", style)
	dataInput.write(5,3,"End Time", style)
	dataInput.write(7,3,"Subjects", style)

	#Add Static Data
	dataInput.write(0,1,ScheduleType)
	dataInput.write(1,1,NumTeachers)
	dataInput.write(2,1,BlockCount)
	dataInput.write(3,1,LunchBlock)
	dataInput.write(4,1,SubCount)

	#Add Teachers
	for x in range(0,NumTeachers):
		dataInput.write(1,x+4,Teachers[x].name)
		dataInput.write(2,x+4,Teachers[x].type)
		dataInput.write(3,x+4,Teachers[x].designation)
		dataInput.write(4,x+4,Teachers[x].startTime)
		dataInput.write(5,x+4,Teachers[x].endTime)

	#Add Block times
	for x in range(0,BlockCount):
		dataInput.write(x+6,0,"Block "+ str(x+1))
		dataInput.write(x+6,1,BlockTimes[x])
		dataInput.write(x+6,2,BlockDoW[x])

	#Add Subjects
	for x in range(0,SubCount):
		dataInput.write(x+7,4,Subjects[x])


def ParseBlocks():
	"""
	Parses the blocks to generate the proper structure for the schedule
	:return: Nothing
	"""
	tempSchedule = [ Block() for i in range(BlockCount)]

	#For Each block in the day
	for x in range(0,BlockCount):
		tempSchedule[x].time = BlockTimes[x]

		#Get days of week's as entrys in a list
		tempString = BlockDoW[x].split("/")
		tempSchedule[x].part = [Day() for i in range(len(tempString))]

		#For each doW
		for y in range(0,len(tempString)):
			tempSchedule[x].part[y].doW = tempString[y]

	for teacher in Teachers:
		teacher.schedule = tempSchedule


def Generate():
	"""
	Prints settings file here
	Would call the generation method, but we were unable to achieve that.
	:return: Nothing
	"""
	ParseBlocks()

	"""Save Book"""
	workbook = xlwt.Workbook()
	scheduleSheet = workbook.add_sheet("Schedule")
	printSchedule(scheduleSheet)
	saveSettings(workbook)
	workbook.save(SAVELOCATION)
	tkMessageBox.showinfo("Information", "No math classes detected.\nOK to continue")


def getSubjects():
	"""
	GUI to get subject lists
	:return: Nothing
	"""
	def addSubject():
		global Subjects
		Subjects = []
		for x in range(0,SubCount):
			Subjects.append(Subs[x].get())
		slave3.destroy()
		Generate()
	"""End Sub"""

	global SubCount
	global Subjects
	Subs = []

	SubCount = tkSimpleDialog.askinteger("Sub", "How Many Subjects do we Have?", initialvalue= SubCount)

	#pad Subject[] for prepop and adding subjects
	while len(Subjects) < SubCount:
		Subjects.append("")

	slave3 = Tk()
	Label(slave3,text="Subjects:").grid(row=0, column=0)
	for x in range(0,SubCount):
		prepop = Entry(slave3)
		prepop.insert(0, Subjects[x])
		Subs.append(prepop)
		Subs[x].grid(row=x+1, column=0)

	sub = Button(slave3, text="Submit", command=lambda : addSubject())
	sub.grid(row=SubCount+1, column=1)


def getBlocks():
	"""
    GUI to ask for block settings
    :return: Nothing
	"""
	def addBlock():
		global BlockTimes
		global BlockDoW
		BlockTimes = []
		BlockDoW = []
		for x in range(0,BlockCount):
			BlockTimes.append(Times[x].get())
			BlockDoW.append(DayStructure[x].get())

		slave2.destroy()
		getSubjects()

	"""End Sub"""

	global BlockCount
	global LunchBlock
	global BlockDoW
	Times = []
	DayStructure = []
	BlockCount = tkSimpleDialog.askinteger("bCount", "How Many Blocks in a day?", initialvalue=BlockCount)
	LunchBlock = tkSimpleDialog.askinteger("lunch", "Which block is lunch?", initialvalue=LunchBlock)
	while LunchBlock > BlockCount-1:
		showinfo("Error", "Lunch must be Less than Blocks in a day - 1")
		LunchBlock = tkSimpleDialog.askinteger("lunch", "Which block is lunch?")

	#Pad BlockTimes / BlockDoW for prepop if less than block cound
	while len(BlockTimes) < BlockCount:
		BlockTimes.append("")
		BlockDoW.append("")

	#Get block Times, slave2 = new window
	slave2 = Tk()
	for x in range(0,BlockCount):
		Label(slave2,text="Block " + str(x+1) +" Time: ").grid(row=x, column=0)
		prepop = Entry(slave2)
		prepop.insert(0, BlockTimes[x])
		Times.append(prepop)
		Times[x].grid(row=x, column=1)


		Label(slave2,text="Structure (Separate with /):").grid(row=x, column=2)
		prepop = Entry(slave2)
		prepop.insert(0, BlockDoW[x])
		DayStructure.append(prepop)
		DayStructure[x].grid(row=x, column=3)

	sub = Button(slave2, text="Submit", command=addBlock)
	sub.grid(row=BlockCount+1, column=1)


def getTeachers():
	"""
	GUI to ask for teacher info
	:return: Nothing
	"""
	def addTeacher():
		global Teachers
		#Clear array to account for shrink after import
		Teachers = []
		for x in range(0,NumTeachers):
			Teachers.append(Teacher())
			Teachers[x].name = Names[x].get()
			Teachers[x].type = Types[x].get()
			Teachers[x].designation = Designations[x].get()
			Teachers[x].startTime = Start[x].get()
			Teachers[x].endTime = End[x].get()

		slave.destroy()
		getBlocks()
	"""End Sub Command"""

	global NumTeachers
	global Teachers
	#Array's of tkinter objects, only way i could find to loop though them with dynamically set number of teachers
	Names = []
	Types = []
	Designations = []
	Start = []
	End = []

	#Get Number of Teachers, stored globaly
	NumTeachers = tkSimpleDialog.askinteger("NumTeachers", "How Many Teachers?", initialvalue=NumTeachers)

	#New GUI Window
	slave = Tk()

	#Pad Teachers array for prepopulation where we add teachers
	while len(Teachers) < NumTeachers:
		Teachers.append(Teacher())

	# For all Teachers, from 0 to Number of Teachers
	for x in range(0,NumTeachers):

		Label(slave, text ="Teacher " + str(x+1)).grid(row=x*6, column=0, columnspan=2, pady=5)
		Label(slave, text ="Name").grid(row=x*6+1, column=0)
		prepop = Entry(slave)
		prepop.insert(0, Teachers[x].name)
		Names.append(prepop)
		Names[x].grid(row=x*6+1,column=1)

		#Type
		Label(slave, text ="Type").grid(row=x*6+2, column=0)
		prepop = Entry(slave)
		prepop.insert(0, Teachers[x].type)
		Types.append(prepop)
		Types[x].grid(row=x*6+2,column=1)

		#Desig
		Label(slave, text ="Designation").grid(row=x*6+3, column=0)
		prepop = Entry(slave)
		prepop.insert(0, Teachers[x].designation)
		Designations.append(prepop)
		Designations[x].grid(row=x*6+3,column=1)

		#Start
		Label(slave, text ="Start Time").grid(row=x*6+4, column=0)
		prepop = Entry(slave)
		prepop.insert(0, Teachers[x].startTime)
		Start.append(prepop)
		Start[x].grid(row=x*6+4,column=1)

		#End
		Label(slave, text ="End Time").grid(row=x*6+5, column=0)
		prepop = Entry(slave)
		prepop.insert(0, Teachers[x].endTime)
		End.append(prepop)
		End[x].grid(row=x*6+5,column=1)
	#End for loop

	sub = Button(slave, text="Submit", command=addTeacher)
	sub.grid(row=NumTeachers*10, column=1)

	slave.mainloop()


def saveLocation():
	"""
	GUI to ask for save location
	:return: nothing
	"""
	global SAVELOCATION
	SAVELOCATION = str(tkFileDialog.askdirectory()) + "/"
	SAVELOCATION += (tkSimpleDialog.askstring("file", "Name of saved file"))
	SAVELOCATION += ".xls"


def setEarly():
	"""
	Sets schedual type to early dev
	:return:
	"""
	global ScheduleType
	ScheduleType = "Early Development"
	saveLocation()
	getTeachers()


def importEarlyDevSettings(sheet):
	"""
	Imports settings from an exsisting schedule
	:param sheet: settings sheet of an .xls
	:return:
	"""
	global ScheduleType
	global NumTeachers
	global Teachers
	global BlockCount
	global BlockTimes
	global LunchBlock
	global SubCount

	ScheduleType = sheet.cell(0,1).value
	NumTeachers = int(sheet.cell(1,1).value)
	BlockCount = int(sheet.cell(2,1).value)
	LunchBlock = int(sheet.cell(3,1).value)
	SubCount = int(sheet.cell(4,1).value)
	for x in range(0, BlockCount):
		BlockTimes.append(int(sheet.cell(x+6,1).value))
		BlockDoW.append(str(sheet.cell(x+6,2).value))
	for x in range(0, NumTeachers):
		Teachers.append(Teacher())
		Teachers[x].name = sheet.cell(1,x+4).value
		Teachers[x].type = sheet.cell(2,x+4).value
		Teachers[x].designation = sheet.cell(3,x+4).value
		Teachers[x].startTime = int(sheet.cell(4,x+4).value)
		Teachers[x].endTime = int(sheet.cell(5,x+4).value)
	for x in range(0, SubCount):
		Subjects.append(sheet.cell(x+7,4).value)
	saveLocation()
	getTeachers()