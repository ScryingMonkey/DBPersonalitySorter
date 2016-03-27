# edit the URI below to add your RDS password and your AWS URL
# The other elements are the same as used in the tutorial
# format: (user):(password)@(db_identifier).amazonaws.com:3306/(db_name)

#SQLALCHEMY_DATABASE_URI = ‘mysql+pymysql://<db_user>:<db_password>@<endpoint>/<db_url>’
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://dbroot:Blu3b3rryR0ck@aa1npu92ypyn8yt.cc6p0ojvcx3g.us-east-1.rds.amazonaws.com:3306/ebdb'

# Uncomment the line below if you want to work with a local DB
#SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'

SQLALCHEMY_POOL_RECYCLE = 3600

WTF_CSRF_ENABLED = True
SECRET_KEY = 'dsaf0897sfdg49995sfdgfdsaqzdf98sdf0a'
