from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self): 
        return ' %r' % self.id
    #esta funcion representation es para que al traer info de base de datos pueda
    #identificarlo de alguna manera, en este caso con el email
    #el usuario xxx@gmail.com (fx solo se verá si haces print) para identificar o reconocer.BaseException()  
    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    #esta funcion serialize sirve para cuando traigas por ejemplo todos los
    # usuarios de la base de datos me entregue la info que yo quiero, en este
    # caso el id y el email, uno no pide la pasword, para que cuando alguien 
    # llame a la clase usuario te retorne info valiosa, no la clave
    #
class People(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self): 
        return '%r' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
        }
class Fav_People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rel_people = db.Column(db.Integer, db.ForeignKey("people.id"))
    rel_user_id = db.Column(db.Integer, db.ForeignKey("user.id"))   
    people = db.relationship("People", foreign_keys=[rel_people])
    user = db.relationship("User", foreign_keys=[rel_user_id])  
#definimos id de la tabla, nombre del personaje, qué usuario lo agregó a fav
#esta info se alimenta de las otras tablas, db.ForeignKey y quien es su foreignkey
#la tabla people en el campo name ("people.name") y el user_fav el FK es la tabla
#User en el campo email con eso tendremos el nombre del personaje, el nombre de 
# quien agregó a fav, el usuario que agregó a favorito y finalmente definimos
# vinculacion entre tablas. Un usuario tiene muchos Fav_People (1amuchos) y un People
# puede estar en muchos fav(1amuchos)
#ahora queremos que esta info se vea en el admin, en la base de datos, en User
#necesitamos hacer comandos especiales, abrimos nueva terminal:
#pipenv run migrate------->efectuar cambios base de datos
#pipenv run upgrade------->para que estos cambios se hagan efectivos
#si les dice done, quiere decir que salió todo bien. 
#Admin me permite agregar campos en la base de datos de forma visual, que debo hacer?
#agregar importar para que Admin pueda pintar apare del User, Fav_People, People,
#
class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self): 
         return '%r' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
    }
class Fav_Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rel_planet = db.Column(db.Integer, db.ForeignKey("planet.id"))
    rel_user_id = db.Column(db.Integer, db.ForeignKey("user.id"))   
    planet = db.relationship("Planet", foreign_keys=[rel_planet])
    user = db.relationship("User", foreign_keys=[rel_user_id]) 
    

  
