class Teacher:
	name = ""
	type = ""
	designation = ""
	startTime = ""
	endTime = ""
	#Will be array of blocks
	schedule = []

class Block:
	time = ""
	#Will be an array of days
	part = []

class Day:
	#Day of week
	doW = ""
	subject = ""