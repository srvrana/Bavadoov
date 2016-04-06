from constraint import *

def schedule (teacherList):
    mathSetList = solveMath(teacherList)

    for mathSolution in mathSetList:
        #update teacherList with math predefiened
        for i in range(0, len(teacherList)):
            for j in range(0,len(teacherList[i].subjectList)):
                if teacherList[i].subjectList[j].mathClass:
                    teacherList[i].subjectList[j].period = mathSolution.get("TeacherList[" + str(i) + "].subjectList[" + str(j) + "].period")
        #pass list with set math to solve
        #This method returns a list of finished teacherlists, unlike mathsolve
        #print len(mathSetList)
        return  solve(teacherList)
       # for solution in solutions:
            #Method call here.
            #We will pass solution, save to excel, ask if okay. if okay returns true and exit
        #    if(Main.happyWith(solution)):
        #        exit()
        #    print"***********************************************"
    #print "Done with ", len(solutions), " solutions"

##############################
# Returns list of solutions  #
##############################
def solveMath(teacherList):
    problem = Problem()
    for i in range(0, len(teacherList)):
        for j in range(0, len(teacherList[i].subjectList)):
            if teacherList[i].subjectList[j].mathClass:
                problem.addVariable("TeacherList[" + str(i) +"].subjectList[" + str(j) +"].period", teacherList[i].aval)
                #This constraint makes sure teacher isn't double booked
                for l in range(j, len(teacherList[i].subjectList)):
                    if j != l:
                        problem.addConstraint(lambda currentSubject, currentTeachersList: currentSubject != currentTeachersList,
                                          ("TeacherList["+str(i)+"].subjectList["+str(j)+"].period", "TeacherList["+str(i)+"].subjectList["+str(l)+"].period"))

    solution = problem.getSolutions()
    if not bool(solution):
        print "No solution found due to math teachers"
        exit()
    return solution


def solve(teacherList):
    problem = Problem()
    for i in range(0, len(teacherList)):
        for j in range(0, len(teacherList[i].subjectList)):
            #Add Math class with predefiened timeslot | [ ] around period domain do it the program wanting a list element, but we have a int
            if teacherList[i].subjectList[j].mathClass:
                problem.addVariable("TeacherList[" + str(i) +"].subjectList[" + str(j) +"].period", [teacherList[i].subjectList[j].period])
            else:
                problem.addVariable("TeacherList[" + str(i) +"].subjectList[" + str(j) +"].period", teacherList[i].aval)
                for l in range(j, len(teacherList[i].subjectList)):
                    if j != l:
                        for z in range(0,len(teacherList[i].subjectList[l].grade)):
                            #If the grade is differnet and name is the same
                            if not any( grade[0] in teacherList[i].subjectList[l].grade[z] for grade in teacherList[i].subjectList[j].grade) and teacherList[i].subjectList[j].name == teacherList[i].subjectList[l].name :
                                #print "TeacherList["+str(i)+"].subjectList["+str(j)+"].period", " != " "TeacherList["+str(i)+"].subjectList["+str(l)+"].period"
                                problem.addConstraint(lambda currentSubject, currentTeachersList: currentSubject != currentTeachersList,
                                            ("TeacherList["+str(i)+"].subjectList["+str(j)+"].period", "TeacherList["+str(i)+"].subjectList["+str(l)+"].period"))
                                break


                for k in range(i, len(teacherList)):
                    for p in range(j, len(teacherList[k].subjectList)):
                        if not teacherList[k].subjectList[p].mathClass:
                            for z in range(0,len(teacherList[i].subjectList[l].grade)):
                                if any( grade[0] in teacherList[i].subjectList[l].grade[z] for grade in teacherList[i].subjectList[j].grade) and teacherList[i].subjectList[j].name != teacherList[i].subjectList[l].name :
                                    foo = "bar"
                                    #print "TeacherList["+str(i)+"].subjectList["+str(j)+"].period", " != ", "TeacherList["+str(k)+"].subjectList["+str(p)+"].period"
                                    problem.addConstraint(lambda currentSubject, currentTeachersList: currentSubject != currentTeachersList,
                                                   ("TeacherList["+str(i)+"].subjectList["+str(j)+"].period", "TeacherList["+str(k)+"].subjectList["+str(p)+"].period"))

    print ("solving.....")
    solutions = problem.getSolution()
    print ("done!")
    if not bool(solutions):
        print "No solution found"
        exit()
    for i in range(0, len(teacherList)):
        for j in range(0, len(teacherList[i].subjectList)):
            teacherList[i].subjectList[j].period = solutions.get("TeacherList[" + str(i) + "].subjectList[" + str(j) + "].period")
    teacherList = compress (teacherList)
    return teacherList

def compress (teacherList):
    for i in range(0,len(teacherList)):
        for j in range(0, len(teacherList[i].subjectList)):

            if not teacherList[i].subjectList[j].mathClass:

                for k in range(j+1,len(teacherList[i].subjectList)):
                    if teacherList[i].subjectList[j].period == teacherList[i].subjectList[k].period:
                        if teacherList[i].subjectList[j].name == teacherList[i].subjectList[k].name:
                            if teacherList[i].subjectList[j].grade[0][0] == teacherList[i].subjectList[k].grade[0][0]:
                                teacherList[i].subjectList[j].grade.append(teacherList[i].subjectList[k].grade[0])
                                #print "compressing"
                                #print teacherList[i].subjectList[j].name, " == ", teacherList[i].subjectList[k].name
                                #print teacherList[i].subjectList[j].period, " == ", teacherList[i].subjectList[k].period
                                #print teacherList[i].subjectList[j].grade[0], " == ", teacherList[i].subjectList[k].grade[0]

                                del teacherList[i].subjectList[k]
                                return compress(teacherList)

    return teacherList
