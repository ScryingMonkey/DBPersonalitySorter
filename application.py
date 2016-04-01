from flask import Flask, render_template, request, redirect,jsonify, url_for, flash
from flask.ext.login import login_user, logout_user, current_user, login_required
from application.models import Data, Users, Questions, Results
from application.forms import EnterDBInfo, RetrieveDBInfo
from application.logic import *
from flask import session as login_session
from flask import make_response
import random, string
#from oauth2client.client import flow_from_clientsecrets, FlowExchangeError
#import httplib2
import json
#import requests
from application import db
import random

# Elastic Beanstalk initalization
application = Flask(__name__)
application.debug=True
# change this to your own value
application.secret_key = 'cC1YCIWOj9GgWspgNEo2'   




#.............................................................................................
#.....GET Requests.............................................................................
#.............................................................................................

# test app from tutorial
@application.route('/test', methods=['GET', 'POST'])
def flaskTutorial():
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
	questions = getQuestions()
	return render_template('questions.html', questions=questions)

# Pull all stored results from database and display them
@application.route('/allResults')
def showAllScores():
	print "...in showAllScores............."
	results = db.session.query(Users, Results).filter(Users.id == Results.user_id ).order_by(Users.id).all()
	for result in results:
		print result[0].name
	return render_template('allScores.html', results=results)

# login page
@application.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))
    return render_template('login.html',
                           title='Sign In')
	
#.............................................................................................
#.....POST Requests.............................................................................
#.............................................................................................

# Show results
@application.route('/results', methods=['GET','POST'])
def showResults():
	print "...In showResults().................."
	if request.method == 'POST':
		#print "...in /results if POST......"
		NumberOfQuestions = len(getQuestions()) #<---- should be a multiple of 7
		print "Number of questions: %s" % NumberOfQuestions
		results = {}
		for n in range(1,NumberOfQuestions+1): #<--- change this to iterate over number of rows in the Questions table
			result = "result" + str(n)	
			#print result
			results.update({n:str(request.form[result])})
		#user_id=login_session['user_id'])
		userName = "DummyUser02"
		# send a user name, get a user object
		user = getUser(userName)
		user_id = user.id #<---- change this to query User table based on name of logged in user
		userName = user.name
		# send dictionary results, get a dictionary of scores and adds scores as a row in the Results table
		scores = addResult(results, user_id)
		#flash('New Menu %s Item Successfully Created' % (newItem.name))
		flash('New Results Successfully Saved')
		return render_template('results.html', scores = scores, userName = userName)
	else:
		return render_template('questions.html')
	
#.............................................................................................
#.....Helper requests.............................................................................
#.............................................................................................

@application.route('/authorize/<provider>')
def oauth_authorize(provider):
    # Flask-Login function
    if not current_user.is_anonymous():
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()

@application.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous():
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    username, email = oauth.callback()
    if email is None:
        # I need a valid email address for my user identification
        flash('Authentication failed.')
        return redirect(url_for('index'))
    # Look if the user already exists
    user=User.query.filter_by(email=email).first()
    if not user:
        # Create the user. Try and use their name returned by Google,
        # but if it is not set, split the email address at the @.
        nickname = username
        if nickname is None or nickname == "":
            nickname = email.split('@')[0]

        # We can do more work here to ensure a unique nickname, if you 
        # require that.
        user=User(nickname=nickname, email=email)
        db.session.add(user)
        db.session.commit()
    # Log in the user, by default remembering them for their next visit
    # unless they log out.
    login_user(user, remember=True)
    return redirect(url_for('index'))

#.............................................................................................
#.....Boiler plate.............................................................................
#.............................................................................................


if __name__ == '__main__':
    #application.run(host='0.0.0.0')<---works on aws eb
	application.run(host = '0.0.0.0', port = 5000)
