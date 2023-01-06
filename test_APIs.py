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

    """
    Assert that the response status code is correct and one of the location is available in the return
    """
    def test_get_all_locations(self):
        ## TODO
        pass
    
    """
    Assert that the response status code and message/result are correct
    Cases to be covered by the test:
        Case 1: sensor ID is an alphabet
        Case 2: Only location ID parameter is available
    """
    def test_get_sensors_in_locations(self):
        ## TODO
        pass
    
    """
    Assert that the response status code and message/result are correct
    Cases to be covered by the test:
        Case 1: No start and end dates - count should be 25
        Case 2: Invalid start date
        Case 3: End date only 
    """
    def test_get_logs_by_date(self):
        ## TODO
        pass
    
    """
    Assert that the response status code and message are correct for the add and delete sensor
    Add one sensor using the "addsensor" API then delete it using the "deletesensor" API
    """
    def test_add_delete_sensor(self):
        ## TODO
        pass
    
    """
    Assert that the response status code and message are correct for the add and delete sensor in location
    Add one sensor in a location using "addsensorinlocation" API then delete it using the "deletesensorinlocation"
    Cases to be covered:
        In insertion:
            Case 1: Invalid sensor/location IDs (alphabet)
            Case 2: Existing sensor and location IDs
        In deletion:
            Case 3: Existing sensor and location IDs
            Case 4: No sensor and location IDs as parameters
    """
    def test_add_delete_sensor_in_location(self):
        ## TODO
        pass
    
    """
    Assert that the response status code and message are correct for the add and delete logs
    Add one log entry using the "addlogentry" API then get its log id number using "getlogsbydate" API then delete it using "delete_log_entry_by_log_id" API
    Cases to be covered:
        In insertion:
            Case 1: Invalid date
            Case 2: Correct sensor location ID, date and value
        In getting log id:
            Case 4: Starting date before the date you used to insert the log entry
        In deletion:
            Case 5: Correct log id
    """
    def test_add_delete_logs(self):
        ## TODO
        pass
        
    def tearDown(self):
        #Delete any work done in the database
        pass
    