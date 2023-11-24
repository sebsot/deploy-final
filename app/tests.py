import unittest
from app import app
from app import datos_participantes

class TestApp(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_index(self):
        response = self.app.get('/index')
        self.assertEqual(response.status_code, 200)

    def test_participantes(self):
        response = self.app.get('/participantes')
        self.assertEqual(response.status_code, 200)

    def test_noExiste(self):
        response = self.app.get('/no-existe')
        self.assertEqual(response.status_code, 404)

    def test_api(self):
        response = self.app.get('/participantes')
        self.assertEqual(response.status_code, 200)
        expected_data = datos_participantes()
        self.assertEqual(response.json['estudiantes'], expected_data)
     

if __name__ == '__main__':
    unittest.main()