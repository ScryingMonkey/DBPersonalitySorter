from application.models import Data, Users, Questions, Results
from application import db
from application import scoreResults


def testDB(table):
	try:
		questions = Questions.query.order_by(Questions.number)
	except:
		print "...Failed to query database................."
	for q in questions:
		print q.number
	print "First: %s %s" % (questions[0].number, questions[0].question)
	print "Last: %s %s" % (questions[-1].number, questions[-1].question)

	return

def testScoring(filePath):
	file = open(filePath, "r")
	results = {}
	for line in file:
		#print result
		origin = 0
		iColon = line.find(":", origin)
		iComma = line.find(",", origin)
		results.update({line[origin:iColon]:line[iColon+1:iComma]})
		origin = iComma+1
	print "Results: %s" % results
	# send dictionary results, returns dictionary scores
	scores = scoreResults(results)
	print "Scores: %s" % scores
	return 
	

testScoring("./static/testSurvey01.txt")