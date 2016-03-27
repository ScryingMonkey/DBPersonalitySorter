from flask import Flask, render_template, request, redirect,jsonify, url_for, flash
from application.models import Data, Users, Questions, Results
from application.forms import EnterDBInfo, RetrieveDBInfo
from flask import session as login_session
from flask import make_response
import random, string
#from oauth2client.client import flow_from_clientsecrets, FlowExchangeError
#import httplib2
import json
#import requests
from application import db



# Elastic Beanstalk initalization
application = Flask(__name__)
application.debug=True
# change this to your own value
application.secret_key = 'cC1YCIWOj9GgWspgNEo2'   

#.............................................................................................
#.....Helper functions.............................................................................
#.............................................................................................

# Takes in a dictionary of results (question1=a, question2=b, etc)
# Returns a dictionary of scores for each personality aspect (ex. N = 18)
def scoreResults(results):
	print "...In scoreResults............"
	scores = {'e':0, 'i':0, 's':0, 'n':0, 't':0, 'f':0, 'j':0, 'p':0}
	personalities = ['z','e','i','s','n','s','n','t','f','t','f','j','p','j','p']
	print "...before scoring: %s ................." % scores
	for x in range(0,10): #<-----------------------this must be corrected to 0,10 once the db is corrected to have 70 questions
		for i,a in enumerate(range(1,14,2)):
			b = a+1
			print i+1+x*7,a,b
			if results[i+1+x*7] == 'a':
				scores[personalities[a]] += 1
			elif results[i+1+x*7] == 'b':
				scores[personalities[b]] += 1
			else:
				print "...ERROR in scoreResutls(): Invalid input on question %s ............." % str(n+7*x)
	print "...after scoring: %s ..............." % scores
	
	return scores


#.............................................................................................
#.....GET Requests.............................................................................
#.............................................................................................

# test app from tutorial
@application.route('/test', methods=['GET', 'POST'])
def index():
    print "...in /test.................."
    form1 = EnterDBInfo(request.form) 
    form2 = RetrieveDBInfo(request.form) 
    
    if request.method == 'POST' and form1.validate():
        data_entered = Data(notes=form1.dbNotes.data)
        try:     
            db.session.add(data_entered)
            db.session.commit()        
            db.session.close()
        except:
            db.session.rollback()
        return render_template('thanks.html', notes=form1.dbNotes.data)
        
    if request.method == 'POST' and form2.validate():
        try:   
            num_return = int(form2.numRetrieve.data)
            query_db = Data.query.order_by(Data.id.desc()).limit(num_return)
            for q in query_db:
                print(q.notes)
            db.session.close()
        except:
            db.session.rollback()
        return render_template('results.html', results=query_db, num_return=num_return)                
    
    return render_template('index.html', form1=form1, form2=form2)

# test html
@application.route('/testApp', methods=['GET'])
def testApp():
	return render_template('testing00.html')

# Show all Questions
@application.route('/', methods=['GET'])
@application.route('/index', methods=['GET'])
@application.route('/questions', methods=['GET'])
def showQuestions():
	try:
		questions = Questions.query.order_by(Questions.number)
	except:
		print "...Failed to query database................."
	return render_template('questions.html', questions=questions)

# Pull all stored results from database and display them
@application.route('/allResults')
def showAllScores():
	scores = Results.query(Results).all()
	for score in scores:
		print score
	return render_template('allScores.html', scores=scores)
	
#.............................................................................................
#.....GET Requests.............................................................................
#.............................................................................................

# Show results
@application.route('/results', methods=['GET','POST'])
def showResults():
	print "...In showResults().................."
	if request.method == 'POST':
		#print "...in /results if POST......"
		results = {}
		for n in range(1,71):
			result = "result" + str(n)	
			#print result
			results.update({n:str(request.form[result])})
		print results
		# send dictionary results, returns dictionary scores
		scores = scoreResults(results)	
		# ToDo: Include user in commit in order to store results by user using Oauth2
		newResults = Results(I = scores['i'],
							E = scores['e'],
							N = scores['n'],
							S = scores['s'],
							T = scores['t'],
							F = scores['f'],
							J = scores['j'],
							P = scores['p'],)
		#user_id=login_session['user_id'])
		try:
			db.session.add(newResults)
			db.session.commit()        
			db.session.close()
		except:
			db.session.rollback()
		
		#flash('New Menu %s Item Successfully Created' % (newItem.name))
		flash('New Results Successfully Saved')
		db.session.commit()
		print "...session sucessfully committed.........."
		return render_template('results.html', scores = scores)
	else:
		return render_template('questions.html')
	


if __name__ == '__main__':
    application.run(host='0.0.0.0')
