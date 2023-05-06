import random
from flask import Flask, jsonify, render_template, request, abort
from flask_migrate import Migrate
from sqlalchemy.sql.expression import func, or_

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

## HTTP GET - Read Record

# all records
@app.route("/api/v1/cafes")
def all_cafes():
    # look into database & get all the cafes
    cafes = db.session.execute(db.select(Cafe).order_by(Cafe.id)).scalars().all()
    # list comprehension to make dicts of each cafe in list
    all_cafes_dict = [cafe.as_dict() for cafe in cafes] 
    # pass the list into a json of cafes 
    return jsonify(cafes=all_cafes_dict)

# random record
@app.route("/api/v1/cafes/random")
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
@app.route("/api/v1/cafes/search")
def search_location():
    # get query parameters
    cafe_location = request.args.get("loc")
    cafe_name = request.args.get("name")
    # search the database

    # check that one of the query parameters are actually passed if not get out
    if not cafe_name and not cafe_location:
        return jsonify(error={"Query Issue": "A query parameter wasn't passed."}), 400

    # set a search parameters to empty list
    search_params = []

    # if the cafe name is passed add it
    if cafe_name and not cafe_location:
        search_params.append(Cafe.name.contains(cafe_name))
    
    # if the cafe location is pass add it
    if cafe_location and not cafe_name:
        search_params.append(Cafe.location.contains(cafe_location))

    found_cafes = db.session.execute(db.select(Cafe).filter(or_(*search_params))).scalars().all()
    # create a dict of the found cafe
    found_cafes_dict = [cafe.as_dict() for cafe in found_cafes]
    # check if the found_cafes_dict is empty then return specific message if it is
    if len(found_cafes_dict) == 0:
        # sends an error response with a specific error code
        return jsonify(error={"Not Found": "Sorry, didn't find any cafes with that search."}), 400
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
        black_coffee_price= cafe_to_add["black_coffee_price"],
    )
    # add to database with add & commit
    db.session.add(new_cafe)
    db.session.commit()
    # return success response
    return jsonify(response={"success": "New cafe was added to the database."})

## HTTP PUT/PATCH - Update Record
# update the price of black coffee
# @app.route("/")

## HTTP DELETE - Delete Record


if __name__ == '__main__':
    app.run()
