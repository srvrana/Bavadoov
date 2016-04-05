from constraint import *
from Classes import*

def solve(teacherList):
    problem = Problem()
    for i in range(0, len(teacherList)):
        for j in range(0, len(teacherList[i].subjectList)):
            problem.addVariable("TeacherList[" + str(i) +"].subjectList[" + str(j) +"].period", teacherList[i].aval)
            for l in range(j, len(teacherList[i].subjectList)):
                if j != l:
                    #print "TeacherList["+str(i)+"].subjectList["+str(j)+"].period", " != " "TeacherList["+str(i)+"].subjectList["+str(l)+"].period"
                    problem.addConstraint(lambda currentSubject, currentTeachersList: currentSubject != currentTeachersList,
                                          ("TeacherList["+str(i)+"].subjectList["+str(j)+"].period", "TeacherList["+str(i)+"].subjectList["+str(l)+"].period"))


            for k in range(i, len(teacherList)):
                for p in range(j, len(teacherList[k].subjectList)):
                 if  teacherList[i].subjectList[j].grade == teacherList[k].subjectList[p].grade and (i!=k or j!=p):
                    #print "TeacherList["+str(i)+"].subjectList["+str(j)+"].period", " != ", "TeacherList["+str(k)+"].subjectList["+str(p)+"].period"
                    problem.addConstraint(lambda currentSubject, currentTeachersList: currentSubject != currentTeachersList,
                                          ("TeacherList["+str(i)+"].subjectList["+str(j)+"].period", "TeacherList["+str(k)+"].subjectList["+str(p)+"].period"))


    solution = problem.getSolution()

    if not bool(solution):
        print "No solution found"
        exit()

    for i in range(0, len(teacherList)):
        for j in range(0, len(teacherList[i].subjectList)):
            teacherList[i].subjectList[j].period = solution.get("TeacherList[" + str(i) + "].subjectList[" + str(j) + "].period")

    return teacherList

