from flask import jsonify, request
from models import APIUsers, db

# set the api methods that need to check for api
API_METHODS = ["POST", "PATCH", "DELETE"]

# pick the routes that need to check because not all get paths may be check free
API_ROUTES = {
    "/api/v1/cafes": API_METHODS,
}

# have function to check api
def check_api_key():
    request_path = request.path
    request_method = request.method

    # skip the non-api routes
    if request_method not in API_METHODS and request_path not in API_ROUTES:
        return 
    
    # get the api key, using custom header here for now, it seems bit simpler and this is a simpler api but still allows for more security
    request_api_key = request.headers.get("X-API-Key")

    # check if the api key is there
    if not request_api_key:
        return jsonify({"Error": "API key is missing."}), 401
    
    # check if the api key is correct
    user = db.session.execute(db.select(APIUsers).filter_by(api_key=request_api_key)).scalar_one()
    if not user:
        return jsonify({"Error": "Invalid API Key"}), 401
    
    # check if the route needs api
    if request_path in API_ROUTES and request_method in API_ROUTES[request_path]:
        return
    
    # deny access if API key is required but not present for current route
    return jsonify({"error": "API key required for this request."}), 401


