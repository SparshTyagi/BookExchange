from flask import Flask
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from config import Config
from database import db
from routes import routes
from models import Base, UserProfile

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'routes.login'


app.register_blueprint(routes)


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(UserProfile).get(int(user_id))
    

if __name__ == '__main__':
    with app.app_context():
        Base.metadata.create_all(db.engine)
    app.run(debug=True)