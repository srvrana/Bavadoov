from MiddleSchoolScheduler import*


Bob =  Teacher("bob",[1,2,3])
Bob.subjectList.append(Subject("Math", 6))
Bob.subjectList.append(Subject("Math2", 7))
Bob.subjectList.append(Subject("Math3", 7))

Sue = Teacher("sue", [1,2,3])
Sue.subjectList.append(Subject("Art", 6))
Sue.subjectList.append(Subject("Art2", 6))
Sue.subjectList.append(Subject("Art2", 7))

Tom = Teacher("tom", [1,2,3])
Tom.subjectList.append(Subject("SS", 8))
Tom.subjectList.append(Subject("SS", 8))
Tom.subjectList.append(Subject("SS", 8))

teacherList = [Bob, Sue, Tom]


teacherList = solve(teacherList)


for i in range(0, len(teacherList)):
    for j in range(0, len(teacherList[i].subjectList)):
        for l in range(j+1, len(teacherList[i].subjectList)):
            if teacherList[i].subjectList[j].period == teacherList[i].subjectList[l].period:
                print "Scheduling Error:\n", "teacherList[",i,"].subjectList[",j,"].period Equals == teacherList[",i,"].subjectList[",l,"].period"
                print "Period ", teacherList[i].subjectList[j].period, " == ", teacherList[i].subjectList[l].period
                exit()

for i in range(0, len(teacherList)):
    print "________"
    print teacherList[i].name
    print "--------"
    for j in range(0, len(teacherList[i].subjectList)):
        print "Period: ", teacherList[i].subjectList[j].period


for grade in range(6,9):
    print"_________"
    print "Grade: ", grade
    print"---------"
    for i in range(0, len(teacherList)):
       for j in range(0, len(teacherList[i].subjectList)):
           if teacherList[i].subjectList[j].grade == grade:
               print teacherList[i].subjectList[j].name, "\t", teacherList[i].subjectList[j].period

