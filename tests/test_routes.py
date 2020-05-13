# project/test_basic.py


import unittest

from src.translator import app


class BasicTests(unittest.TestCase):

    ############################
    #   setup and teardown     #
    ############################

    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app.test_client()

        self.assertEqual(app.debug, False)

    # executed after each test
    def tearDown(self):
        pass

###############
#    tests    #
###############

    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_get_delete(self):
        response = self.app.delete('/translate/from/to/foo/',
                                   follow_redirects=True)
        response = self.app.get('/translate/from/to/foo/',
                                follow_redirects=True)
        self.assertEqual(response.status_code, 404)

    def test_add(self):
        response = self.app.post('/translate/from/to/foo/bar/',
                                 follow_redirects=True)
        self.assertEqual(response.data, b'{"status": "success"}')
        self.assertEqual(response.status_code, 200)
        response = self.app.get('/translate/from/to/foo/',
                                follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'{"translation": "bar"}')
        response = self.app.delete('/translate/from/to/foo/',
                                   follow_redirects=True)
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
