import unittest
import json

from app import app


class APIsTest(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        
    def test_get_all_sensors(self):
        #given
        
        params = {"type" : "all" }
        
        response = self.app.get('/api/getsensors/', query_string=params)
        json_response = response.json
        
        #Make sure the respose status is 200
        self.assertEqual(response.status_code, 200)
        
        #Check the content of the response
        self.assertIn({"sensor name" : "LMT84LP", "type": "temperature"}, json_response["RESULT"])

    def tearDown(self):
        #Delete any work done in the database
        pass