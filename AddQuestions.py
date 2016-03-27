from application.models import Data, Users, Questions, Results
from application import db


# Drop all data in tables
def clearQuestions():
	try:
		questions = Questions.query.all()
		print "...queried successfully........."
		for q in questions:
			db.session.delete(q)
		print "...deleted successfully.........."
		db.session.commit()        
		print "...Questions successfully cleared.................."
	except:
		db.session.rollback()
		print "...Failed to clear Questions......................."
	finally:
		db.session.close()
	return
# Takes in a file path to a txt file and returns a list
# of dictionaries of questions gathered from the text file
def CollectQuestions(filePath):
	file = open(filePath, "r")
	questions = []
	n = 0
	for i, line in enumerate(file):
		print "line[:3]: %s" % line[:3]
		print "line %s: %s" % (n,line)
		if line[:3] == "[Q]":
			print "...if passed.........."
			n+=1
			iQ = line.find("[Q]")
			iA = line.find("(a)")
			iB = line.find("(b)")

			question = {'number' : n,
						'question': line[iQ+3:iA].strip(),
						'answerA': line[iA+3:iB].strip(),
						'answerB': line[iB+3:].strip()}
			print question
			questions.append(question)

		else:
			print "...Failed on collecting question: %s" % n
			continue
			
	file.close()
	return questions

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
		db.session.add(question)
		try:
			db.session.commit()        
			db.session.close()
		except:
			db.session.rollback()
	print "... ...exiting for loop"
	return


#clearQuestions()
path = "static\Keirsey_Sorter.txt"
#addQuestions(path)
testDB(Questions)