import unittest
from app import create_app, db
from models import Movie, Actor
from flask_jwt_extended import create_access_token

class CastingAgencyTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['TESTING'] = True

        with self.app.app_context():
            db.create_all()
            self.insert_mocked_data()

        self.access_token = self.get_access_token()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def insert_mocked_data(self):
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

    def get_access_token(self):
        with self.app.app_context():
            # Create a JWT token for testing
            access_token = create_access_token(identity={'username': 'admin', 'roles': ['Casting Assistant', 'Casting Director', 'Executive Producer']})
            return access_token

    def test_get_movies(self):
        res = self.client.get('/movies', headers={'Authorization': f'Bearer {self.access_token}'})
        self.assertEqual(res.status_code, 200)

    def test_create_movie(self):
        res = self.client.post('/movies', json={'title': 'New Movie', 'release_date': '2024-12-01'}, headers={'Authorization': f'Bearer {self.access_token}'})
        self.assertEqual(res.status_code, 201)

    def test_update_movie(self):
        movie = Movie(title='Old Movie', release_date='2024-01-01')
        with self.app.app_context():
            db.session.add(movie)
            db.session.commit()
        res = self.client.patch(f'/movies/{movie.id}', json={'title': 'Updated Movie'}, headers={'Authorization': f'Bearer {self.access_token}'})
        self.assertEqual(res.status_code, 200)

    def test_delete_movie(self):
        movie = Movie(title='Delete Movie', release_date='2024-01-01')
        with self.app.app_context():
            db.session.add(movie)
            db.session.commit()
        res = self.client.delete(f'/movies/{movie.id}', headers={'Authorization': f'Bearer {self.access_token}'})
        self.assertEqual(res.status_code, 204)

    def test_get_actors(self):
        res = self.client.get('/actors', headers={'Authorization': f'Bearer {self.access_token}'})
        self.assertEqual(res.status_code, 200)

    def test_create_actor(self):
        res = self.client.post('/actors', json={'name': 'New Actor', 'age': 30, 'gender': 'Male'}, headers={'Authorization': f'Bearer {self.access_token}'})
        self.assertEqual(res.status_code, 201)

    def test_update_actor(self):
        actor = Actor(name='Old Actor', age=50, gender='Male')
        with self.app.app_context():
            db.session.add(actor)
            db.session.commit()
        res = self.client.patch(f'/actors/{actor.id}', json={'name': 'Updated Actor'}, headers={'Authorization': f'Bearer {self.access_token}'})
        self.assertEqual(res.status_code, 200)

    def test_delete_actor(self):
        actor = Actor(name='Delete Actor', age=40, gender='Female')
        with self.app.app_context():
            db.session.add(actor)
            db.session.commit()
        res = self.client.delete(f'/actors/{actor.id}', headers={'Authorization': f'Bearer {self.access_token}'})
        self.assertEqual(res.status_code, 204)

    def test_rbac(self):
        # Implement role-based access control tests here
        pass

if __name__ == "__main__":
    unittest.main()
