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
#aqui hacemos esto para en lugar de tener la clase completa tenga el objeto, en 
# lugar de retornar el response body ("hello,.."),  retorno todos y nuevos usuarios 
# de la base de datos, si cambian su correo por ejemplo al pedirla llegarán los datos
# actualizados     

#En resumen tenemos ruta user con metodo Get, cada ruta tiene su fx y gracias a SQL alchemy
#me traigo a todos los usuarios, como es un arreglo de clases y no puedo mostrarlas asi,vamos a 
# iterar por sobre cada uno de ellos aplicando metodo serialize, me mostrará info en formato
# diccionario (objeto) para poder leerlo de mejor forma y asi estando en un nuevo formato facil 
# de leer lo guardo en un nuevo arreglo y lo retornas. ESTA ES LA FORMA LARGA      

#FORMA CORTA, funcion map, retorna un arreglo y hacer algo en fx de ese arreglo, 
#quiero que resultado sea una lista en un map dentro de una fx lambda y voy a recibir un usuario
#y a ese usuario le pondre un serialize es decir por cada elemento del arreglo voy a serializar el
#valor y lo guardare en la misma variable. es como el for in pero en forma resumida. list es para que
#el resultado sea un arreglo.
    
    #all_users = list(map(lambda user: user.serialize() ,all_users))
   
    return jsonify(new_users),200
                #all_users si fuera la forma corta

#iterar por sobre el arreglo y por cada elemento del arreglo como era una clase llamar a su metodo serialize, 
#guardar la info en un arreglo para poder retornarlo, eso es con metodo map, return jsonify(all_users) porque
#es la variable donde guardé el arreglo.

#si quiero solo 1 usuario por su id
@app.route("/user/<int:id>", methods= ['GET'])
def one_user(id):
    one = User.query.get(id) 
    if(one is None):
        return "el user no existe"
    else:
        return jsonify(one.serialize())

#si quiero solo 1 usuario por su email
@app.route("/one/<correo>", methods= ['GET'])
def one_user_mail(correo):
    one = User.query.filter_by(email=correo).first()
    if(one is None):
        return "el user no existe"
    else:
        return jsonify(one.serialize())
#Post agregar nuevo user   
@app.route("/user", methods=['POST'])
def new_user():
   
    body = request.get_json()
    print(body)
    if( "email" not in body):
        return "falta email"
    if( "password" not in body):
        return "falta password"

    user = User.query.filter_by(email= body['email']).first()
    if(user):
        return "no puedo registrar  con este mail"

    nuevo = User()
    nuevo.email = body["email"]
    nuevo.password = body["password"]
    nuevo.is_active = True

    db.session.add(nuevo)
    db.session.commit()

    return {"msg":"user guardado"}

#[GET] /users/favorites Listar todos los favoritos que pertenecen al usuario actual. 
@app.route("/planet", methods=['POST'])
def new_planet():
   
    body = request.get_json()
    print(body)
    if( "name" not in body):
        return {"msg":"falta nombre del planeta"}

    planet = Planet.query.filter_by(name= body['name']).first()
    if(planet):
        return {"msg":"este planeta ya existe"}

    nuevo = Planet()
    nuevo.name = body["name"]
   

    db.session.add(nuevo)
    db.session.commit()

    return {"msg":"planeta guardado"}

@app.route("/people", methods=['POST'])
def new_people():
   
    body = request.get_json()
    print(body)
    if( "name" not in body):
        return {"msg":"falta nombre del personaje"}

    people = People.query.filter_by(name= body['name']).first()
    if(people):
        return {"msg":"este personaje ya existe"}

    nuevo = People()
    nuevo.name = body["name"]
   

    db.session.add(nuevo)
    db.session.commit()

    return {"msg":"personaje guardado"}

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
def one_people(id):
    onepeople = People.query.get(id) 
    if(onepeople is None):
        return "people no existe"
    else:
        return jsonify(onepeople.serialize())
    #return jsonify({
    #    "mensaje": "aca estara la info del personaje con id "+str(id)
    #})

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
def one_planet(id):
    oneplanet = Planet.query.get(id) 
    if(oneplanet is None):
        return "planet no existe"
    else:
        return jsonify(oneplanet.serialize())
    #return jsonify({
    #    "mensaje": "aca estara la info del planeta con id "+str(id)
    #})

# @app.route("/users/favorites/", methods=['GET'])
# def new_fa/users/favoritesv_planet(planet_id):
# [GET] /users/favorites
# [GET] 

@app.route("/favorite/planet/<int:user_id>/<int:planet_id>", methods=['POST'])
def new_fav_planet(user_id, planet_id):
    print (user_id, planet_id)
    # body = request.get_json()
    # # if "planet_name" not in body:
    # #     return jsonify({
    # #     "mensaje": "Se requiere el nombre del planeta."
    # # }), 400
    user= User.query.filter_by(id=user_id).first()
    if (user is None):
        return {"msg":"user invalido"}
    planet= Planet.query.filter_by(id=planet_id).first()
    if (planet is None):
        return {"msg":"planet invalido"}

    nuevo_planet = Fav_Planet(planet= planet, user= user)
    print(nuevo_planet)

    db.session.add(nuevo_planet)
    db.session.commit()

    return jsonify({
       "mensaje": "el planeta con id "+ str(planet_id) + " ha sido agregado"
    })

@app.route("/favorite/people/<int:people_id>", methods=['POST'])
def post_fav_people(people_id):
       
    user= User.query.filter_by(id=people_id).first()
    print(user)
    add_people = Fav_People.query.filter_by(rel_user=user).first()
    db.session.add(add_people)
    db.session.commit()
    
    return jsonify({
        "mensaje": "el personaje con id "+ str(people_id) + " ha sido agregado"
    })

    # nuevo_people = Fav_People(people_id)
    # nuevo.people_name = body["people_name"]

    
    # # nuevo_people.is_active = True

    # db.session.add(nuevo_people)
    # db.session.commit()

    # return "ok"
    #return jsonify({
    #    "mensaje": "el personaje con id "+ str(people_id) + " ha sido agregado"
    #})

@app.route("/favorite/people/<int:people_id>", methods=['DELETE'])
def delete_fav_people(people_id):
    user= User.query.filter_by(id=people_id).first()
    print(user)
    delete_people = Fav_People.query.filter_by(rel_user=user).first()
    db.session.delete(delete_people)
    db.session.commit()
    
    return jsonify({
        "mensaje": "el personaje con id "+ str(people_id) + " ha sido borrado"
    })

@app.route("/favorite/planet/<int:planet_id>", methods=['DELETE'])
def delete_fav_planet(planet_id):

##hago consulta en tabla planet para filtrar fila planet_id
    planet = Planet.query.filter_by(id=planet_id).first()

    # planet = Fav_Planet.query.filter_by(planet_id)
    # db.session.planet.delete(delete_fav_planet(planet_id))
    # db.session.commit()

    # planet = Planet.query.get(planet_id)
    # if planet:
    #     db.session.delete(planet)
    #     db.session.commit()
    #     return "Planeta eliminado", 204
    # else:
    #     return "Planeta no encontrado", 404


    delete_planet = Fav_Planet.query.filter_by(planet_id)
    db.session.delete(delete_planet)
    db.session.commit()
    
 
    fav_planet = Fav_Planet.query.get(planet_id)
    if(fav_planet):
        db.session.delete(fav_planet)
        db.session.commit()
        return "fav planet eliminado"
    else:
        return "fav planet no existe"

    return jsonify({
        "mensaje": "el planeta con id "+ str(planet_id) + " ha sido borrado"
    })
    
#delete user por id
@app.route("/user/<int:id>", methods=['DELETE'])
def delete(id):
    user = User.query.get(id)
    if(user):
        db.session.delete(user)
        db.session.commit()
        return {"msg":"user con el id "+ str(id) + " ha sido eliminado"}
    else:
        return "user no existe"

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
