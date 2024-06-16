from app import create_app
from models import db, Movie, Actor

app = create_app()

with app.app_context():
    # Insert mocked data into the movies table
    movies = [
        Movie(title='The Shawshank Redemption', release_date='1994-09-23'),
        Movie(title='The Godfather', release_date='1972-03-24'),
        Movie(title='The Dark Knight', release_date='2008-07-18'),
        Movie(title='Pulp Fiction', release_date='1994-10-14'),
        Movie(title='Forrest Gump', release_date='1994-07-06'),
        Movie(title='Inception', release_date='2010-07-16'),
        Movie(title='Fight Club', release_date='1999-10-15'),
        Movie(title='The Matrix', release_date='1999-03-31'),
        Movie(title='The Lord of the Rings: The Return of the King', release_date='2003-12-17'),
        Movie(title='The Silence of the Lambs', release_date='1991-02-14')
    ]
    db.session.bulk_save_objects(movies)
    db.session.commit()

    # Insert mocked data into the actors table
    actors = [
        Actor(name='Morgan Freeman', age=83, gender='Male'),
        Actor(name='Marlon Brando', age=80, gender='Male'),
        Actor(name='Christian Bale', age=47, gender='Male'),
        Actor(name='Uma Thurman', age=51, gender='Female'),
        Actor(name='Tom Hanks', age=65, gender='Male'),
        Actor(name='Leonardo DiCaprio', age=47, gender='Male'),
        Actor(name='Brad Pitt', age=58, gender='Male'),
        Actor(name='Keanu Reeves', age=57, gender='Male'),
        Actor(name='Elijah Wood', age=40, gender='Male'),
        Actor(name='Jodie Foster', age=59, gender='Female')
    ]
    db.session.bulk_save_objects(actors)
    db.session.commit()
