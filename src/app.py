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
from models import db, User, People, Planets, Favoritos
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
    all_users = User.query.all()
    usuarios = list( map ( lambda user: user.serialize(), all_users))

    response_body = {
        "todos los users" : usuarios
    }

    return jsonify(response_body), 200


@app.route('/user/favorites', methods= ['GET'])
def get_user_favorites():

    all_favorites = Favoritos.query.all()
    favs = list( map ( lambda fav: fav.serialize(), all_favorites))

    response_body = {
        "todos los favoritos" : favs
    }

    return jsonify(response_body), 200


@app.route('/people', methods= ['GET'])
def get_people():
    # all_people = User.query.all()
    # print(all_people[0].__repr__())
    all_people = People.query.all()
    people = list( map( lambda people: people.serialize(), all_people))

    return jsonify({
        "mensaje": "todos los personajes",
        "people": people
    })

@app.route('/planets', methods= ['GET'])
def get_planets():
    all_planets = Planets.query.all()
    planets = list( map( lambda planets: planets.serialize(), all_planets))

    return jsonify({
        "mensaje": "todos los planetas",
        "planets": planets
    })


@app.route('/people/<int:people_id>', methods= ['GET'])
def get_one_people(people_id):
    personaje = People.query.get(people_id)

    return jsonify({
        "people by id": personaje
    })

@app.route('/planets/<int:planet_id>', methods= ['GET'])
def get_one_planet(planet_id):
    planet = Planets.query.get(planet_id)
    return jsonify({
        "planet by id": planet
    })


@app.route('/favorite/planet/<int:planet_id>', methods= ['POST'])
def add_new_planet_to_current_user_favs(planet_id):
    body = request.body(jsonify) #traer los datos del usuario. user_email
    print(body)
    new_favorite = Favoritos( user_email= body['email'], planet=planet_id) 
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify({"aqui nuevo favorito": new_favorite})

@app.route('/favorite/people/<int:planet_id>', methods= ['POST'])
def add_new_people_to_current_user_favs():
    return jsonify({
        "aqui ira la funcion POST para ": "Add a new favorite people to the current user with the planet id = planet_id."
    })

@app.route('/favorite/planet/<int:planet_id>', methods= ['DELETE'])
def delete_favorite_planet(planet_id):

    planet = Planets.query.get(planet_id)
    db.session.delete(planet)
    db.session.commit()

    return jsonify({
        "planeta borrado ": planet
    })

@app.route('/favorite/planet/<int:planet_id>', methods= ['DELETE'])
def delete_favorite_people(planet_id):
    del favorite.planet[planet_id]
    return jsonify({
        "aqui ira la funcion DELETE para ": "Delete favorite planet with the id = planet_id."
    })





# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
