from application.models import Data, Users, Questions, Results
from application import db
from config import getFakeDBURI, getDBURI

# Takes in a dictionary of results (question1=a, question2=b, etc)
# Returns a dictionary of scores for each personality aspect (ex. N = 18)
def scoreResultsDBPSorter(results):
	print "...In scoreResults............"
	NumberOfQuestions = len(results) #<---- should be a multiple of 7
	#print "Number of questions: %s" % NumberOfQuestions
	scores = {'e':0, 'i':0, 's':0, 'n':0, 't':0, 'f':0, 'j':0, 'p':0}
	personalities = ['z','e','i','s','n','s','n','t','f','t','f','j','p','j','p']
	print "...before scoring: %s ................." % scores
	for x in range(0, NumberOfQuestions/7): #<-----------------------this must be NumberOfQuestions/7
		for i,a in enumerate(range(1,14,2)):
			b = a+1
			#print i+1+x*7,a,b
			if results[i+1+x*7] == 'a':
				scores[personalities[a]] += 1
			elif results[i+1+x*7] == 'b':
				scores[personalities[b]] += 1
			else:
				print "...ERROR in scoreResutls(): Invalid input on question %s ............." % str(n+7*x)
	print "...after scoring: %s ..............." % scores
	
	return scores

# Add a row to the Users table	
def addUser(userName, userEmail, userPassword):
	"""
	Add Dummy user to Users Database
	"""
	#Add dummy user to database		
	user = Users(name = userName,
				email = userEmail,
				password = userPassword)
	print "...Adding user: %s. %s..." %(userName, userEmail)
	db.session.add(user)
	try:
		db.session.commit()        
		db.session.close()
		print "...Successfully added user: %s. %s..." %(userName, userEmail)
	except:
		print "...Failed to commit........."
		db.session.rollback()
		raise
	return

# Add a row to the Results table
# takes in a dictionary of scores
def addResult(results, id):
	scores = scoreResultsDBPSorter(results)	
	# ToDo: Include user id in commit in order to store results by user using Oauth2
	newResults = Results(user_id = id,#<----------fix this when login is logging users in db
						I = scores['i'],
						E = scores['e'],
						N = scores['n'],
						S = scores['s'],
						T = scores['t'],
						F = scores['f'],
						J = scores['j'],
						P = scores['p'])
	db.session.add(newResults)
	try:
		db.session.commit()        
		db.session.close()
		print "...Successfully added newResults: %s" % scores
	except:
		print "...Failed to commit........."
		db.session.rollback()
		raise
	return scores

# returns a query object of Questions.all() ordered by number
def getQuestions():
	print "...getting Questions............"
	DATABASE = getDBURI("./gitIgnored/SQLALCHEMY_DATABASE_URI.txt")
	print "...Querying database: %s" % DATABASE
	try:
		questions = Questions.query.order_by(Questions.number).all()
		print "...Successfully queried Questions.query.order_by(Questions.number).all()......"
	except:
		print "...Failed to query Questions.query.order_by(Questions.number).all()................."
		raise
	return questions

# returns a query object of Results.all()
def getResults():
	try:
		results = Results.query.all()
		print "...Successfully queried Results.query.all()......"
	except:
		print "...Failed to query Results.query.all()................."
		raise
	return results

# returns a query object of Users.all()
def getUsers():
	try:
		users = Users.query.all()
		print "...Successfully queried Users.query.all()......"
	except:
		print "...Failed to query Users.query.all()................."
		raise
	return users
	
#take in user name, query User table and return user object
def getUser(userName):
	users = getUsers()
	print "............................................"
	print "...Users:"
	for u in users:
		print "......user %s, name: %s" % (u.id,u.name)
	print "............................................"
	print "...Looking for user: %s" % userName
	user = Users.query.filter_by(name = userName).first()
	print "...returning user: %s" % user.name
	return user