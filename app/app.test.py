from app import app, User, db
import unittest
import json
import os

class FlaskTestCase(unittest.TestCase):
	def setUp(self):
		app.config['TESTING'] = True
		app.config['WTF_CSRF_ENABLED'] = False
		app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
		self.app = app.test_client()
		db.create_all()

	def tearDown(self):
		db.session.remove()
		db.drop_all()

	def test_database(self):
		test = os.path.exists('site.db')
		self.assertTrue(test)

	def test_user(self):
		u = User(username='admin', email='admin@example.com')
		db.session.add(u)
		db.session.commit()
		user = User.query.filter_by(username='admin').first()
		email = User.query.filter_by(email='admin@example.com').first()
		assert user.username == 'admin'
		assert user.email == 'admin@example.com'

	def test_index(self):
		test = app.test_client(self)
		response = test.get('/', content_type='html/text')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.data, b'Hello, World!')

	def test_api(self):
		response = self.app.get('/api')
		data = json.loads(response.get_data(as_text=True))
		self.assertEqual(data['username'], 'admin')
		self.assertEqual(data['email'], 'admin@example.com')

	def test_404(self):
		response = self.app.get('/forum')
		self.assertEqual(response.status, '404 NOT FOUND')

	def login(self, username, password):
	    return self.app.post('/login', data=dict(
	        username=username,
	        password=password
	    ), follow_redirects=True)

	def test_login(self):
		response = self.login(app.config['USERNAME'], app.config['PASSWORD'])
		self.assertIn(b'Hello, World!', response.data)

if __name__ == '__main__':
    unittest.main()