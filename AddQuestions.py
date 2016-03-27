from application.models import Data, Users, Questions, Results
from application import db


# Takes in a file path to a txt file and returns a list
# of dictionaries of questions gathered from the text file
def CollectQuestions(filePath):
    file = open(filePath, "r")
    questions = []
    n = 0
    for i, line in enumerate(file):
    #    print "line[:3]: %s" % line[:3]
    #    print "line:...%s" % line
        if line[:3] == "[Q]":
            n+=1
            iQ = line.find("[Q]")
            iA = line.find("(a)")
            iB = line.find("(b)")

            #print "q:...", line[iQ+3:iA].strip()
            #print "a:...", line[iA+3:iB].strip()
            #print "b:...", line[iB+3:].strip()
    #        for i, char in enumerate(line):
    #            if char ==
            question = {'number' : n,
                        'question': line[iQ+3:iA].strip(),
                        'answerA': line[iA+3:iB].strip(),
                        'answerB': line[iB+3:].strip()}
            #print question
            questions.append(question)

        else:
			continue
			
    return questions

#    for q in data:
#        print "%s. %s..." %(q['number'], q['question'])
#        print "(a) ", q['answerA']
#        print "(b) ", q['answerB']
#        print ""

    file.close()

def addQuestions(txtFilePath):
	"""
	Save data in the database
	The method is called for every item pipeline component.
	"""
	#Gather questions from txt file
	questionsList = CollectQuestions(txtFilePath)
	print "...questions gathered"
	#Add questions to database		
	for q in questionsList:
		print "... ...entering for loop"
		question = Questions(number = q['number'],
								  question = q['question'],
								  answerA = q['answerA'],
								  answerB = q['answerB'] )
		print "%s. %s..." %(q['number'], q['question'])
		try:     
			db.session.add(question)
			db.session.commit()        
			db.session.close()
		except:
			db.session.rollback()
	print "... ...exiting for loop"
	return

path = "static\Keirsey_Sorter.txt"
addQuestions(path)