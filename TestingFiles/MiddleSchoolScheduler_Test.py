from MiddleSchoolScheduler import*
from Classes import*
import timeit


Cooper =  Teacher("Cooper",[1,2,3,4,5])
Cooper.homeRoom = "6"
Cooper.subjectList.append(Subject("Math 4 Alg B", ["8B"], True))
Cooper.subjectList.append(Subject("Math 4 Alg A", ["7B","8A"], True))
Cooper.subjectList.append(Subject("Math 3", ["6B","7A"], True))
Cooper.subjectList.append(Subject("Math 2", ["6A"], True))


Rae = Teacher("Rae", [1,2,3,4])
Rae.homeRoom = "7"
Rae.subjectList.append(Subject("Spanish", ["6A"], False))
Rae.subjectList.append(Subject("Spanish", ["6B"], False))
Rae.subjectList.append(Subject("Spanish", ["8B"], False))
Rae.subjectList.append(Subject("Spanish", ["8A"], False))
Rae.subjectList.append(Subject("Spanish", ["7B"], False))
Rae.subjectList.append(Subject("Spanish", ["7A"], False))


Salazar = Teacher("Salazar", [1,2,3,4])
Salazar.homeRoom = "8A"
Salazar.subjectList.append(Subject("SS", ["6B"], False))
Salazar.subjectList.append(Subject("SS", ["6A"], False))
Salazar.subjectList.append(Subject("SS", ["7B"], False))
Salazar.subjectList.append(Subject("SS", ["7A"], False))
Salazar.subjectList.append(Subject("SS", ["8A"], False))
Salazar.subjectList.append(Subject("SS", ["8B"], False))

Scott = Teacher("Scott", [1,2,3,4])
Scott.homeRoom = "8B"
Scott.subjectList.append(Subject("Sci", ["6B"], False))
Scott.subjectList.append(Subject("Sci", ["6A"], False))
Scott.subjectList.append(Subject("Sci", ["7A"], False))
Scott.subjectList.append(Subject("Sci", ["7B"], False))
Scott.subjectList.append(Subject("Sci", ["8B"], False))
Scott.subjectList.append(Subject("Sci", ["8A"], False))

teacherList = [Cooper, Rae, Salazar, Scott]
start = timeit.default_timer()
listOfSolutions = schedule(teacherList)


print len(listOfSolutions), " found.\nTesting for conflict..."

for teacherList in listOfSolutions:
    for i in range(0, len(teacherList)):
        for j in range(0, len(teacherList[i].subjectList)):
            for l in range(j+1, len(teacherList[i].subjectList)):
                if teacherList[i].subjectList[j].period == teacherList[i].subjectList[l].period:
                    print "Scheduling Error:\n", "teacherList[",i,"].subjectList[",j,"].period Equals == teacherList[",i,"].subjectList[",l,"].period"
                    print "Period ", teacherList[i].subjectList[j].period, " == ", teacherList[i].subjectList[l].period
                    print "name " , teacherList[i].subjectList[j].name,  " == ", teacherList[i].subjectList[l].name
                    print "grade " , teacherList[i].subjectList[j].grade,  " == ", teacherList[i].subjectList[l].grade
                    print "List index: ", i
                    exit()

            for k in range(0,len(teacherList)):
                for p in range(0,len(teacherList[k].subjectList)):
                    if k!= i or p != j:
                        if any(grade in teacherList[k].subjectList[p].grade for grade in teacherList[i].subjectList[j].grade) and teacherList[k].subjectList[p].period == teacherList[i].subjectList[j].period:
                            print "Scheduling Error:\n", "teacherList[",i,"].subjectList[",j,"].grade == teacherList[",k,"].subjectList[",p,"].grade"
                            print "Period ", teacherList[i].subjectList[j].period, " == ", teacherList[k].subjectList[p].period
                            print "name " , teacherList[i].subjectList[j].name,  " == ", teacherList[k].subjectList[p].name
                            print "grade " , teacherList[i].subjectList[j].grade,  " == ", teacherList[k].subjectList[p].grade
                            print "List index: ", i
                            exit()

stop = timeit.default_timer()
print "No conflict.. man Spencer's Handsome.."
print "RunTime: ",stop - start
    #for i in range(0, len(teacherList)):
        #print "________"
        #print teacherList[i].name
        #print "--------"
        #for j in range(0, len(teacherList[i].subjectList)):
            #print "Period: ", teacherList[i].subjectList[j].period, teacherList[i].subjectList[j].name, teacherList[i].subjectList[j].grade

    #for grade in range(6,9):
        #for block in ["A","B"]:
            #currentGrade = str(grade)+block
            #print"_________"
            #print "Grade: ", currentGrade
            #print"---------"
            #for i in range(0, len(teacherList)):
                #for j in range(0, len(teacherList[i].subjectList)):
                    #if currentGrade in teacherList[i].subjectList[j].grade:
                        #print  teacherList[i].subjectList[j].period, "\t", teacherList[i].subjectList[j].name

