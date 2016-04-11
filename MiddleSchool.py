from Tkinter import *
from MiddleSchoolScheduler import schedule
from tkMessageBox import *
import copy
import tkSimpleDialog
import tkFileDialog
from Classes import *
import xlwt
from xlrd import open_workbook

SAVELOCATION = ""
ScheduleType = ""
TeacherList = []

def setMiddleTest():
	global ScheduleType
	global TeacherList

	ScheduleType = "Middle"
	saveLocation()
	getMiddleTeachers() 	#Set TeacherList with initialized SubjectLists

	parsedList = parseTeacherList()

	printTeachers(parsedList)
	schedule(parsedList, SAVELOCATION, False)


def saveLocation():
	global SAVELOCATION
	SAVELOCATION = str(tkFileDialog.askdirectory()) + "/"
	SAVELOCATION += (tkSimpleDialog.askstring("file", "Name of saved file"))
	SAVELOCATION += ".xls"

"""
	Gets us the Number of teachers and their info
	Calls Get Blocks
"""
def getMiddleTeachers():
	global TeacherList
	NewTeacherList 	= []
	NumTeachers 		= ''

	#Array's of tkinter objects, only way i could find to loop though them with dynamically set number of teachers
	Name 							= []
	Grade 						= []
	Avail 						= []
	NumberOfSubjects 	= []


	def addTeacher(x, slave):
		NewTeacherList.append(Teacher())
		NewTeacherList[x].name = Name[x].get()
		NewTeacherList[x].aval = Avail[x].get()
		NewTeacherList[x].homeRoom = Grade[x].get().upper()

		numOfSubjects = int(NumberOfSubjects[x].get())

		slave.destroy()
		vari = getSubjectList(x, numOfSubjects)

		NewTeacherList[x].subjectList = vari
		if len(NewTeacherList) < NumTeachers:
			promptTeacher(x+1)

		slave.quit()
	#End addTeacher()

	def promptTeacher(x):
		slave = Tk()

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

		Label(slave, text ="Teacher " + str(x+1)).grid(row=0, column=0, columnspan=2, pady=5)
		Label(slave, text ="Name: ").grid(row=1, column=0)
		Name[x].grid(row=1,column=1)

		Label(slave, text ="Homeroom: ").grid(row=2, column=0)
		Grade[x].grid(row=2,column=1)

		Label(slave, text ="Availability: ").grid(row=3, column=0)
		Avail[x].grid(row=3,column=1)

		Label(slave, text ="Number of Subjects: ").grid(row=4, column=0)
		NumberOfSubjects[x].grid(row=4,column=1)

		sub = Button(slave, text="Submit", command=lambda: addTeacher(x, slave))
		sub.grid(row=5, column=1)
		
		slave.mainloop()
	#promptTeacher()

	#Get Number of Teachers, stored globaly
	NumTeachers = tkSimpleDialog.askinteger("NumTeachers", "How Many Teachers?", initialvalue=NumTeachers)

	#Pad Teachers array for prepopulation where we add teachers
	while len(TeacherList) < NumTeachers:
		TeacherList.append(Teacher())

	promptTeacher(0)
	TeacherList = NewTeacherList



def getSubjectList(x, numOfSubjects):
	NumSubjects = numOfSubjects
	NewSubjectList = []

	Name 		= []
	Grade 	= []
	Period 	= []
	Math 		= []

	def addSubject(x, y, slave2):
		NewSubjectList.append(Subject())
		NewSubjectList[y].name = Name[y].get()
		NewSubjectList[y].grade = Grade[y].get().upper()
		NewSubjectList[y].mathClass = Math[y]

		slave2.destroy()

		if len(NewSubjectList) < NumSubjects:
			promptSubject(x, y+1)
		
		slave2.quit()
	"""End Sub Command"""

	def promptSubject(x, y):
		def changeChkVal():
				Math[y] = not Math[y]

		slave2 = Tk()

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

		Label(slave2, text ="Subject " + str(y+1)).grid(row=0, column=0, columnspan=2, pady=5)
		Label(slave2, text ="Name: ").grid(row=1, column=0)
		Name[y].grid(row=1,column=1)

		Label(slave2, text ="Grade: ").grid(row=2, column=0)
		Grade[y].grid(row=2,column=1)

		#Checkbutton(slave2, text ="Math: ", command=cb).grid(row=4,  column=0)
		cb = Checkbutton(slave2, text="Math: ", command=changeChkVal)
		if Math[y]:
			cb.select()
		cb.grid(row=4,  column=0)

		sub = Button(slave2, text="Submit", command=lambda: addSubject(x, y, slave2))
		sub.grid(row=5, column=1)
		
		slave2.mainloop()
		"""End Sub Command"""
	"""End Sub Command"""

	while len(TeacherList[x].subjectList) < NumSubjects:
		TeacherList[x].subjectList.append(Subject())

	promptSubject(x, 0)
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
