from application import db

class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    notes = db.Column(db.String(128), index=True, unique=False)
    
    def __init__(self, notes):
        self.notes = notes

    def __repr__(self):
        return '<Data %r>' % self.notes


class Users(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(250), nullable=False)
	email = db.Column(db.String(250), unique=True, nullable=False)
	password = db.Column(db.String(250), nullable=False)
	def __init__(self, name, email, password, results):
		self.name = name
		self.email = email
		self.password = password
	def __repr__(self):
		return '<Users %r>' % self.name
	@property
	def serialize(self):
		"""Return object data in easily serializeable format"""
		return {
			'id'           : self.id,
			'name'         : self.name,
			'email'        : self.email,
		}

class Questions(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	number = db.Column(db.Integer, nullable=False, unique=True)
	question = db.Column(db.String(250), nullable=False)
	answerA = db.Column(db.String(250), nullable=False)
	answerB = db.Column(db.String(250), nullable=False)
	def __init__(self, number, question, answerA, answerB):
		self.number = number
		self.question = question
		self.answerA = answerA
		self.answerB = answerB
	def __repr__(self):
		return '<Questions %r>' % self.number
	@property
	def serialize(self):
		"""Return object data in easily serializeable format"""
		return {
			'id'         : self.id,
			'number'     : self.number,
			'question'   : self.question,
			'answerA'    : self.scoringA,
			'answerB'    : self.scoringB
		}
 
class Results(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
	users = db.relationship('Users', backref=db.backref('posts', lazy='dynamic'))
	I = db.Column(db.String(250))
	E = db.Column(db.String(250))
	N = db.Column(db.String(250))
	S = db.Column(db.String(250))
	T = db.Column(db.String(250))
	F = db.Column(db.String(250))
	J = db.Column(db.String(250))
	P = db.Column(db.String(250))
	def __init__(self, user_id, I, E, N, S, T, F, J, P):
		self.user_id = user_id
		self.I = I
		self.E = E
		self.N = N
		self.S = S
		self.T = T
		self.F = F
		self.J = J
		self.P = P
		#self.users = users
	def __repr__(self):
		return '<Results %r>' % self.id
	@property
	def serialize(self):
		"""Return object data in easily serializeable format"""
		return {
			'id'         : self.id,
			'user_id'    : self.user_id,
			'I'          : self.I,
			'E'          : self.E,
			'N'          : self.N,
			'S'          : self.S,
			'T'          : self.T,
			'F'          : self.F,
			'J'          : self.J,
			'P'          : self.P
        }