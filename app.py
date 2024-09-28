from flask import Flask
from config import Config
from database import db
from routes import routes

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

app.register_blueprint(routes)

from models import Base

with app.app_context():
    Base.metadata.create_all(db.engine)
    
if __name__ == '__main__':
    app.run(debug=True)