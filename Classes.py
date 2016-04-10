class Block:
	time = ""
	part = []

class Day:
	doW = ""
	subject = ""

class Subject:
    def __init__(self):
        self.name=""
        self.grade=[] # List of strings
        self.period = 0
        self.mathClass = False


class Teacher:
    def __init__(self):
        self.name = ""
        self.aval = [] #List of ints
        self.subjectList = []
        self.type = ""
        self.designation = ""
        self.startTime = ""
        self.endTime = ""
        self.homeRoom = ""  #String
