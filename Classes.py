class Block:
    def __init__(self):
	    self.time = ""
	    self.part = []

class Day:
    def __init__(self):
	    self.doW = ""
	    self.subject = ""

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
