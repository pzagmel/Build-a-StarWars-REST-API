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
from models import db, User, People, Fav_People, Planet, Fav_Planet
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

@app.route('/user', methods=['GET'])
def handle_hello():
#debo traer a todos los usuarios ya registrados..., creo una variable all_users, a la tabla User.query, es decir una consulta, donde me quiero
#traer todos.
    all_users = User.query.all()
#print(all_user[0].serialize())
#con el print puedo ver usuarios registrados en la consola, si quiero al 
#primer usuario print (all_user[0]) entonces ya tengo clase User que se 
#identifica con el email(funcion representation)
#ahora usaremos fx serialize, que me describe la informacion
#print(all_user[0].serialize()) me traera su id y correo.
#Nosotros tenemos una clase que define estructura de la base de datos
# me traje a todos los usuarios y los puedo pintar. ahora si queiro ver a todos
#los usuarios...sabemos que all_users es un arreglo y si agregara otro se suma
#a lista, como itero en un arreglo? con un for in range en fx de todos
#los usuarios que tenga (len(all_users)), voy a iterar cada unod e los elementos
#del arreglo, ahora puedo mostrar todos, print (arreglo en posicion[i])i porque
#tomara 0 hasta el total y eso.serialize para ejecutar fx que entrega sus valores.
#con estas lineas de codigo hago que me muestre todos los usuarios del arreglo.
#Ahora tenemos que guardar a estos usuarios, en un arreglo vacío new_users.
    
    new_users = []
    for i in range(len(all_users)):
        print(all_users[i].serialize())
        new_users.append(all_users[i].serialize())
#aqui hacemos esto para en lugar de tener la clase completam tenga el objeto, en 
# lugar de retornar el response body ("hello,.."),  retorno todos y nuevos usuarios 
# de la base de datos, si cambian su correo por ejemplo al pedirla llegarán los datos
# actualizados     

#En resumen tenemos ruta user con metodo Get, cada ruta tiene su fx y gracias a SQL alchemy
#me traigo a todos los usuarios, como es un arreglo de clases y no puedo mostrarlas asi,vamos a 
# irerar por sobre cada uno de ellos aplicando metodo serialize, me mostrará info en formato
# diccionario (objeto) para poder leerlo de mejor forma y asi estando en un nuevo formato facil 
# de leer lo guardo en un nuevo arreglo y lo retornas. ESTA ES LA FORMA LARGA      

#FORMA CORTA, funcion map, retorna un arreglo y hacer algo en fx de ese arreglo, 
#quiero que resultado sea una lista en un map dentro de una fx lambda y voy a recibir un usuario
#y a ese usuario le pondre un serialize es decir por cada elemento del arreglo voy a serializar el
#valor y lo guardare en la misma variable. es como el for in pero en forma resumida. list es para que
#el resultado sea un arreglo.
    
    #all_users = list(map(lambda user: user.serialize() ,all_users))
    response_body = {
        "msg": "Hello, this is your GET /user response"
    }
    return jsonify(new_users), 200
                #all_users si fuera la forma corta

@app.route("/people", methods=["GET"])
def get_all_people():

    all_people = People.query.all()
    new_people = []
    for i in range(len(all_people)):
        print(all_people[i].serialize())
        new_people.append(all_people[i].serialize())
    
    response_body = {
        "mensaje": "aca estaran todos los personajes"
    }
    return jsonify(new_people), 200
  

@app.route("/people/<int:id>", methods=["GET"])
def get_one_people(id):

    return jsonify({
        "mensaje": "aca estara la info del personaje con id "+str(id)
    })

@app.route("/planets", methods=["GET"])
def get_all_planets():

    all_planet = Planet.query.all()
    new_planet = []
    for i in range(len(all_planet)):
        print(all_planet[i].serialize())
        new_planet.append(all_planet[i].serialize())
    
    response_body = {
        "mensaje": "aca estaran todos los planetas"
    }
    return jsonify(new_planet), 200

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
