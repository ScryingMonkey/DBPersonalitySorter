from application.models import Data, Users, Questions, Results
from application.logic import addUser
from application import db

addUser("DummyUser04", "dummy4@domain.com", "password")