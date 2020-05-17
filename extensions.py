from flask_login import LoginManager
from playhouse.flask_utils import FlaskDB
from flask_bcrypt import Bcrypt

login_manager = LoginManager()
database = FlaskDB()
bcrypt = Bcrypt()
