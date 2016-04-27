from MiddleSchoolScheduler import*
from Classes import*
import timeit




def test():
    """
    Test Script:
    This test only includes math classes. Should return valid schedules.
    """
    Cooper =  Teacher()
    Cooper.name = "Cooper"
    Cooper.homeRoom = "6"
    Cooper.aval = [1,2,3,4]
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


    teacherList = [ Cooper]



    print "Starting Middle school test script..."
    start = timeit.default_timer()

    listOfSolutions = schedule(teacherList, "C:\Users\Spencer\Dropbox\Bavadoov\Output\TestingStuff.xls", True)



    print len(listOfSolutions), " solutions found.\nTesting for conflict..."

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


if __name__ == "__main__":
    test()