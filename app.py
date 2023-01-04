import os
from DBobj import DBobj
from flask import Flask, request, jsonify, make_response
import dotenv


app = Flask(__name__)
DEBUG = app.debug

### CORS section
@app.after_request
def after_request_func(response):
    if DEBUG:
        print("in after_request")
    origin = request.headers.get('Origin')
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Headers', 'x-csrf-token')
        response.headers.add('Access-Control-Allow-Methods',
                            'GET, POST, OPTIONS, PUT, PATCH, DELETE')
        if origin:
            response.headers.add('Access-Control-Allow-Origin', origin)
    else:
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        if origin:
            response.headers.add('Access-Control-Allow-Origin', origin)

    return response
### end CORS section


#initialize db object
db_obj = None
with app.app_context():
    dotenv.load_dotenv()
    user = os.environ.get("PGUSER")
    pwd = os.environ.get("PGPASSWORD")
    db_obj = DBobj("sensors_data", user, pwd)

@app.route('/')
def hello():
    return 'Welcome to CS190B Sensors Hub'

#####################################################
### Get data from server
#####################################################
''' Get sensors in our database
--Parameters:
----type (string)--> allowed values: temperature/air_quality/humidity/gas/all 
--Returns:
----List of sensors according to the type in JSON in "RESULT" key or the error msg in "MESSAGE"
--Exception: return json with key "Message" and value f"Exception {e}" where e is the exception error. Code 500

'''
@app.route('/api/getsensors/', methods=['GET'])
def get_sensors():
    # Retrieve the msg from url parameter of GET request 
    # and return MESSAGE response (or error or success)
    try:
        type = request.args.get("type", None)

        if DEBUG:
            print("GET respond() msg: {}".format(type))

        response = {}
        if not type: #invalid/missing message
            response["MESSAGE"] = "no sesnor type is found, please send a type (temperature/air_quality/humidity/gas/all)."
            status = 400
        else: #valid message
            if type == "all":
                result = db_obj.execute_sql("SELECT * FROM SENSORS")
            else:
                result = db_obj.execute_sql(f"SELECT * FROM SENSORS WHERE type='{type}'")
            if result[0]:
                
                execution_result = result[1].fetchall() # method that fetches all the remaining tuples from the last executed statement from a table (returns a list of tuples)
                response["RESULT"] = []
                for row in execution_result:
                    response["RESULT"].append({"sensor name": row[1], "type": row[2]})
                status = 200
            else:
                response['MESSAGE'] = f"Error executing sql {result[1]}"
                status = 400
    except Exception as e:
        print(e)
        print(result)
        print(execution_result)
        response["MESSAGE"] = f"Exception {e}"
        status = 500
    # Return the response in json format with status code
    return jsonify(response), status

'''
get locations should return a json format with all the locations and their IDs
Return:
- If there is an error in retrieving the locations, return json with MESSAGE key and value "Error retrieving locations" - code 400
- If an exception occured in the whole function, return json with MESSAGE key and value f"Exception {e}" where e is the exception message - code 500
- If succeeded, return json with RESULT and a list of the returned data - code 200
- Example of the return:
---- Exception: {"MESSAGE":"Exception tuple index out of range","RESULT":[]}
---- Success: {"RESULT":[{"location":"Main Gate","location_id":1},{"location":"Left Lower Corner","location_id":2},{"location":"Right Lower Corner","location_id":3},{"location":"Left Upper Corner","location_id":4},{"location":"Right Upper Corner","location_id":5},{"location":"Middle","location_id":6}]}
Please note location and location_id order is not relevent as these elements are accessed by KEY and not index (check dictionaries in python for more clarification)
'''
@app.route('/api/getlocations/', methods=['GET'])
def get_locations():
    ## TODO
    pass

'''
get sensors in location api takes sensor id or location id and returns a list
Parameters: 
-sensor_id (int)--> sensor id (optional)
-location_id (int) --> location id(optional)
Returns:
- If none of the sensor or location id were specified, returned all from the sensors
- If sensor id is specified and no location: return the rows where the sensor id is available
- If location id is specified and no sensor id: return the rows where the location is available
- If both are specified, return the row where they are both avaiable 
--Exception: return json with key "Message" and value f"Exception {e}" where e is the exception error. Code 500
- The return format is always JSON:
--- in case of successful data retrieval, RESULT key with value a list of the retrieved data - code 200
Example for api/getsensorsinlocations?location_id=2:
{
    "RESULT": [
        {"location_id": 2, "sensor_id": 1,"sensor_location_id": 2},
        {"location_id": 2, "sensor_id": 5, "sensor_location_id": 4}
    ]
}
--- in case of failure in retrieving data, MESSAGE key with value "Error: failed to retrieve data"
'''
@app.route('/api/getsensorsinlocations', methods=['GET'])
def get_sensors_in_locations():
    ## TODO
    pass


'''
get logs by date takes a start and/or end dates and returns the logs in this period
Parameters:
- start (string) --> date only (no time) in this format mm-dd-YYYY (optional)
- end (string) --> date only (no time) in this format mm-dd-YYYY (optional)
Return:
- If start is specified and no end, return all logs from this date till the most recent entry
- If end is specified and no start, return all logs from the beginning till the end date
- If both, then return logs in this period
- If none, return the last 20 log entries
- Exception: return json with key "Message" and value f"Exception {e}" where e is the exception error. Code 500

Example return for /api/getlogsbydate?end=12-14-2022&start=12-10-2022:
{
    "RESULT": [
        { "log_id": 9,"sensor_location_id": 3,"timestamp": "Tue, 13 Dec 2022 00:08:24 GMT","value": "30"},
        { "log_id": 10,"sensor_location_id": 4,"timestamp": "Mon, 12 Dec 2022 00:08:24 GMT","value": "40"},
        { "log_id": 11,"sensor_location_id": 5,"timestamp": "Sun, 11 Dec 2022 00:08:24 GMT","value": "50"},
        { "log_id": 12,"sensor_location_id": 6,"timestamp": "Sat, 10 Dec 2022 00:08:24 GMT","value": "60"}
    ]
}

'''
@app.route('/api/getlogsbydate', methods=["GET"])
def get_logs_by_date():
    ## TODO
    pass

#####################################################
### add data to server
#####################################################

'''
add sensors should have arguments name and type.
NOTE: Make sure the http method used is correct
Parameters:
sensor_name (string) --> the name of the sensor
sensor_type (string) --> the type of the sensor
Return: 
--If no sensor available in the table with same name and type, return in JSON MESSAGE key with value "Sensor added successfully" - code 201
--If an argument is missing, return in JSON MESSAGE key with value "Argument is missing, please pass name and type for the sesnor as argument" - code 400
--If sensor exists, return in JSON MESSAGE key with value "Failed: Sensor exists in the database"- code 400
--If failed to check if sensor exists: return in JSON MESSAGE key with value ""Failed to check if sensor exists" - code 400
--If failed to add sensor, return in JSON MESSAGE key with value f"Failed to add sensor {error}" (error from the execution of the command) - code 400
--Exception: return json with key "Message" and value f"Exception {e}" where e is the exception error. Code 500

'''
@app.route('/api/addsensors/', methods=['PUT'])
def add_sensors():
    ## TODO
    pass

'''
add sensor in location should allow you to specify a sensor and location ids
NOTE: Make sure the http method used is correct
Parameters:
--sensor_id (int) --> Sensor ID (mandatory)
--location_id (int) --> Location ID (mandatory)
Returns:
-- If sensor and location row already exists: retrun in JSON format MESSAGE key with value: "Failed: Sensor in this location exists in the database"- code 400
-- else, return
-- Exception: return json with key "Message" and value f"Exception {e}" where e is the exception error. Code 500
 
'''
@app.route('/api/addsensorinlocation/', methods=['PUT'])
def add_sensor_in_location():
    ## TODO
    pass


'''
add log entry
NOTE: Make sure the http method used is correct
Parameters:
s_l_id (int) --> sensor location id
value (int) --> value of the sensor reading
timestamp (string) --> date and time of the reading (mm-dd-yyyyThh:mm:ss) i.e 12-22-2022T10:15:20
Return:
-- If a parameter is missing, return json with key "Message" and value 
    "Parameter is missing, expecting sensor location id (s_l_id) and value" - code 400
-- If all parameters are available, insertion is successful: return json with key "Message" and value
    "Log entry added successfully" and code 200. If failed then the message value is "Failed to add log entry {error}" 
    and error is any error returned from the transaction. code 400
-- Exception: return json with key "Message" and value f"Exception {e}" where e is the exception error. Code 500
'''
@app.route('/api/addlogentry/', methods=['PUT'])
def add_log_entry():
    ## TODO
    pass

#####################################################
### Delete data from server - TO BE USED IN THE TESTING
#####################################################
'''
delete a sensor by name 
Parameters:
sensor --> name of the sensor to be deleted (Mandatory)
Returns:
-- if sensor name is missing, return JSON with key "Message" and value "Parameter sensor is missing" - code 400
-- else, return JSON with key "Message" and value "Sensor deleted successfully" - code 200
or "Failed to delete sensor {error}" where error is any error message from the execution. - code 400
-- Exception: return json with key "Message" and value f"Exception {e}" where e is the exception error. Code 500
'''
@app.route('/api/deletesensor/', methods=['DELETE'])
def delete_sensor():
    ## TODO
    pass


'''
Delete sensor in location
Parameters:
-- s_id --> The id of the sensor
-- l_id --> The id of the location 
Return:
-- If sensor id or location id is missing, return JSON with key "Message" and value "Parameters sensor id (s_id) and/or location id (l_id) are missing" - code 400
-- else if successful, return JSON with key "Message" and value "Sensor in location is deleted successfully" - code 200
or "Failed to delete sensor in location {error}" where error is any error message from the execution. - code 400
-- Exception: return json with key "Message" and value f"Exception {e}" where e is the exception error. Code 500
'''
@app.route('/api/deletesensor/', methods=['DELETE'])
def delete_sensor_in_location():
    ## TODO
    pass

'''
Delete a log entry
Parameters:
-- s_l_id (int) --> Sensor location ID (Mandatory)
-- timestamp (string) --> date and time of the reading (mm-dd-yyyyThh:mm:ss) i.e 12-22-2022T10:15:20 (Mandatory)
Return:
-- If any of the parameters is missing, return JSON with key "Message" and value "Parameters sensor location id (s_l_id) and/or timestamp id (timestamp) are missing" - code 400
-- else if successful, return JSON with key "Message" and value "Log entry is deleted successfully" - code 200
or "Failed to delete log entry {error}" where error is any error message from the execution. - code 400
-- Exception: return json with key "Message" and value f"Exception {e}" where e is the exception error. Code 500
'''
@app.route('/api/deletesensor/', methods=['DELETE'])
def delete_log_entry():
    ## TODO
    pass
#####################################################
### Update data from server
#####################################################
"""
WORK IN PROGRESS
Move sensor from location to another
Parameters:
--sensor_id : sensor to be moved id
--current_location: the current location of the sensor
--new_location: the new location to be used for the sensor
Returns:

"""
@app.route('/api/movesensorinlocation', methods=['PUT'])
def move_sensor_in_location():
    ## TODO 
    pass

def main():
    '''The threaded option for concurrent accesses, 0.0.0.0 host says listen to all network interfaces 
    (leaving this off changes this to local (same host) only access, port is the port listened on
    -- this must be open in your firewall or mapped out if within a Docker container. 
    '''
    
    app.run(threaded=True)

if __name__ == '__main__':
    main()