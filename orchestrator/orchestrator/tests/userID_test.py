import unittest
import json
from orchestrator.main import app

class TestUserEndpoints(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_generate_user_id(self):
        # Test the POST method for generating a user ID
        response = self.app.post('/generateUserId', headers={'Content-Type': 'application/json'}, data=json.dumps({'name': 'John Doe'}))
        data = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)
        self.assertIn('user_id', data)

    def test_get_user_details(self):
        # Test the GET method for retrieving user details
        response = self.app.get('/getUserDetails/John%20Doe')

        # Assuming that the user already exists from the previous test
        data = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)
        self.assertIn('user_id', data)
        self.assertIn('user_name', data)

    def test_get_user_details_not_found(self):
        # Test the case when the user is not found
        response = self.app.get('/getUserDetails/NonExistentUser')

        data = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'User not found')

if __name__ == '__main__':
    unittest.main()
