from Tkinter import *
from tkMessageBox import *
import tkSimpleDialog
import tkFileDialog
import Classes
import xlwt
from xlrd import open_workbook

"""Global Variables"""
SAVELOCATION = ""
ScheduleType = ""
NumTeachers = 0
Teachers = []
BlockCount = 0
BlockTimes = []
BlockDoW = []
LunchBlock = 0
SubCount = 0
Subjects = []
"""End Variables """


"""
	Test method
"""
def printTestOutput():
	#Test print Data
	print ScheduleType
	for x in Teachers:
		print x.name, x.type, x.designation, x.startTime,x.endTime
	for x in range(0,BlockCount):
		if x == LunchBlock-1:
			print "LUNCH:"
		print "Block " + str(x+1) + " : " + str(BlockTimes[x])
		print "Structure = " + str(BlockDoW[x])
	print "Subjects"
	for x in Subjects:
		print x
"""
	Put teacher names and block times into outputfile
"""
def frameSchedule(sheet):
	style = xlwt.easyxf("font: bold 1")
	#Fill times
	for x in range(0,BlockCount):
		if x == LunchBlock -1:
			sheet.write(x+1,0, "Lunch: " + str(BlockTimes[x]), style)
		else:
			sheet.write(x+1,0, BlockTimes[x], style)
	#Teacher labels
	for x in range(0,NumTeachers):
		sheet.write(0,x+1, Teachers[x].name, style)
"""
	Saves user input to the xls file
"""
def saveSettings(workbook):
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
"""
	Main Generation Method
"""
def Generate():
	printTestOutput()
	workbook = xlwt.Workbook()
	scheduleSheet = workbook.add_sheet("Schedule")
	frameSchedule(scheduleSheet)
	"""Hard stuff goes here"""
	#Add settings
	saveSettings(workbook)
	workbook.save(SAVELOCATION)
	print "Saved to " + SAVELOCATION


def getSubjects():
	def addSubject():
		for x in range(0,SubCount):
			Subjects.append(Subs[x].get())
		slave3.destroy()
		master.destroy()
		Generate()
	"""End Sub"""

	global SubCount
	global Subjects
	Subs = []

	SubCount = tkSimpleDialog.askinteger("Sub", "How Many Subjects do we Have?")
	slave3 = Tk()
	Label(slave3,text="Subjects:").grid(row=0, column=0)
	for x in range(0,SubCount):
		Subs.append(Entry(slave3))
		Subs[x].grid(row=x+1, column=0)
	sub = Button(slave3, text="Submit", command=addSubject)
	sub.grid(row=SubCount+1, column=1)

"""
	Gets number of blocks in a day, which block is lunch, and dynamically asked for times for each block
"""
def getBlocks():

	"""
	Sub Command - Stores info brought in from tkinter GUI
	"""
	def addBlock():
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
	BlockCount = tkSimpleDialog.askinteger("bCount", "How Many Blocks in a day?")
	LunchBlock = tkSimpleDialog.askinteger("lunch", "Which block is lunch?")
	while LunchBlock > BlockCount-1:
		showinfo("Error", "Lunch must be Less than Blocks in a day - 1")
		LunchBlock = tkSimpleDialog.askinteger("lunch", "Which block is lunch?")

	#Get block Times, slave2 = new window
	slave2 = Tk()
	for x in range(0,BlockCount):
		Label(slave2,text="Block " + str(x+1) +" Time: ").grid(row=x, column=0)
		Times.append(Entry(slave2))
		Times[x].grid(row=x, column=1)
		Label(slave2,text="Structure (Separate with /):").grid(row=x, column=2)
		DayStructure.append(Entry(slave2))
		DayStructure[x].grid(row=x, column=3)

	sub = Button(slave2, text="Submit", command=addBlock)
	sub.grid(row=BlockCount+1, column=1)

"""
	Gets us the Number of teachers and their info
	Calls Get Blocks
"""
def getTeachers():
	"""
	Sub Command - Stores info brought in from tkinter GUI
	This info is in the Array of 'Teacher classes' named Teachers
	"""
	def addTeacher():
		for x in range(0,NumTeachers):
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
	NumTeachers = tkSimpleDialog.askinteger("NumTeachers", "How Many Teachers?")

	#New GUI Window
	slave = Tk()
	#Append a teacher class to end of Teachers[]
	Teachers.append(Classes.Teacher())
	#Populate Teacher 1
	'''Label(slave, text ="Teacher 1").grid(row=0, column=0, columnspan=2)
	#Names
	Label(slave, text ="Name").grid(row=1, column=0)
	Names.append(Entry(slave))
	Names[0].grid(row=1,column=1)

	#Type
	Label(slave, text ="Type").grid(row=2, column=0)
	Types.append(Entry(slave))
	Types[0].grid(row=2,column=1)

	#Desig
	Label(slave, text ="Designation").grid(row=3, column=0)
	Designations.append(Entry(slave))
	Designations[0].grid(row=3,column=1)

	#Start
	Label(slave, text ="Start Time").grid(row=4, column=0)
	Start.append(Entry(slave))
	Start[0].grid(row=4,column=1)

	#End
	Label(slave, text ="End Time").grid(row=5, column=0)
	End.append(Entry(slave))
	End[0].grid(row=5,column=1)'''
	# For all Teachers, from 1 to Number of Teachers
	for x in range(0,NumTeachers):
		tempEnd = ""
		tempStart = ""
		tempDesig = ""
		tempType = ""
		tempName = ""
		Teachers.append(Classes.Teacher())
		Label(slave, text ="Teacher " + str(x+1)).grid(row=x*6, column=0, columnspan=2, pady=5)
		Label(slave, text ="Name").grid(row=x*6+1, column=0)
		if(x < len(Teachers)):
			tempName = Teachers[x].name
		tempEntry = Entry(slave)
		tempEntry.insert(0, tempName)
		Names.append(tempEntry)
		Names[x].grid(row=x*6+1,column=1)
		#Type
		Label(slave, text ="Type").grid(row=x*6+2, column=0)
		if(x < len(Teachers)):
			tempType = Teachers[x].type
		tempEntry = Entry(slave)
		tempEntry.insert(0, tempType)
		Types.append(tempEntry)
		Types[x].grid(row=x*6+2,column=1)
		#Desig
		Label(slave, text ="Designation").grid(row=x*6+3, column=0)
		if(x < len(Teachers)):
			tempDesig = Teachers[x].designation
		tempEntry = Entry(slave)
		tempEntry.insert(0, tempDesig)
		Designations.append(tempEntry)
		Designations[x].grid(row=x*6+3,column=1)

		#Start
		Label(slave, text ="Start Time").grid(row=x*6+4, column=0)
		if(x < len(Teachers)):
			tempStart = Teachers[x].startTime
		tempEntry = Entry(slave)
		tempEntry.insert(0, tempStart)
		Start.append(tempEntry)
		Start[x].grid(row=x*6+4,column=1)

		#End
		Label(slave, text ="End Time").grid(row=x*6+5, column=0)
		if(x < len(Teachers)):
			tempEnd = Teachers[x].endTime
		tempEntry = Entry(slave)
		tempEntry.insert(0, tempEnd)
		End.append(tempEntry)
		End[x].grid(row=x*6+5,column=1)
	#End for loop

	sub = Button(slave, text="Submit", command=addTeacher)
	sub.grid(row=NumTeachers*10, column=1)

	slave.mainloop()


def saveLocation():
	global SAVELOCATION
	SAVELOCATION = str(tkFileDialog.askdirectory()) + "/"
	SAVELOCATION += (tkSimpleDialog.askstring("file", "Name of saved file"))
	SAVELOCATION += ".xls"
"""
	Sets Schedual Type to "Early" (childhood)
	Calls getTeachers
"""
def setEarly():
	global ScheduleType
	ScheduleType = "Early Development"
	saveLocation()
	getTeachers()

"""
	Sets Schedual Type to "Grade School"
	Calls getTeachers
"""
def setGrade():
	global ScheduleType
	ScheduleType = "Grade"
	saveLocation()
	getTeachers()

"""
	Import from an existing schedule
"""
def impSchedual():
	global ScheduleType
	global NumTeachers
	global Teachers
	global BlockCount
	global BlockTimes
	global LunchBlock
	global SubCount
	filename = tkFileDialog.askopenfilename(parent=master,title='Chose file to open')

	book = open_workbook(filename)
	sheet = book.sheet_by_name("User Input")
	ScheduleType = sheet.cell(0,1).value
	NumTeachers = int(sheet.cell(1,1).value)
	BlockCount = int(sheet.cell(2,1).value)
	LunchBlock = int(sheet.cell(3,1).value)
	SubCount = int(sheet.cell(4,1).value)

	for x in range(0, BlockCount):
		BlockTimes.append(int(sheet.cell(x+6,1).value))
		BlockDoW.append(str(sheet.cell(x+6,2).value))

	for x in range(0, NumTeachers):
		Teachers.append(Classes.Teacher())
		Teachers[x].name = sheet.cell(1,x+4).value
		Teachers[x].type = sheet.cell(2,x+4).value
		Teachers[x].designation = sheet.cell(3,x+4).value
		Teachers[x].startTime = int(sheet.cell(4,x+4).value)
		Teachers[x].endTime = int(sheet.cell(5,x+4).value)

	for x in range(0, SubCount):
		Subjects.append(sheet.cell(x+7,4).value)

	saveLocation()
	getTeachers()
	Generate()

"""
	MAIN METHOD STARTS HERE
	Button selection will set Schedual type to a string
"""
master = Tk()
master.minsize(width=250, height=220)
early = Button (master, text="Early Development", command=setEarly)
grade = Button (master, text="Grade School", command=setGrade)
imp = Button(master, text="Import from Existing", command=impSchedual)
early.grid(row=0, column=0, ipady = 15, ipadx=75)
grade.grid(row=1, column=0, ipady = 15, ipadx=89)
imp.grid(row=2, column = 0, ipady = 15, ipadx=68)

master.mainloop()


