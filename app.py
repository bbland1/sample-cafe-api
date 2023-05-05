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

## HTTP GET - Read Record

# all records
@app.route("/all")
def all_cafes():
    # look into database & get all the cafes
    cafes = db.session.execute(db.select(Cafe).order_by(Cafe.id)).scalars().all()
    # list comprehension to make dicts of each cafe in list
    all_cafes_dict = [cafe.as_dict() for cafe in cafes] 
    # pass the list into a json of cafes 
    return jsonify(cafes=all_cafes_dict)

# random record
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

# search for a record by location
@app.route("/search")
def search_cafe():
    # get the the query params of the location
    cafe_location = request.args.get("location")
    # search the database
    found_cafes = db.session.execute(db.select(Cafe).filter_by(location=cafe_location)).scalars().all()
    # create a dict of the found cafe
    found_cafes_dict = [cafe.as_dict() for cafe in found_cafes]
    # check if the found_cafes_dict is empty then return specific message if it is
    if len(found_cafes_dict) == 0:
        # sends an error response with a specific error code
        return jsonify(error={"Not Found": "Sorry, we don't have any cafes at that location."}), 400
    # return the json
    return jsonify(cafes=found_cafes_dict)

## HTTP POST - Create Record

# add a cafe to the database with api call
@app.route("/add", methods=["POST"])
def add_cafe():
    # get the request body info and create the new cafe using the model
    # check if the data is json or from encoded
    if request.is_json:
        cafe_to_add = request.get_json()
    else:
        cafe_to_add = request.form

    # print(cafe_to_add)
    # validate the data sent to make sure the database required data is there
    required_fields = ["name", "map_url", "img_url", "location", "seats", "has_toilet", "has_wifi", "has_sockets", "can_take_calls"]
    if not all(field in cafe_to_add for field in required_fields):
        # sends an error response with a specific error code
        return jsonify(error={"Not Found": "Sorry you had an empty field."}), 400
    
    # set all the required fields of the form
    new_cafe = Cafe(
        name= cafe_to_add["name"],
        map_url= cafe_to_add["map_url"],
        img_url= cafe_to_add["img_url"],
        location= cafe_to_add["location"],
        seats= cafe_to_add["seats"],
        # these need to be booleans in the database so we wrap the calls in bool to convert
        has_toilet= bool(cafe_to_add["has_toilet"]),
        has_wifi= bool(cafe_to_add["has_wifi"]),
        has_sockets= bool(cafe_to_add["has_sockets"]),
        can_take_calls= bool(cafe_to_add["can_take_calls"]),
        coffee_price= cafe_to_add["coffee_price"],
    )
    # add to database with add & commit
    db.session.add(new_cafe)
    db.session.commit()
    # return success response
    return jsonify(response={"success": "New cafe was added to the database."})

## HTTP PUT/PATCH - Update Record

## HTTP DELETE - Delete Record


if __name__ == '__main__':
    app.run()
