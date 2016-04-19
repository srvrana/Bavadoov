from constraint import *
from copy import deepcopy
import xlwt
import os
from collections import defaultdict
from Tkinter import *
import tkMessageBox
import MiddleSchool

"""
    Main Method To be called
    Takes a True / False bool for testing indication
"""
def schedule (teacherList, saveLocation, testing):

    solutionsByMathSet = []

    mathCheck = False
    mathSetList = False
    for teacher in teacherList:
        for subject in teacher.subjectList:
            if subject.mathClass:
                mathCheck = True
                break

    if not mathCheck:
        tkMessageBox.showinfo("Information", "No math classes detected.\nOK to continue")
    else:
        mathSetList = solveMath(teacherList)
    fullSolutionList= []

    if bool(mathSetList):
        for mathSolution in mathSetList:
            solutionsByMathSet.append([])

            tempList = deepcopy(teacherList)
            for i in range(0, len(tempList)):
                for j in range(0,len(tempList[i].subjectList)):
                    if tempList[i].subjectList[j].mathClass:
                        tempList[i].subjectList[j].period = mathSolution.get("TeacherList[" + str(i) + "].subjectList[" + str(j) + "].period")
            solutionItter = solve(tempList)
            for x in solutionItter:
                tempList = deepcopy(teacherList)
                for i in range(0, len(teacherList)):
                    for j in range(0, len(tempList[i].subjectList)):
                        tempList[i].subjectList[j].period = x.get("TeacherList[" + str(i) + "].subjectList[" + str(j) + "].period")

                tempList = compress (tempList)
                if len(tempList) > 0:
                    solutionsByMathSet[-1].append(tempList)
                if len(solutionsByMathSet) > 35000:
                    break

        for subset in solutionsByMathSet:
            subset = sortBySubjectCount(subset)

        minSolutionCounter = float("inf")
        for set in solutionsByMathSet:
            if len(set) == 0:
                del(set)
            elif len(set) < minSolutionCounter:
                minSolutionCounter = len(set)

        for i in range(0,minSolutionCounter):
            for subset in solutionsByMathSet:
                if len(subset) >0:
                    fullSolutionList.append(subset[i])


    elif not mathCheck:
        solutionItter = solve(teacherList)
        for x in solutionItter:
            tempList = deepcopy(teacherList)
            for i in range(0, len(teacherList)):
                for j in range(0, len(tempList[i].subjectList)):
                    tempList[i].subjectList[j].period = x.get("TeacherList[" + str(i) + "].subjectList[" + str(j) + "].period")

            tempList = compress (tempList)
            fullSolutionList.append(tempList)
            if len(fullSolutionList) > 20000:
                break

    if not bool(fullSolutionList):
        tkMessageBox.showinfo("Error", "No solutions were able to be found.")
        exit()



    fullSolutionList = sortBySubjectCount (fullSolutionList)
    auditable = scheduleAuditable(teacherList)
    homerooms = schedualHomeroom(teacherList)

   #To support testing
    if testing:
        return fullSolutionList

    #Else
    printingMethod(fullSolutionList,auditable,homerooms, saveLocation)

"""
    Returns list of solutions
"""
def solveMath(teacherList):
    """
    problem = Problem()
    for i in range(0, len(teacherList)):
        for j in range(0, len(teacherList[i].subjectList)):
            if teacherList[i].subjectList[j].mathClass:
                for k in range (0,len(teacherList[i].subjectList)):
                    problem.addVariable("TeacherList[" + str(i) +"].subjectList[" + str(k) +"].period", teacherList[i].aval)
                i += 1

    for i in range(0, len(teacherList)):
        for j in range(0, len(teacherList[i].subjectList)):
            if teacherList[i].subjectList[j].mathClass:
                for l in range(j, len(teacherList[i].subjectList)):
                    if j != l:
                        problem.addConstraint(lambda currentSubject, currentTeachersList: currentSubject != currentTeachersList,
                                          ("TeacherList["+str(i)+"].subjectList["+str(j)+"].period", "TeacherList["+str(i)+"].subjectList["+str(l)+"].period"))

    solution = problem.getSolutions()
    if not bool(solution):
        return []
    return solution
    """
    containsMathList = []
    problem = Problem()
    #add all math classes
    for i in range(0, len(teacherList)):
        for j in range(0, len(teacherList[i].subjectList)):
            if teacherList[i].subjectList[j].mathClass:
                problem.addVariable("TeacherList[" + str(i) +"].subjectList[" + str(j) +"].period", teacherList[i].aval)

    #For teachers that have math classes, they can't be dual booked.
    for i in range(0, len(teacherList)):
        for j in range(0,len(teacherList[i].subjectList)):
            for k in range(j,len(teacherList[i].subjectList)):
                if j != k and teacherList[i].subjectList[j].mathClass and teacherList[i].subjectList[k].mathClass:
                    problem.addConstraint(lambda currentSubject, currentTeachersList: currentSubject != currentTeachersList,
                                    ("TeacherList["+str(i)+"].subjectList["+str(j)+"].period", "TeacherList["+str(i)+"].subjectList["+str(k)+"].period"))

    #For math classes, grades can't be double booked. list[i].[j] list[l].[m]
    for i in range(0, len(teacherList)):
        for j in range(0, len(teacherList[i].subjectList)):
            if teacherList[i].subjectList[j].mathClass:
                for l in range(i+1, len(teacherList)):
                    for m in range(0, len(teacherList[l].subjectList)):
                        if teacherList[l].subjectList[m].mathClass:
                            if any( grade in teacherList[i].subjectList[j].grade for grade in teacherList[l].subjectList[m].grade):
                                problem.addConstraint(lambda currentSubject, currentTeachersList: currentSubject != currentTeachersList,
                                            ("TeacherList["+str(i)+"].subjectList["+str(j)+"].period", "TeacherList["+str(l)+"].subjectList["+str(m)+"].period"))

    solution = problem.getSolutions()
    if not bool(solution):
        return []
    return solution

"""
    Returns list of solutions
"""
def solve(teacherList):
    problem = Problem()
    for i in range(0, len(teacherList)):
        for j in range(0, len(teacherList[i].subjectList)):
            #Add Math class with predefiened timeslot | [ ] around period domain do it the program wanting a list element, but we have a int
            if teacherList[i].subjectList[j].mathClass:
                problem.addVariable("TeacherList[" + str(i) +"].subjectList[" + str(j) +"].period", [teacherList[i].subjectList[j].period])
            else:
                problem.addVariable("TeacherList[" + str(i) +"].subjectList[" + str(j) +"].period", teacherList[i].aval)
                for l in range(0, len(teacherList[i].subjectList)):
                    if j != l:
                        for z in range(0,len(teacherList[i].subjectList[l].grade)):
                            #If the grade is differnet and name is the same
                            if not any( grade[0] in teacherList[i].subjectList[l].grade[z][0] for grade in teacherList[i].subjectList[j].grade) and teacherList[i].subjectList[j].name == teacherList[i].subjectList[l].name :
                                problem.addConstraint(lambda currentSubject, currentTeachersList: currentSubject != currentTeachersList,
                                            ("TeacherList["+str(i)+"].subjectList["+str(j)+"].period", "TeacherList["+str(i)+"].subjectList["+str(l)+"].period"))
                                break
                        #print teacherList[i].subjectList[j].name, " !=",  teacherList[i].subjectList[l].name
                        if teacherList[i].subjectList[j].name != teacherList[i].subjectList[l].name:
                            problem.addConstraint(lambda currentSubject, currentTeachersList: currentSubject != currentTeachersList,
                                            ("TeacherList["+str(i)+"].subjectList["+str(j)+"].period", "TeacherList["+str(i)+"].subjectList["+str(l)+"].period"))


                for k in range(0, len(teacherList)):
                    for p in range(0, len(teacherList[k].subjectList)):
                        if any( grade in teacherList[i].subjectList[j].grade for grade in teacherList[k].subjectList[p].grade) and teacherList[i].subjectList[j].name != teacherList[k].subjectList[p].name :
                            problem.addConstraint(lambda currentSubject, currentTeachersList: currentSubject != currentTeachersList,
                                            ("TeacherList["+str(i)+"].subjectList["+str(j)+"].period", "TeacherList["+str(k)+"].subjectList["+str(p)+"].period"))



    solutions = problem.getSolutionIter()
    if not bool(solutions):
        return []
    return solutions


"""
    Returns compressed list
"""
def compress (teacherList):
    for i in range(0,len(teacherList)):
        for j in range(0, len(teacherList[i].subjectList)):

            if not teacherList[i].subjectList[j].mathClass:

                for k in range(j+1,len(teacherList[i].subjectList)):
                    if teacherList[i].subjectList[j].period == teacherList[i].subjectList[k].period:
                        if teacherList[i].subjectList[j].name == teacherList[i].subjectList[k].name:
                            if teacherList[i].subjectList[j].grade[0][0] == teacherList[i].subjectList[k].grade[0][0]:
                                teacherList[i].subjectList[j].grade.append(teacherList[i].subjectList[k].grade[0])
                                del teacherList[i].subjectList[k]
                                return compress(teacherList)

    return teacherList

"""
    Returns list sorted so that first entry has the most free space
"""
def sortBySubjectCount(solutionList):

    for solution in solutionList:
        count = 0
        for teacher in solution:
            count += len(teacher.subjectList)
        solution.append(count)

    solutionList.sort(key=lambda x: x[-1])

    for solution in solutionList:
        del solution[-1]

    return solutionList

"""
    Returns homeroom list for scheudal output
"""
def schedualHomeroom(teacherList):
    class homeroom:
        def __init__(self,grade,name):
            self.grade = grade
            self.name = name

    tempList = []
    for teacher in teacherList:
        tempList.append(homeroom(teacher.homeRoom, teacher.name))
    tempList.sort(key=lambda x: x.grade[0])
    return tempList

"""
    Returns schedual for audiable stuff
"""
def scheduleAuditable (teacherList):
    class teach:
        def __init__(self,name):
            self.name = name
            self.count = 0
    names = []
    for teacher in teacherList:
        names.append(teach(teacher.name))

    assignments =[[0]*6 for i in range(3)]

    for j in range (0,3):
        for i in range (0,6):
            names.sort(key=lambda x: x.count)
            assignments[j][i] = names[0].name
            if i == 0 or i ==1:
                names[0].count +=2
            else:
                names[0].count +=1
    return assignments

"""
    Prints schedules to an excel file
"""
def printingMethod(fullSolutionList,auditable,homerooms, saveLocation):

    happy = False
    styleBold = xlwt.easyxf("font: bold 1")
    allowNewLine = xlwt.XFStyle()
    allowNewLine.alignment.wrap = 1
    styleCenter = xlwt.easyxf("alignment: horizontal center")
    styleCenter.alignment.wrap = 1

    while not happy:
        workbook = xlwt.Workbook()
        sheet = workbook.add_sheet("Schedule")
        for i in range(0,5):
            sheet.col(i).width = 256*30
        #Default info inlcuding audit and homeroom
        fillDefault(sheet, auditable,homerooms )
        #Fill with generated
        currentSchedual = fullSolutionList.pop(0)

        monWed = [[],[],[]]
        tueThur = [[],[],[]]


        for teacher in currentSchedual:
            for subject in teacher.subjectList:
                subject.grade.sort()
                if subject.period ==1:
                    monWed[0].append(subject)
                elif subject.period ==2:
                    monWed[1].append(subject)
                elif subject.period ==3:
                    monWed[2].append(subject)
                elif subject.period ==4:
                    tueThur[0].append(subject)
                elif subject.period ==5:
                    tueThur[1].append(subject)
                elif subject.period ==6:
                    tueThur[2].append(subject)

        for period in monWed:
            period.sort(key = lambda x:x.grade)
        for period in tueThur:
            period.sort(key = lambda x:x.grade)

        for x in range(0,len(monWed)):
            content = ""
            for subject in monWed[x]:
                content += str(subject.grade) +  ": " + subject.name + "\n\n"
            monWed[x] = content

        for x in range(0,len(tueThur)):
            content = ""
            for subject in tueThur[x]:
                content += str(subject.grade) + ": " + subject.name + "\n\n"
            tueThur[x] = content




        sheet.write(4,1,monWed[0],styleCenter)
        sheet.write(6,1,monWed[1],styleCenter)
        sheet.write(9,1,monWed[2],styleCenter)

        sheet.write(4,2,tueThur[0],styleCenter)
        sheet.write(6,2,tueThur[1],styleCenter)
        sheet.write(9,2,tueThur[2],styleCenter)

        sheet.write(4,3,monWed[0],styleCenter)
        sheet.write(6,3,monWed[1],styleCenter)
        sheet.write(9,3,monWed[2],styleCenter)

        sheet.write(4,4,tueThur[0],styleCenter)
        sheet.write(6,4,tueThur[1],styleCenter)
        sheet.write(9,4,tueThur[2],styleCenter)

        sheetTwo = workbook.add_sheet("Friday")
        printFriday(sheetTwo,currentSchedual,auditable,homerooms)
        for i in range(0,2):
            sheetTwo.col(i).width = 256*30

        sheetThree = workbook.add_sheet("Rotation")
        printRotations(sheetThree,currentSchedual)
        for i in range(0,5):
            sheetThree.col(i).width = 256*30

        #Save settings to workbook with jacob's code

        MiddleSchool.saveMiddleSchoolSettings(workbook)
        workbook.save(saveLocation)
        print "Saved to " + saveLocation
        os.system("start "+saveLocation)
        happy = isUserHappy()
        #happy = True


"""
    Fills in everything except class'
"""
def fillDefault (sheet,auditable,homerooms ):
    styleBold = xlwt.easyxf("font: bold 1; alignment: horizontal center")
    styleBold.alignment.wrap = 1
    styleCenter = xlwt.easyxf("alignment: horizontal center")
    styleCenter.alignment.wrap = 1
    styleNewLine = xlwt.easyxf()
    styleNewLine.alignment.wrap = 1

    sheet.write(0,0,"Middle School Schedule", styleBold)
    sheet.write(1,0,"Period", styleBold)
    sheet.write(1,1,"Monday", styleBold)
    sheet.write(1,2,"Tuesday", styleBold)
    sheet.write(1,3,"Wednesday", styleBold)
    sheet.write(1,4,"Thursday", styleBold)
    sheet.write(2,0,"8:00 - 8:20",styleBold)
    #Before care
    for i in range(1,5):
        content = auditable[i%2][0] + " / " + auditable[i%2][1]
        sheet.write(2,i,"Before Care:\n\n" + content,styleCenter)

    sheet.write(3,0,"8:30 - 8:35\n\nHomeroom", styleBold)
    #Homeroom
    content = ""
    for teacher in homerooms:
        content +=  teacher.grade + ": " + teacher.name + "\n"
    for i in range(1,5):
        sheet.write(3,i,content,styleCenter)

    sheet.write(4,0,"8:35 - 9:55\n\n 1", styleBold)
    sheet.write(5,0,"9:55 - 10:00",styleBold)
    #Break
    for i in range(1,5):
        sheet.write(5,i,"Morning Break", styleBold)

    sheet.write(6,0,"10:00 - 11:20\n\n2", styleBold)
    sheet.write(7,0,"11:20 - 12:05\n\n Specials", styleBold)
    #Rotation
    for i in range(1,5):
        sheet.write(7,i,"Quarterly Rotation", styleBold)

    sheet.write(8,0,"Lunch: 12:05 -\n12:25\n\nRecess: 12:25 -\n12:50",styleBold)
    # Lunches
    for i in range(1,5):
        content = auditable[i%2][2] + " / " + auditable[i%2][3]
        sheet.write(8,i,"Lunch:\n\n" + content,styleCenter)

    sheet.write(9,0,"12:50 - 2:10\n\n3", styleBold)
    sheet.write(10,0,"2:10 - 2:15",styleBold)
    for i in range(1,5):
        sheet.write(10,i,"Afternoon Break", styleBold)
    sheet.write(11,0,"2:15 - 3:00",styleBold)
    #end of day
    for i in range(1,5):
        content = "Study Hall: " + auditable[i%2][4] + "\n" +"Project Room: ", auditable[i%2][5]
        sheet.write(11,i,content,styleCenter)

"""
    prints sheet for friday schedule
"""
def printFriday(sheet, currentSchedual,auditable, homerooms):
    styleBold = xlwt.easyxf("font: bold 1; alignment: horizontal center")
    styleBold.alignment.wrap = 1
    styleCenter = xlwt.easyxf("alignment: horizontal center")
    styleCenter.alignment.wrap = 1
    styleNewLine = xlwt.easyxf()
    styleNewLine.alignment.wrap = 1

    friday = ["","","","","",""]
    #generate period lists
    for teacher in currentSchedual:
        for subject in teacher.subjectList:
            friday[subject.period-1] += (str(subject.grade) + " : " + subject.name + "\n")


    sheet.write(0,0,"Period",styleBold)
    sheet.write(0,1,"Friday",styleBold)
    #before care
    sheet.write(1,0,"8:00 - 8:20",styleBold)
    content = auditable[-1][0] + " / " + auditable[-1][1]
    sheet.write(1,1,"Before Care:\n\n" + content,styleCenter)
    #homeroom
    sheet.write(2,0,"8:30 - 8:35\n\nHomeroom",styleBold)
    content = ""
    for teacher in homerooms:
        content +=  teacher.grade + ": " + teacher.name + "\n"
    sheet.write(2,1,content,styleCenter)
    #P1
    sheet.write(3,0,"8:35 - 9:15\n\n1",styleBold)
    sheet.write(3,1,friday[0],styleCenter)
    #P2
    sheet.write(4,0,"9:15 - 9:55\n\n2",styleBold)
    sheet.write(4,1,friday[1],styleCenter)
    #Braek
    sheet.write(5,0,"9:55 - 10:00",styleBold)
    sheet.write(5,1, "Morning Break",styleBold)
    #P3
    sheet.write(6,0,"10:00 - 10:40\n\n3",styleBold)
    sheet.write(6,1,friday[2],styleCenter)
    #P4
    sheet.write(7,0,"10:40 - 11:20\n\n4",styleBold)
    sheet.write(7,1,friday[3],styleCenter)
    #Rotation
    sheet.write(8,0,"11:20 - 12:05",styleBold)
    sheet.write(8,1,"Quarterly Rotation",styleBold)

    #Lunch
    sheet.write(9,0,"Lunch: 12:50 - 1:30\n\nRecess: 12:25 - 12:50",styleBold)
    content = auditable[-1][2] + " , " + auditable[-1][3]
    sheet.write(9,1,"Lunch: " + content,styleBold)
    #P5
    sheet.write(10,0,"12:50 - 1:30\n\n5",styleBold)
    sheet.write(10,1,friday[4],styleCenter)
    #P6
    sheet.write(11,0,"1:30 - 2:10\n\n6",styleBold)
    sheet.write(11,1,friday[5],styleCenter)
    #Break
    sheet.write(12,0,"2:10 - 2:15",styleBold)
    sheet.write(12,1,"Afternoon Break",styleBold)
    #End of day
    sheet.write(13,0,"2:15 - 3:00",styleBold)
    content = "Study Hall: " + auditable[-1][4] + "\nGuided Study: " + auditable[-1][5]
    sheet.write(13,1,content,styleBold)

"""
    Generates quartery rotation, returns as dictionary
"""
def generateRotation (currentSchedual):
    gradeList = defaultdict(list)
    for teacher in currentSchedual:
        for subject in teacher.subjectList:
            for grade in subject.grade:
                if grade in gradeList.keys():
                    gradeList[grade].append(subject)
                else:
                    gradeList[str(grade)] =[subject]
    for key in gradeList.keys():
        tempList = gradeList[key]
        tempList.sort(key = lambda x: x.period)
        for i in range(0,len(tempList)):
            tempList[i] = tempList[i].name
        gradeList[key] = tempList
    return gradeList

"""
    prints sheet for Quarterly rotations
"""
def printRotations(sheet,currentSchedual):
    styleBold = xlwt.easyxf("font: bold 1")
    allowNewLine = xlwt.XFStyle()
    allowNewLine.alignment.wrap = 1
    styleCenter = xlwt.easyxf("alignment: horizontal center")
    styleCenter.alignment.wrap = 1

    gradeList = generateRotation(currentSchedual)

    sheet.write(0,0,"Class Rotations",styleBold)

    keys = gradeList.keys()
    keys.sort()
    i = 1
    for key in keys:
        sheet.write(i,0,key,styleBold)
        if i < 5:
            #Boy i'm lazy
            sheet.write(0,i,"Quarter: " + str(i),styleBold)

        classList = gradeList[key]
        x = len(classList)
        y = x/2
        mw = ""
        tth =""
        for j in range(0,len(classList)):
            if j <= y:
                mw += (classList[j] + "\n")
            else:
                tth += (classList[j] + "\n")

        sheet.write(i,1,mw)
        sheet.write(i,2,tth)
        sheet.write(i,3,mw)
        sheet.write(i,4,tth)
        i += 1

"""
   Gui for acceptance of schedual
"""
def isUserHappy ():
    

    global root
    root = Tk()
    root.columnconfigure(0,weight=1)
    root.minsize(width=250, height=200)
    Happy = Button(root, text="Accept Current Schedule",command = happy)
    Sad = Button(root,text="Close Schedule and Get Another", command = sad)
    Happy.grid(row=0, column=0, ipady=15,ipadx=19)
    Sad.grid(row=1,column=0, ipady=15)
    Label(root,text = "Warning:\n\nYou must close the open schedule before you can generate another!").grid(row=2)
    Label(root,text = "You may save the current one to another location if necessary").grid(row=3)
    root.mainloop()


def happy():
    root.destroy()
    exit()

def sad():
    root.destroy()
    return False

