import random
from flask import Flask, jsonify, render_template, request
from flask_migrate import Migrate
from sqlalchemy.sql.expression import func

from models import Cafe, db

app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

migrate = Migrate(app, db)

# with app.app_context():
#     db.create_all()


@app.route("/")
def home():
    return render_template("index.html")

# HTTP GET - all records
@app.route("/all")
def all_cafes():
    # look into database & get all the cafes
    cafes = db.session.execute(db.select(Cafe).order_by(Cafe.id)).scalars().all()
    # list comprehension to make dicts of each cafe in list
    all_cafes_dict = [cafe.as_dict() for cafe in cafes] 
    # pass the list into a json of cafes 
    return jsonify(cafes=all_cafes_dict)

# HTTP GET - random record
@app.route("/random")
def random_cafe():
    # look into the database
    # order the database randomly
    # take the first row
    random_cafe = db.session.execute(db.select(Cafe).order_by(func.random())).first()[0]
    # use the made dictionary method in the model to change info to dict
    cafe_dict = random_cafe.as_dict()
    # return json info
    return jsonify(cafe_dict)

## HTTP GET - Read Record

## HTTP POST - Create Record


## HTTP PUT/PATCH - Update Record

## HTTP DELETE - Delete Record


if __name__ == '__main__':
    app.run()
