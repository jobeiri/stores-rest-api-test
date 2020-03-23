from models.user import UserModel
from tests.integration.integration_base_test import IntegrationBaseTest
import json


class UserTest(IntegrationBaseTest):
    def test_register_user(self):
        with self.app() as client:
            with self.app_context():
                response = client.post("/register", data={"username": "test", "password": "1234"})

                self.assertEqual(response.status_code, 201)
                self.assertIsNotNone(UserModel.find_by_username("test"))
                self.assertDictEqual({"message": "User created successfully."},
                                     json.loads(response.data))

    def test_register_and_login(self):
        with self.app() as client:
            with self.app_context():
                client.post("/register",
                            data={"username": "test", "password": "1234"})
                auth_response = client.post("/auth",
                                            data=json.dumps({"username": "test", "password": "1234"}),
                                            headers={"Content-Type": "application/json"})

                self.assertIn("access_token", json.loads(auth_response.data).keys())

    def test_register_duplicate_user(self):
        with self.app() as client:
            with self.app_context():
                client.post("/register",
                            data={"username": "test", "password": "1234"})
                response = client.post("/register",
                                       data={"username": "test", "password": "1234"})

                self.assertEqual(response.status_code, 400)
                self.assertDictEqual({"message": "A user with that username already exists."},
                                     json.loads(response.data))
