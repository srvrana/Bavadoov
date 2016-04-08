from constraint import *
from copy import deepcopy

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
        solutions = solve(teacherList)
        return solutions
        #for solution in solutions:
        #    return solution
            #exit()
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
                            #print teacherList[i].subjectList[l].grade[z][0]
                            #If the grade is differnet and name is the same
                            if not any( grade[0] in teacherList[i].subjectList[l].grade[z][0] for grade in teacherList[i].subjectList[j].grade) and teacherList[i].subjectList[j].name == teacherList[i].subjectList[l].name :
                                #print "TeacherList["+str(i)+"].subjectList["+str(j)+"].period", " != " "TeacherList["+str(i)+"].subjectList["+str(l)+"].period"
                                #print teacherList[i].subjectList[j].name, " != ", teacherList[i].subjectList[l].name
                                #print teacherList[i].subjectList[j].grade, " != ", teacherList[i].subjectList[l].grade


                                problem.addConstraint(lambda currentSubject, currentTeachersList: currentSubject != currentTeachersList,
                                            ("TeacherList["+str(i)+"].subjectList["+str(j)+"].period", "TeacherList["+str(i)+"].subjectList["+str(l)+"].period"))
                                break


                for k in range(0, len(teacherList)):
                    for p in range(0, len(teacherList[k].subjectList)):
                        if any( grade in teacherList[i].subjectList[j].grade for grade in teacherList[k].subjectList[p].grade) and teacherList[i].subjectList[j].name != teacherList[k].subjectList[p].name :
                            #print "TeacherList["+str(i)+"].subjectList["+str(j)+"].period", " != ", "TeacherList["+str(k)+"].subjectList["+str(p)+"].period"
                            problem.addConstraint(lambda currentSubject, currentTeachersList: currentSubject != currentTeachersList,
                                            ("TeacherList["+str(i)+"].subjectList["+str(j)+"].period", "TeacherList["+str(k)+"].subjectList["+str(p)+"].period"))

    print ("solving.....")
    solutions = problem.getSolutions()
    print ("Done!")
    if not bool(solutions):
        print "No solution found"
        exit()

    print ("compressing...")
    finalList= []
    for x in range(0,len(solutions)):
        tempList = deepcopy(teacherList)
        for i in range(0, len(teacherList)):
            for j in range(0, len(tempList[i].subjectList)):
                tempList[i].subjectList[j].period = solutions[x].get("TeacherList[" + str(i) + "].subjectList[" + str(j) + "].period")

        tempList = compress (tempList)
        finalList.append(tempList)
    print ("Done!")

    return finalList

def compress (teacherList):
    for i in range(0,len(teacherList)):
        for j in range(0, len(teacherList[i].subjectList)):

            if not teacherList[i].subjectList[j].mathClass:

                for k in range(j+1,len(teacherList[i].subjectList)):
                    if teacherList[i].subjectList[j].period == teacherList[i].subjectList[k].period:
                        if teacherList[i].subjectList[j].name == teacherList[i].subjectList[k].name:
                            if teacherList[i].subjectList[j].grade[0][0] == teacherList[i].subjectList[k].grade[0][0]:
                                #print "compressing"
                                #print teacherList[i].subjectList[j].name, " == ", teacherList[i].subjectList[k].name
                                #print teacherList[i].subjectList[j].period, " == ", teacherList[i].subjectList[k].period
                                #print teacherList[i].subjectList[j].grade, " == ", teacherList[i].subjectList[k].grade

                                teacherList[i].subjectList[j].grade.append(teacherList[i].subjectList[k].grade[0])
                                #print "becomes"
                                #print teacherList[i].subjectList[j].name
                                #print teacherList[i].subjectList[j].period
                                #print teacherList[i].subjectList[j].grade

                                #print "removing"
                                #print teacherList[i].subjectList[k].name
                                #print teacherList[i].subjectList[k].period
                                #print teacherList[i].subjectList[k].grade
                                #print "\n"
                                del teacherList[i].subjectList[k]
                                return compress(teacherList)

    return teacherList
