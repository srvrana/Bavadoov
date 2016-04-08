class Block:
	time = ""
	part = []

class Day:
	doW = ""
	subject = ""

class Subject:
    def __init__(self,name,grade, mathClass ):
        self.name=name
        self.grade=grade # List of strings
        self.period = 0
        self.mathClass = mathClass


class Teacher:
    def __init__(self,name,aval):
        self.name = name
        self.aval = aval #List of ints
        self.subjectList = []
        self.type = ""
        self.designation = ""
        self.startTime = ""
        self.endTime = ""
        self.homeRoom = ""  #String
