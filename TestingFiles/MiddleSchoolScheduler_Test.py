from MiddleSchoolScheduler import*
from Classes import*


Cooper =  Teacher("Cooper",[1,2,3,4])
Cooper.subjectList.append(Subject("Math 4 Alg B", ["8B"], True))
Cooper.subjectList.append(Subject("Math 4 Alg A", ["7B","8A"], True))
Cooper.subjectList.append(Subject("Math 3", ["6B","7A"], True))
Cooper.subjectList.append(Subject("Math 2", ["6A"], True))


Rae = Teacher("Rae", [1,2,3,4])
Rae.subjectList.append(Subject("Spanish", ["6A"], False))
Rae.subjectList.append(Subject("Spanish", ["6B"], False))
Rae.subjectList.append(Subject("Spanish", ["8B"], False))
Rae.subjectList.append(Subject("Spanish", ["8A"], False))
Rae.subjectList.append(Subject("Spanish", ["7B"], False))
Rae.subjectList.append(Subject("Spanish", ["7A"], False))


Salazar = Teacher("Salazar", [1,2,3,4])
Salazar.subjectList.append(Subject("SS", ["6B"], False))
Salazar.subjectList.append(Subject("SS", ["6A"], False))
Salazar.subjectList.append(Subject("SS", ["7B"], False))
Salazar.subjectList.append(Subject("SS", ["7A"], False))
Salazar.subjectList.append(Subject("SS", ["8A"], False))
Salazar.subjectList.append(Subject("SS", ["8B"], False))

Scott = Teacher("Scott", [1,2,3,4])
Scott.subjectList.append(Subject("Sci", ["6B"], False))
Scott.subjectList.append(Subject("Sci", ["6A"], False))
Scott.subjectList.append(Subject("Sci", ["7A"], False))
Scott.subjectList.append(Subject("Sci", ["7B"], False))
Scott.subjectList.append(Subject("Sci", ["8B"], False))
Scott.subjectList.append(Subject("Sci", ["8A"], False))

teacherList = [Cooper, Rae, Salazar, Scott]
teacherList = schedule(teacherList)


for i in range(0, len(teacherList)):
    for j in range(0, len(teacherList[i].subjectList)):
        for l in range(j+1, len(teacherList[i].subjectList)):
            if teacherList[i].subjectList[j].period == teacherList[i].subjectList[l].period:
                print "Scheduling Error:\n", "teacherList[",i,"].subjectList[",j,"].period Equals == teacherList[",i,"].subjectList[",l,"].period"
                print "Period ", teacherList[i].subjectList[j].period, " == ", teacherList[i].subjectList[l].period
                print "name " , teacherList[i].subjectList[j].name,  " == ", teacherList[i].subjectList[l].name
                print "grade " , teacherList[i].subjectList[j].grade,  " == ", teacherList[i].subjectList[l].grade

                exit()

for i in range(0, len(teacherList)):
    print "________"
    print teacherList[i].name
    print "--------"
    for j in range(0, len(teacherList[i].subjectList)):
        print "Period: ", teacherList[i].subjectList[j].period

for grade in range(6,9):
    for block in ["A","B"]:
        currentGrade = str(grade)+block
        print"_________"
        print "Grade: ", currentGrade
        print"---------"
        for i in range(0, len(teacherList)):
            for j in range(0, len(teacherList[i].subjectList)):
                if currentGrade in teacherList[i].subjectList[j].grade:
                    print  teacherList[i].subjectList[j].period, "\t", teacherList[i].subjectList[j].name

