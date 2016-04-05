class Block:
	time = ""
	#Will be an array of days
	part = []

class Day:
	#Day of week
	doW = ""
	subject = ""

class Subject:
    def __init__(self,name,grade):
        self.name=name
        self.grade=grade
        self.period = 0


class Teacher:
    def __init__(self,name,aval):
        self.name = name
        self.aval = aval
        self.subjectList = []