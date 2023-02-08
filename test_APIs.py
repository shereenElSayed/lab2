import unittest
import json

from app import app


class APIsTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = app.test_client()

    def test_get_all_sensors(self):
        # given

        params = {"type": "all"}

        response = self.app.get('/api/getsensors/', query_string=params)
        json_response = response.json

        # Make sure the response status is 200
        self.assertEqual(response.status_code, 200)

        # Check the content of the response
        self.assertIn({'id': 1, 'sensor name': 'LMT84LP', 'type': 'temperature'}, json_response["RESULT"])

    def test_get_all_locations(self):
        """
        Assert that the response status code is correct and one of the location is available in the return
        """
        # TODO
        raise NotImplementedError("Implement the code and delete this line when you are done")

    def test_get_sensors_in_locations(self):
        """
        Assert that the response status code and message/result are correct
        Cases to be covered by the test:
            Case 1: sensor ID is an alphabet
            Case 2: Only location ID parameter is available
        """
        # TODO
        raise NotImplementedError("Implement the code and delete this line when you are done")

    def test_get_logs_by_date(self):
        """
        Assert that the response status code and message/result are correct
        Cases to be covered by the test:
            Case 1: No start and end dates - count should be 20
            Case 2: Invalid start date
            Case 3: End date only
        """
        # TODO
        raise NotImplementedError("Implement the code and delete this line when you are done")

    def test_add_delete_sensor(self):
        """
        Assert that the response status code and message are correct for the add and delete sensor
        Add one sensor using the "addsensor" API then delete it using the "deletesensor" API
        """
        # TODO
        raise NotImplementedError("Implement the code and delete this line when you are done")

    def test_add_delete_sensor_in_location(self):
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
        # TODO
        raise NotImplementedError("Implement the code and delete this line when you are done")

    def test_add_delete_logs(self):
        """
        Assert that the response status code and message are correct for the add and delete logs
        Add one log entry using the "addlogentry" API then get its log id number using
                "getlogsbydate" API then delete it using "delete_log_entry_by_log_id" API
        Cases to be covered:
            In insertion:
                Case 1: Invalid date
                Case 2: Correct sensor location ID, date and value
            In getting log id:
                Case 4: Starting date before the date you used to insert the log entry
            In deletion:
                Case 5: Correct log id
        """
        # TODO
        raise NotImplementedError("Implement the code and delete this line when you are done")

    @classmethod
    def tearDown(cls):
        pass
        # Delete any work done in the database
