from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from models import db, Movie, Actor
from auth import requires_role

routes = Blueprint('routes', __name__)

# Login endpoint to generate JWT token
@routes.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    # Normally, you would verify the username and password from the database
    # Here we assume the credentials are valid for demonstration purposes
    if username == 'admin' and password == 'password':
        access_token = create_access_token(identity={'username': username, 'roles': ['Casting Assistant', 'Casting Director', 'Executive Producer']})
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"msg": "Bad username or password"}), 401

# GET requests
@routes.route('/movies', methods=['GET'])
@requires_role('Casting Assistant')
def get_movies():
    movies = Movie.query.all()
    return jsonify([movie.format() for movie in movies])

@routes.route('/actors', methods=['GET'])
@requires_role('Casting Assistant')
def get_actors():
    actors = Actor.query.all()
    return jsonify([actor.format() for actor in actors])

# POST requests
@routes.route('/movies', methods=['POST'])
@requires_role('Casting Director')
def create_movie():
    data = request.get_json()
    new_movie = Movie(title=data['title'], release_date=data['release_date'])
    db.session.add(new_movie)
    db.session.commit()
    return jsonify(new_movie.format()), 201

@routes.route('/actors', methods=['POST'])
@requires_role('Casting Director')
def create_actor():
    data = request.get_json()
    new_actor = Actor(name=data['name'], age=data['age'], gender=data['gender'])
    db.session.add(new_actor)
    db.session.commit()
    return jsonify(new_actor.format()), 201

# PATCH requests
@routes.route('/movies/<int:id>', methods=['PATCH'])
@requires_role('Casting Director')
def update_movie(id):
    data = request.get_json()
    movie = Movie.query.get(id)
    if 'title' in data:
        movie.title = data['title']
    if 'release_date' in data:
        movie.release_date = data['release_date']
    db.session.commit()
    return jsonify(movie.format())

@routes.route('/actors/<int:id>', methods=['PATCH'])
@requires_role('Casting Director')
def update_actor(id):
    data = request.get_json()
    actor = Actor.query.get(id)
    if 'name' in data:
        actor.name = data['name']
    if 'age' in data:
        actor.age = data['age']
    if 'gender' in data:
        actor.gender = data['gender']
    db.session.commit()
    return jsonify(actor.format())

# DELETE requests
@routes.route('/movies/<int:id>', methods=['DELETE'])
@requires_role('Executive Producer')
def delete_movie(id):
    movie = Movie.query.get(id)
    db.session.delete(movie)
    db.session.commit()
    return '', 204

@routes.route('/actors/<int:id>', methods=['DELETE'])
@requires_role('Casting Director')
def delete_actor(id):
    actor = Actor.query.get(id)
    db.session.delete(actor)
    db.session.commit()
    return '', 204
