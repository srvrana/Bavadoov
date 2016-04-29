from Tkinter import *
from tkMessageBox import *
import copy
import tkSimpleDialog
import tkFileDialog
from Classes import *
#This is put into a try / catch due to the fact that when running the test scrips, this class is never created.
try:
	from MiddleSchoolScheduler import schedule
except ImportError:
	pass
import xlwt
from xlrd import open_workbook

SAVELOCATION = ""
ScheduleType = ""
TeacherList = []
OldNumTeachers = 0

def setMiddleTest(master):
	global ScheduleType
	global TeacherList

	ScheduleType = "Middle"
	saveLocation()
	getMiddleTeachers() 	#Set TeacherList with initialized SubjectLists

	parsedList = parseTeacherList()

	printTeachers(parsedList)
	master.destroy()
	schedule(parsedList, SAVELOCATION, False)
	


def saveLocation():
	global SAVELOCATION
	SAVELOCATION = str(tkFileDialog.askdirectory()) + "/"
	SAVELOCATION += (tkSimpleDialog.askstring("file", "Name of saved file"))
	SAVELOCATION += ".xls"

def importMiddleSchoolSettings(sheet, master):
	global OldNumTeachers
	OldNumTeachers = int(sheet.cell(1,1).value)
	for x in range(0,OldNumTeachers):
		TeacherList.append(Teacher())
		TeacherList[x].name 		= sheet.cell((x + 4) + (4 * x),1).value
		TeacherList[x].aval 		= sheet.cell((x + 5) + (4 * x),1).value
		TeacherList[x].homeRoom = sheet.cell((x + 6) + (4 * x),1).value
		NumSubjects 						= int(sheet.cell((x + 7) + (4 * x),1).value)

		for y in range(0,NumSubjects):
			TeacherList[x].subjectList.append(Subject())
			TeacherList[x].subjectList[y].name = sheet.cell((x + 4) + (4 * x),(4+y)).value
			TeacherList[x].subjectList[y].grade = sheet.cell((x + 5) + (4 * x),(4+y)).value
			TeacherList[x].subjectList[y].mathClass = bool(sheet.cell((x + 6) + (4 * x),(4+y)).value)

	setMiddleTest(master)

def saveMiddleSchoolSettings(workbook):
	dataInput = workbook.add_sheet("User Input", cell_overwrite_ok=True)
	dataInput.col(0).width = 256*25
	dataInput.col(1).width = 256*20
	dataInput.col(3).width = 256*15
	#FrameWork
	style = xlwt.easyxf('font:bold 1')
	dataInput.write(0,0,"Type Of Schedule:", style)
	dataInput.write(1,0,"Number Of Teachers:", style)
	dataInput.write(3,0,"Teachers", style)
	dataInput.write(4,0,"Name:", style)
	dataInput.write(5,0,"Homeroom:", style)
	dataInput.write(6,0,"Availability:", style)
	dataInput.write(7,0,"Number of Subjects:", style)

	dataInput.write(3,3,"Subjects", style)
	dataInput.write(4,3,"Name:", style)
	dataInput.write(5,3,"Grade:", style)
	dataInput.write(6,3,"Math:", style)

	dataInput.write(0,1,ScheduleType)
	dataInput.write(1,1,len(TeacherList))

	for x in range(0,len(TeacherList)):
		dataInput.write((x + 4) + (4 * x),1,TeacherList[x].name)
		dataInput.write((x + 5) + (4 * x),1,TeacherList[x].aval)
		dataInput.write((x + 6) + (4 * x),1,TeacherList[x].homeRoom)
		dataInput.write((x + 7) + (4 * x),1,len(TeacherList[x].subjectList))

		for y in range(0,len(TeacherList[x].subjectList)):
			dataInput.write((x + 4) + (4 * x),(4+y),TeacherList[x].subjectList[y].name)
			dataInput.write((x + 5) + (4 * x),(4+y),TeacherList[x].subjectList[y].grade)
			dataInput.write((x + 6) + (4 * x),(4+y),TeacherList[x].subjectList[y].mathClass)





"""
	Gets us the Number of teachers and their info
	Calls Get Blocks
"""
def getMiddleTeachers():
	global TeacherList
	global OldNumTeachers
	NewTeacherList 	= []
	
	NumTeachers = 0

	#Array's of tkinter objects, only way i could find to loop though them with dynamically set number of teachers
	Name 							= []
	Grade 						= []
	Avail 						= []
	NumberOfSubjects 	= []


	def addTeacher(slave):
		for x in range(0,len(TeacherList)):
			NewTeacherList.append(Teacher())
			NewTeacherList[x].name = Name[x].get()
			NewTeacherList[x].aval = Avail[x].get()
			NewTeacherList[x].homeRoom = Grade[x].get().upper()
			
			numOfSubjects = int(NumberOfSubjects[x].get())
			vari = getSubjectList(x, numOfSubjects, NewTeacherList[x].name)
			NewTeacherList[x].subjectList = vari
			
		slave.destroy()
		slave.quit()
	#End addTeacher()

	#promptTeacher()

	#Get Number of Teachers, stored globaly
	while(NumTeachers < 1):
		NumTeachers = tkSimpleDialog.askinteger("NumTeachers", "How Many Teachers?", initialvalue=OldNumTeachers)

	#Pad Teachers array for prepopulation where we add teachers
	t = len(TeacherList)
	while len(TeacherList) < NumTeachers:
		TeacherList.append(Teacher())
		TeacherList[t].aval = ''
		t = t + 1

	slave = Tk()

	for x in range(0,NumTeachers):
		prepop = Entry(slave)
		prepop.insert(0, TeacherList[x].name)
		Name.append(prepop)

		prepop = Entry(slave)
		prepop.insert(0, TeacherList[x].homeRoom)
		Grade.append(prepop)

		prepop = Entry(slave)
		prepop.insert(0, TeacherList[x].aval)
		Avail.append(prepop)

		prepop = Entry(slave)
		prepop.insert(0, len(TeacherList[x].subjectList))
		NumberOfSubjects.append(prepop)

		Label(slave, text ="Teacher " + str(x+1)).grid(row=x*6, column=0, columnspan=2, pady=5)

		Label(slave, text ="Name: ").grid(row=x*6+1, column=0)
		Name[x].grid(row=x*6+1,column=1)

		Label(slave, text ="Homeroom: ").grid(row=x*6+2, column=0)
		Grade[x].grid(row=x*6+2,column=1)

		Label(slave, text ="Availability: ").grid(row=x*6+3, column=0)
		Avail[x].grid(row=x*6+3,column=1)

		Label(slave, text ="Number of Subjects: ").grid(row=x*6+4, column=0)
		NumberOfSubjects[x].grid(row=x*6+4,column=1)

	sub = Button(slave, text="Submit", command=lambda: addTeacher(slave))
	sub.grid(row=NumTeachers*10, column=1)
	
	slave.mainloop()

	TeacherList = NewTeacherList



def getSubjectList(x, numOfSubjects, teacherName):
	NumSubjects = numOfSubjects
	NewSubjectList = []

	Name 		= []
	Grade 	= []
	Period 	= []
	Math 		= []

	def addSubject(slave2):
		for y in range(0,NumSubjects):
			NewSubjectList.append(Subject())
			NewSubjectList[y].name = Name[y].get()
			NewSubjectList[y].grade = Grade[y].get().upper()
			NewSubjectList[y].mathClass = Math[y]

		slave2.destroy()
		slave2.quit()
	"""End Sub Command"""

	
	s = len(TeacherList[x].subjectList)
	while len(TeacherList[x].subjectList) < NumSubjects:
		TeacherList[x].subjectList.append(Subject())
		TeacherList[x].subjectList[s].grade = ''
		s = s + 1


	def changeChkVal():
			Math[y] = not Math[y]

	slave2 = Tk()

	for y in range(0,NumSubjects):
		prepop = Entry(slave2)
		prepop.insert(0, TeacherList[x].subjectList[y].name)
		Name.append(prepop)

		prepop = Entry(slave2)
		prepop.insert(0, TeacherList[x].subjectList[y].grade)
		Grade.append(prepop)

		prepop = Entry(slave2)
		prepop.insert(0, TeacherList[x].subjectList[y].period)
		Period.append(prepop)

		Math.append(bool)
		Math[y] = TeacherList[x].subjectList[y].mathClass or False

		Label(slave2, text = teacherName + "Subject " + str(y+1)).grid(row=y*6, column=0, columnspan=2, pady=5)
		Label(slave2, text ="Name: ").grid(row=y*6+1, column=0)
		Name[y].grid(row=y*6+1,column=1)

		Label(slave2, text ="Grade: ").grid(row=y*6+2, column=0)
		Grade[y].grid(row=y*6+2,column=1)

		#Checkbutton(slave2, text ="Math: ", command=cb).grid(row=4,  column=0)
		cb = Checkbutton(slave2, text="Math", command=changeChkVal)
		if Math[y]:
			cb.select()
		cb.grid(row=y*6+3,  column=0)

	sub = Button(slave2, text="Submit", command=lambda: addSubject(slave2))
	sub.grid(row=NumSubjects*10, column=0)
	
	slave2.mainloop()

	return NewSubjectList


def parseTeacherList():
	global TeacherList
	parsedTeacherList = []
	#For Each block in the day
	for x in range(0, len(TeacherList)):
		parsedTeacherList.append(copy.deepcopy(TeacherList[x])) 
		parsedTeacherList[x].aval = map(int, parsedTeacherList[x].aval.split(','))

		parsedTeacherList[x].subjectList = []
		for y in range(0, len(TeacherList[x].subjectList)):
			tempList = copy.deepcopy(TeacherList[x].subjectList[y].grade)
			tempList = tempList.split(',')
			#print parsedTeacherList[x].subjectList[y].grade
			if (not TeacherList[x].subjectList[y].mathClass):
				for z in range(0, len(tempList)):
					if '/' in tempList[z]:
						tempList[z] = tempList[z].split('/')
						tempSlashList = []
						for tx in range(0, len(tempList[z])):
							tempSlashList.append(str(tempList[z][tx]) + str('A'))
							tempSlashList.append(str(tempList[z][tx]) + str('B'))
						for ty in range(0, len(tempSlashList)):
							tempSubject = copy.deepcopy(TeacherList[x].subjectList[y])
							tempSubject.grade = []
							tempSubject.grade.append(tempSlashList[ty])
							parsedTeacherList[x].subjectList.append(tempSubject)
					else:
						tempSubject = copy.deepcopy(TeacherList[x].subjectList[y])
						tempSubject.grade = []
						tempSubject.grade.append(tempList[z])
						parsedTeacherList[x].subjectList.append(tempSubject)
			else:
				parsedTeacherList[x].subjectList.append(copy.deepcopy(TeacherList[x].subjectList[y]))
				parsedTeacherList[x].subjectList[y].grade = parsedTeacherList[x].subjectList[y].grade.split(',')

	return parsedTeacherList

def printTeachers(passedList):
	for x in range(0, len(passedList)):
		print passedList[x].__class__
		print passedList[x].name," : ", passedList[x].name.__class__
		print passedList[x].aval," : ", passedList[x].aval.__class__
		print "Period type = ", passedList[x].aval[0].__class__
		print passedList[x].homeRoom," : ", passedList[x].homeRoom.__class__
		print
		for y in range(0, len(passedList[x].subjectList)):
			print passedList[x].subjectList[y].name," : ", passedList[x].subjectList[y].name.__class__
			print passedList[x].subjectList[y].grade," : ",passedList[x].subjectList[y].grade.__class__
			print "grade type = ", passedList[x].subjectList[y].grade[0].__class__
			print passedList[x].subjectList[y].period," : ",passedList[x].subjectList[y].period.__class__
			print passedList[x].subjectList[y].mathClass," : ", passedList[x].subjectList[y].mathClass.__class__
			print
