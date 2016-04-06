class Block:
	time = ""
	part = []

class Day:
	doW = ""
	subject = ""

class Subject:
    def __init__(self,name,grade, mathClass ):
        self.name=name
        self.grade=grade
        self.period = 0
        self.mathClass = mathClass


class Teacher:
    def __init__(self,name,aval):
        self.name = name
        self.aval = aval
        self.subjectList = []
        self.type = ""
        self.designation = ""
        self.startTime = ""
        self.endTime = ""