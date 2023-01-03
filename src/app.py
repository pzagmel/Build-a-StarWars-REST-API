"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/users', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route("/users/favorites", methods=["GET"])
def get_fav_user():

    response_body = {
        "msg": "Get all the favorites that belong to the current user."
    }

    return jsonify(response_body), 200

@app.route("/people", methods=["GET"])
def get_all_people():

    return jsonify({
        "mensaje": "aca estaran todos los personajes"
    })

@app.route("/people/<int:id>", methods=["GET"])
def get_one_people(id):

    return jsonify({
        "mensaje": "aca estara la info del personaje con id "+str(id)
    })

@app.route("/planets", methods=["GET"])
def get_all_planets():

    return jsonify({
        "mensaje": "aca estaran todos los planetas"
    })

@app.route("/planets/<int:id>", methods=["GET"])
def get_one_planet(id):

    return jsonify({
        "mensaje": "aca estara la info del planeta con id "+str(id)
    })

@app.route("/favorite/planet/<int:planet_id>", methods=['POST'])
def post_fav_planet(planet_id):
    
    return jsonify({
        "mensaje": "el planeta con id "+ str(planet_id) + " ha sido agregado"
    })

@app.route("/favorite/people/<int:people_id>", methods=['POST'])
def post_fav_people(people_id):
    
    return jsonify({
        "mensaje": "el pesconaje con id "+ str(people_id) + " ha sido agregado"
    })

@app.route("/favorite/people/<int:people_id>", methods=['DELETE'])
def delete_fav_people(people_id):
    
    return jsonify({
        "mensaje": "el personaje con id "+ str(people_id) + " ha sido borrado"
    })

@app.route("/favorite/people/<int:planet_id>", methods=['DELETE'])
def delete_fav_planet(planet_id):
    
    return jsonify({
        "mensaje": "el planeta con id "+ str(planet_id) + " ha sido borrado"
    })


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
