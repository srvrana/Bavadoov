from MiddleSchoolScheduler import*
from Classes import*
import timeit


Cooper =  Teacher()
Cooper.name = "Cooper"
Cooper.homeRoom = "6"
Cooper.aval = [1,2,3,4,5]
Cooper.subjectList.append(Subject())
Cooper.subjectList[-1].name = "Math 4 Alg B"
Cooper.subjectList[-1].grade = ["8B"]

Cooper.subjectList.append(Subject())
Cooper.subjectList[-1].name = "Math 4 Alg A"
Cooper.subjectList[-1].grade = ["7B","8A"]

Cooper.subjectList.append(Subject())
Cooper.subjectList[-1].name = "Math 3"
Cooper.subjectList[-1].grade = ["6B","7A"]

Cooper.subjectList.append(Subject())
Cooper.subjectList[-1].name = "Math 2"
Cooper.subjectList[-1].grade = ["6A"]

for subject in Cooper.subjectList:
    subject.mathClass = True


Rae = Teacher()
Rae.name = "Rae"
Rae.aval = [1,2,3,4,5]
Rae.homeRoom = "7"
Rae.subjectList.append(Subject())
Rae.subjectList[-1].grade =["6A"]

Rae.subjectList.append(Subject())
Rae.subjectList[-1].grade =["6B"]

Rae.subjectList.append(Subject())
Rae.subjectList[-1].grade =["8B"]

Rae.subjectList.append(Subject())
Rae.subjectList[-1].grade =["8A"]

Rae.subjectList.append(Subject())
Rae.subjectList[-1].grade =["7B"]

Rae.subjectList.append(Subject())
Rae.subjectList[-1].grade =["7A"]

for subject in Rae.subjectList:
    subject.name = "Spanish"


Salazar = Teacher()
Salazar.name = "Salazar"
Salazar.aval = [1,2,3,4,5]
Salazar.homeRoom = "8A"
Salazar.subjectList.append(Subject())
Salazar.subjectList[-1].grade=["6B"]

Salazar.subjectList.append(Subject())
Salazar.subjectList[-1].grade=["6A"]

Salazar.subjectList.append(Subject())
Salazar.subjectList[-1].grade=["7B"]

Salazar.subjectList.append(Subject())
Salazar.subjectList[-1].grade=["7A"]

Salazar.subjectList.append(Subject())
Salazar.subjectList[-1].grade=["8A"]

Salazar.subjectList.append(Subject())
Salazar.subjectList[-1].grade=["8B"]

for subject in Salazar.subjectList:
    subject.name = "SS"


Scott = Teacher()
Scott.name = "Scott"
Scott.aval = [1,2,3,4,5]
Scott.homeRoom = "8B"
Scott.subjectList.append(Subject())
Scott.subjectList[-1].grade = ["6B"]

Scott.subjectList.append(Subject())
Scott.subjectList[-1].grade = ["6A"]

Scott.subjectList.append(Subject())
Scott.subjectList[-1].grade = ["7A"]

Scott.subjectList.append(Subject())
Scott.subjectList[-1].grade = ["7B"]

Scott.subjectList.append(Subject())
Scott.subjectList[-1].grade = ["8B"]

Scott.subjectList.append(Subject())
Scott.subjectList[-1].grade = ["8A"]

for subject in Scott.subjectList:
    subject.name = "Sci"

teacherList = [Salazar, Cooper, Rae, Scott]



print "Starting Middle school test script..."
start = timeit.default_timer()

#set bool to False to produce testfile.xml output file.
# if bool = False uncomment the exit statment below

#True + remove lower exit()  = what we'll use for actual testing script.
listOfSolutions = schedule(teacherList, "C:\Users\Spencer\Dropbox\Bavadoov\Output\TestingStuff.xls", False)


exit()

#print len(listOfSolutions), " solutions found.\nTesting for conflict..."

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
print "No conflict!"
print "RunTime: ",stop - start
