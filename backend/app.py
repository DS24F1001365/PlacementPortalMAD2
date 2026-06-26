from flask import Flask
from flask_cors import CORS

from models import db
from models import create_admin


app = Flask(__name__)

CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ppa.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()
    create_admin()

if __name__ == "__main__":

    app.run(debug=True)