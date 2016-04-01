import os

# edit the URI below to add your RDS password and your AWS URL
# The other elements are the same as used in the tutorial
# format: (user):(password)@(db_identifier).amazonaws.com:3306/(db_name)

#SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://<db_user>:<db_password>@<endpoint>/<db_url>'
#SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://dbroot:Blu3b3rryR0ck@aa1npu92ypyn8yt.cc6p0ojvcx3g.us-east-1.rds.amazonaws.com:3306/ebdb'

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
		filePath = "./gitIgnored/SQLALCHEMY_DATABASE_URI.txt"
		file = open(filePath, "r")
		SQLALCHEMY_DATABASE_URI = file.read()
		
	print "...SQLALCHEMY_DATABASE_URI : %s" % SQLALCHEMY_DATABASE_URI
	return SQLALCHEMY_DATABASE_URI



	
SQLALCHEMY_POOL_RECYCLE = 3600

WTF_CSRF_ENABLED = True
SECRET_KEY = 'dsaf0897sfdg45sfdgfdsaqzdf98sdf0a'

def test():
	getDBURI("./gitIgnored/SQLALCHEMY_DATABASE_URI.txt")
	
test()