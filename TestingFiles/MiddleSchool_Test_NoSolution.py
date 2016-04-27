from MiddleSchoolScheduler import*
from Classes import*
import timeit


def test():
    """
    Test Script:
    Should return 0 results, as the schedual is imposable to form.
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



    Rae = Teacher()
    Rae.name = "Rae"
    Rae.aval = [1,2,3,4,5,6]
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
    Salazar.aval = [1,2,3]
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
    Scott.aval = [1,2,3]
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

    listOfSolutions = schedule(teacherList, "C:\Users\Spencer\Dropbox\Bavadoov\Output\TestingStuff.xls", True)



    print len(listOfSolutions), " solutions found.\n"
    if len(listOfSolutions) ==0:
        print "This is correct"
    else:
        print "Error!  This is an imposable schedule."

if __name__ == "__main__":
    test()
