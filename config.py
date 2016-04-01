import os
#.............................................
# Database configuration
#.............................................
# edit the URI below to add your RDS password and your AWS URL
# The other elements are the same as used in the tutorial
# format: (user):(password)@(db_identifier).amazonaws.com:3306/(db_name)

#SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://<db_user>:<db_password>@<endpoint>/<db_url>'

# Uncomment the line below if you want to work with a local DB
#SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'

def getDBURI(filePath):
	if 'RDS_HOSTNAME' in os.environ:
		print "...in AWS branch of config.py.getDBURI()....."
		db = {	'ENGINE': 'mysql+pymysql',
				'NAME': os.environ['RDS_DB_NAME'],
				'USER': os.environ['RDS_USERNAME'],
				'PASSWORD': os.environ['RDS_PASSWORD'],
				'HOST': os.environ['RDS_HOSTNAME'],
				'PORT': os.environ['RDS_PORT'],
		}
		#SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://<db_user>:<db_password>@<endpoint>/<db_url>'
		SQLALCHEMY_DATABASE_URI = db['ENGINE'],"://",db['USER'],":",db['PASSWORD'],"@",db['HOST'],"/",db['NAME']
	else:
		print "...in local branch in config.py.getDBURI()....."
		file = open(filePath, "r")
		SQLALCHEMY_DATABASE_URI = file.read()
	
	return SQLALCHEMY_DATABASE_URI

SQLALCHEMY_DATABASE_URI = getDBURI("./gitIgnored/SQLALCHEMY_DATABASE_URI.txt")
print "...SQLALCHEMY_DATABASE_URI : %s" % SQLALCHEMY_DATABASE_URI

#.............................................
# Oauth2 configuration
#.............................................
"""
GOOGLE_LOGIN_CLIENT_ID = "<your-id-ending-with>/apps.googleusercontent.com"
GOOGLE_LOGIN_CLIENT_SECRET = "<your-secret>"

OAUTH_CREDENTIALS={
		'google': {
			'id': GOOGLE_LOGIN_CLIENT_ID,
			'secret': GOOGLE_LOGIN_CLIENT_SECRET
		}
}"""
#.............................................
# Other things
#.............................................

SQLALCHEMY_POOL_RECYCLE = 3600

WTF_CSRF_ENABLED = True
SECRET_KEY = 'dsaf0897sfdg45sfdgfdsaqzdf98sdf0a'