from flask import Flask, jsonify, render_template, request
from flask_migrate import Migrate

from models import Cafe, db

app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

migrate = Migrate(app, db)


@app.route("/")
def home():
    return render_template("index.html")
    

# a route to pull a random cafe from sample data
@app.route("/random")
def random():
    pass
## HTTP GET - Read Record

## HTTP POST - Create Record

## HTTP PUT/PATCH - Update Record

## HTTP DELETE - Delete Record


if __name__ == '__main__':
    app.run(debug=True)
