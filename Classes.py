class Teacher:
	name = ""
	type = ""
	designation = ""
	startTime = ""
	endTime = ""
	#Will be array of blocks
	schedule = []

class Block:
	Time = ""
	DayLayout =""
	#Will be an array of days
	Parts = []

class Days:
	#Day of week
	DoW = ""
	Subject = ""