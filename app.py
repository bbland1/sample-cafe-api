from flask import Flask, jsonify, render_template, request
from flask_migrate import Migrate
from sqlalchemy.sql.expression import func

from models import Cafe, APIUsers, db
from api_key import check_api_key

app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

migrate = Migrate(app, db)

with app.app_context():
    db.create_all()

# @app.before_request
# def before_request():
#     check_api_key()


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
    return jsonify(cafes=cafe_dict)

# search for a record by location
@app.route("/api/v1/cafes/search")
def search_location():
    # get query parameters
    cafe_location = request.args.get("loc")
    cafe_name = request.args.get("name")
    # search the database

    # check that one of the query parameters are actually passed if not get out
    if not cafe_name and not cafe_location:
        return jsonify({"Error": "A query parameter wasn't passed."}), 400

    # set a found_cafe to empty list so the results from the proper search depending on the query is passed
    found_cafes = []

    # when the cafe location and name is passed the search will filter based on both 
    if cafe_name and cafe_location:
        found_cafes = db.session.execute(db.select(Cafe).filter(Cafe.location.contains(cafe_location)).filter(Cafe.name.contains(cafe_name))).scalars().all()

    # if just name is passed
    if cafe_name and not cafe_location:
        found_cafes = db.session.execute(db.select(Cafe).filter(Cafe.name.contains(cafe_name))).scalars().all()
    
    # if just location is passed
    if cafe_location and not cafe_name:
        found_cafes = db.session.execute(db.select(Cafe).filter(Cafe.location.contains(cafe_location))).scalars().all()

    # create a dict of the found cafe
    found_cafes_dict = [cafe.as_dict() for cafe in found_cafes]
    # check if the found_cafes_dict is empty then return specific message if it is
    if len(found_cafes_dict) == 0:
        # sends an error response with a specific error code
        return jsonify({"Error": "Sorry, didn't find any cafes with that search."}), 400
    # return the json
    return jsonify(cafes=found_cafes_dict)

## HTTP POST - Create Record

# generating a user with an api key
@app.route("/api/v1/cafes/users", methods=["POST"])
def add_api_user():
    if request.is_json:
        username = request.get_json()
    else:
        username = request.form

    if not username:
        return jsonify({'error': 'Username is required'}), 400
    
    new_user = APIUsers(username=username["username"])
    return jsonify({"username": new_user.username, "api_key": new_user.api_key})

# add a cafe to the database with api call
@app.route("/api/v1/cafes", methods=["POST"])
@check_api_key
def add_cafe():
    # get the request body info and create the new cafe using the model
    # check if the data is json or form encoded
    if request.is_json:
        cafe_to_add = request.get_json()
    else:
        cafe_to_add = request.form

    # validate the data sent to make sure the database required data is there
    required_fields = ["name", "map_url", "img_url", "location", "seats", "has_toilet", "has_wifi", "has_sockets", "can_take_calls"]
    if not all(field in cafe_to_add for field in required_fields):
        # sends an error response with a specific error code
        return jsonify({"Error": "Sorry you had an empty field."}), 404
    
    # set all the required fields of the form
    new_cafe = Cafe(
        name=cafe_to_add["name"],
        map_url=cafe_to_add["map_url"],
        img_url=cafe_to_add["img_url"],
        location=cafe_to_add["location"],
        seats=cafe_to_add["seats"],
        # these need to be booleans in the database so we wrap the calls in bool to convert
        has_toilet=bool(cafe_to_add["has_toilet"]),
        has_wifi=bool(cafe_to_add["has_wifi"]),
        has_sockets=bool(cafe_to_add["has_sockets"]),
        can_take_calls=bool(cafe_to_add["can_take_calls"]),
        black_coffee_price=cafe_to_add["black_coffee_price"],
    )
    # add to database with add & commit
    db.session.add(new_cafe)
    db.session.commit()
    # return success response
    return jsonify({"Success": "New cafe was added to the database."})

## HTTP PUT/PATCH - Update Record

# update a record  based on id search
@app.route("/api/v1/cafes/<int:cafe_id>", methods=["PATCH"])
@check_api_key
def update_cafe(cafe_id):
    #search the database using the passed in 
    cafe_info = db.session.execute(db.select(Cafe).filter_by(id=cafe_id)).scalar_one()

    # check that a cafe was found and if not return error
    if not cafe_info:
        return jsonify({"Error": "No product was found with that id."}), 404
    
    # check if the data is json or form encoded
    if request.is_json:
        update_info = request.get_json()
    else:
        update_info = request.form

    # check to make sure some type of update parameter was passed
    if not update_info:
        return jsonify({"Error": "Nothing was passed to update."}), 404
    
    # check which of the parameters were passed and update the ones that are truthy
    if "name" in update_info:
        cafe_info.name = update_info["name"]

    # ? it maybe good for the url to look into checking that the updated url is a url and maybe in the adding too???
    if "map_url" in update_info:
        cafe_info.map_url = update_info["map_url"]

    if "img_url" in update_info:
        cafe_info.img_url = update_info["img_url"]

    if "location" in update_info:
        cafe_info.location = update_info["location"]

    if "seats" in update_info:
        cafe_info.seats = update_info["seats"]

    if "has_toilet" in update_info:
        cafe_info.has_toilet = bool(update_info["has_toilet"])

    if "has_wifi" in update_info:
        cafe_info.has_wifi = bool(update_info["has_wifi"])

    if "has_sockets" in update_info:
        cafe_info.has_sockets = bool(update_info["has_sockets"])

    if "can_take_calls" in update_info:
        cafe_info.can_take_calls = bool(update_info["can_take_calls"])
        
    if "black_coffee_price" in update_info:
        cafe_info.black_coffee_price = update_info["black_coffee_price"]

    # commit the changes
    db.session.commit()

    # return a success
    return jsonify({"Success": f"{cafe_info.name} was updated."})

## HTTP DELETE - Delete Record
@app.route("/api/v1/cafes/<int:cafe_id>", methods=["DELETE"])
@check_api_key
def delete_cafe(cafe_id):
    # find the record by the id
    cafe_to_delete = db.session.execute(db.select(Cafe).filter_by(id=cafe_id)).scalar_one()

    # check that a cafe was found and if not return error
    if not cafe_to_delete:
        return jsonify({"Error": "No product was found with that id."}), 404

    # delete and save the delete
    db.session.delete(cafe_to_delete)
    db.session.commit()
    # return a success
    return jsonify({"Success": f"{cafe_to_delete.name} was deleted."})


if __name__ == '__main__':
    app.run()
