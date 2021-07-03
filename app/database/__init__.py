from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from app import app
from flask_mail import Mail, Message

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:huyger66@it2-db.cpnlkwyl2llm.ap-southeast-1.rds.amazonaws.com:3306/cvsearchdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

mysql_db = SQLAlchemy(app)
migrate = Migrate(app, mysql_db)
marshmallow = Marshmallow(app) 
