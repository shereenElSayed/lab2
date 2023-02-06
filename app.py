import os
from DBobj import DBobj
from flask import Flask, request, jsonify, make_response
import dotenv

app = Flask(__name__)
DEBUG = app.debug


#####################################################
# CORS section
#####################################################
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


#####################################################
# end CORS section
#####################################################

# initialize db object
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
# Get data from server
#####################################################
@app.route('/api/getsensors/', methods=['GET'])
def get_sensors():
    """ Get sensors in our database
    Parameters:
    -- type (string)--> allowed values: temperature/air_quality/humidity/gas/all 
    Returns:
    -- If no type parameter, return JSON with "MESSAGE" key and value "Failed: type parameter is missing" - code 400
    -- If successful, return JSON with 
     ----"MESSAGE" key and value "Succeeded: data retrieved successfully"
     ----"RESULT" key and the value is a list of the sensors in JSON objects. Each object has "id",
     "sensor name" and "type" keys and values from the db
    -- If failed, return JSON with "MESSAGE" key and value f"Error retrieving sensors {error}"
    (error from the execution of the command) - code 400
    -- Exception: return JSON with key "MESSAGE" and value f"Exception {e}" where e is the exception error. Code 500
    """
    response = {}
    result = "Code not reached getting the result"
    try:
        sensor_type = request.args.get("type", None)

        if DEBUG:
            print("GET respond() msg: {}".format(sensor_type))

        if not sensor_type:  # invalid/missing message
            response["MESSAGE"] = "Failed: type parameter is missing"
            status = 400
        else:  # valid message
            sql_get_all_command = "SELECT * FROM SENSORS"
            if sensor_type == "all":
                result = db_obj.execute_sql(sql_get_all_command)
            else:
                result = db_obj.execute_sql(f"{sql_get_all_command} WHERE type='{sensor_type}'")
            if result[0]:

                execution_result = result[1].fetchall()  # method that fetches all the remaining tuples
                # from the last executed statement from a table (returns a list of tuples)
                response["MESSAGE"] = "Succeeded: data retrieved successfully"
                response["RESULT"] = []
                for row in execution_result:
                    response["RESULT"].append({"id": row[0], "sensor name": row[1], "type": row[2]})
                status = 200
            else:
                response['MESSAGE'] = f"Error retrieving sensors {result[1]}"
                status = 400
    except Exception as e:
        print(e)
        print(result)
        response["MESSAGE"] = f"Exception {e}"
        status = 500
    # Return the response in json format with status code
    return jsonify(response), status


@app.route('/api/getlocations/', methods=['GET'])
def get_locations():
    """
    get locations should return a JSON object with all the locations and their IDs
    Parameters:
      No parameters 
    Returns:
    -- If failed in retrieving the locations, return JSON object with "MESSAGE" key and value
     f"Error retrieving locations {error}" (error from the execution of the command) - code 400
    -- If successful, return JSON object with 
     ----"MESSAGE" key and value "Succeeded: data retrieved successfully"
     ----"RESULT" key and the value is a list of the locations in JSON objects.
     Each object has "location" and "location_id"
    -- If an exception occurred in the whole function, return JSON object with "MESSAGE" key and value
    f"Exception {e}" where e is the exception message - code 500
    - Example of the return:
    {"MESSAGE": "Succeeded: data retrieved successfully",
    "RESULT":[{"location":"Main Gate","location_id":1},
            {"location":"Left Lower Corner","location_id":2},{"location":"Right Lower Corner","location_id":3},
            {"location":"Left Upper Corner","location_id":4},{"location":"Right Upper Corner","location_id":5},
            {"location":"Middle","location_id":6}]}
    NOTE: location and location_id order is not relevant as these elements are accessed by KEY and not index
        (check dictionaries in python for more clarification)
    """
    # TODO
    raise NotImplementedError("PLease implement method and remove this line from code when done")


@app.route('/api/getsensorsinlocations/', methods=['GET'])
def get_sensors_in_locations():
    """
    get sensors in location api takes sensor id or location id and returns a list of sensors located at location
    Parameters: 
    -sensor_id (int)--> sensor id (optional)
    -location_id (int) --> location id(optional)
    Returns:
    -- If any of the IDs is not a valid integer, return JSON with key "MESSAGE" and value
    "Error: IDs are not a valid integer" - code 400
    -- If failed in retrieving the data, return JSON object with "MESSAGE" key and value
    f"Error retrieving sensors in location {error}" (error from the execution of the command) - code 400
    -- If succeeded, return JSON object with :
    ----"MESSAGE" key and value "Succeeded: data retrieved successfully" 
    ----"RESULT" key and the value is a list of the sensors in location
        (details below) in JSON objects. Each object has "location_id", "sensor_id" and "sensor_location_id"
    -- If none of the sensor or location id were specified, returned all from the sensors
    -- If sensor id is specified and no location: return the rows where the sensor id is available
    -- If location id is specified and no sensor id: return the rows where the location is available
    -- If both are specified, return the row where they are both available
    --Exception: return json with key "MESSAGE" and value f"Exception {e}" where e is the exception error. Code 500
    - The return format is always JSON:
    --- in case of successful data retrieval, RESULT key with value a list of the retrieved data - code 200
    Example for api/getsensorsinlocations?location_id=2:
    {   "MESSAGE": "Succeeded: data retrieved successfully",
        "RESULT": [
            {"location_id": 2, "sensor_id": 1,"sensor_location_id": 2},
            {"location_id": 2, "sensor_id": 5, "sensor_location_id": 4}
        ]
    }
    """
    # TODO
    raise NotImplementedError("PLease implement method and remove this line from code when done")


@app.route('/api/getlogsbydate/', methods=["GET"])
def get_logs_by_date():
    """
    get logs by date takes a start and/or end dates and returns the logs in this period
    Parameters:
    -- start (string) --> date only (no time) in this format mm-dd-YYYY (optional)
    -- end (string) --> date only (no time) in this format mm-dd-YYYY (optional)
    Returns:
    -- If either of the dates is not a valid date, return JSON object with key "MESSAGE" and value
    "Error: Dates are invalid or wrong format" - code 400
    -- If succeeded, return JSON object with :
    ----"MESSAGE" key and value "Succeeded: data retrieved successfully" 
    ----"RESULT" key and the value is a list of logs(details below) in JSON objects.
    Each object has log_id, sensor_location id, timestamp and value keys
    -- If start is specified and no end, return all logs from this date till the most recent entry
    -- If end is specified and no start, return all logs from the beginning till the end date
    -- If both, then return logs in this period (the logs on the start and end dates should be included HINT: your condition
    should be <= and >=)
    -- If none, return the last 20 log entries - order by log_id descending order
    -- Exception: return JSON object with key "MESSAGE" and value f"Exception {e}" where e is the exception error.
            Code 500

    Example return for /api/getlogsbydate?end=12-14-2022&start=12-10-2022:
    {
        "MESSAGE": "Succeeded: data retrieved successfully",
        "RESULT": [
            { "log_id": 9,"sensor_location_id": 3,"timestamp": "Tue, 13 Dec 2022 00:08:24 GMT","value": "30"},
            { "log_id": 10,"sensor_location_id": 4,"timestamp": "Mon, 12 Dec 2022 00:08:24 GMT","value": "40"},
            { "log_id": 11,"sensor_location_id": 5,"timestamp": "Sun, 11 Dec 2022 00:08:24 GMT","value": "50"},
            { "log_id": 12,"sensor_location_id": 6,"timestamp": "Sat, 10 Dec 2022 00:08:24 GMT","value": "60"}
        ]
    }
    """
    # TODO
    raise NotImplementedError("PLease implement method and remove this line from code when done")


#####################################################
# add data to server
#####################################################


@app.route('/api/addsensor/', methods=['PUT'])
def add_sensor():
    """
    add sensors should have arguments name and type.
    NOTE: Make sure the http method used is correct
    Parameters:
    sensor_name (string) --> the name of the sensor (mandatory)
    sensor_type (string) --> the type of the sensor (mandatory)
    Return: 
    -- If any parameter is missing, return JSON with "MESSAGE" key and value
    "Failed: name and/or type parameters are missing" - code 400
    -- If failed to add sensor, return in JSON object "MESSAGE" key with value
    f"Failed to add sensor {error}" (error from the execution of the command) - code 400
    -- If succeeded, return in JSON "MESSAGE" key with value "Succeeded: Sensor added successfully" - code 200
    -- Exception: return json with key "MESSAGE" and value f"Exception {e}" where e is the exception error. Code 500
    """
    # TODO
    raise NotImplementedError("PLease implement method and remove this line from code when done")


@app.route('/api/addsensorinlocation/', methods=['PUT'])
def add_sensor_in_location():
    """
    add sensor in location should allow you to specify a sensor and location ids
    NOTE: Make sure the http method used is correct
    Parameters:
    --sensor_id (int) --> Sensor ID (mandatory)
    --location_id (int) --> Location ID (mandatory)
    Returns:
    -- if sensor or location id is not available in parameters, return in JSON "MESSAGE" key with value
    "Failed: sensor id and/or location id parameters are missing" - code 400
    -- if sensor or location id is not an integer, return in JSON "MESSAGE" key with value
    "Error: IDs are not a valid integer" - code 400
    -- if insertion succeeded, return in  JSON "MESSAGE" key "Succeeded: Sensor added in location successfully"
        and code 200.
    -- Exception: return json with key "MESSAGE" and value f"Exception {e}" where e is the exception error. Code 500
    """
    # TODO
    raise NotImplementedError("PLease implement method and remove this line from code when done")


@app.route('/api/addlogentry/', methods=['PUT'])
def add_log_entry():
    """
    add log entry
    NOTE: Make sure the http method used is correct
    Parameters:
    s_l_id (int) --> sensor location id (mandatory)
    value (int) --> value of the sensor reading (mandatory)
    timestamp (string) --> date and time of the reading (mm-dd-yyyyThh:mm:ss) i.e 12-22-2022T10:15:20 (mandatory)
    Return:
    -- If a parameter is missing, return JSON object with key "MESSAGE" and value 
        "Failed: sensor location id (s_l_id), timestamp and/or value parameters are missing" - code 400
    -- If the ID is not a valid integer, return JSON object with key "MESSAGE" and value
    "Error: ID is not a valid integer" - code 400
    -- If the timestamp is not a valid date or valid format, return JSON oject with key "MESSAGE" and value
    "Error: Dates are invalid or wrong format" - code 400
    -- If insertion is successful: return JSON object with key "MESSAGE" and value
        "Succeeded: Log entry added successfully" and code 200.
    -- If failed then the MESSAGE value is "Failed to add log entry {error}" and
        error is any error returned from the transaction. code 400
    -- Exception: return json with key "MESSAGE" and value f"Exception {e}" where e is the exception error. Code 500
    """
    # TODO
    raise NotImplementedError("PLease implement method and remove this line from code when done")


#####################################################
# Delete data from server - TO BE USED IN THE TESTING
#####################################################


@app.route('/api/deletesensor/', methods=['DELETE'])
def delete_sensor():
    """
    delete a sensor by name 
    Parameters:
    sensor --> name of the sensor to be deleted (Mandatory)
    type --> type of the sensor to be deleted (Mandatory)
    Returns:
    -- if sensor parameter is missing, return JSON object with key "MESSAGE" and value
        "Failed: sensor and/or type parameter is missing" - code 400
    -- If successful: return JSON object with key "MESSAGE" and value
        "Succeeded: Sensor deleted successfully" - code 200
    -- If failure: return JSON object with key "MESSAGE" and value
        "Failed to delete sensor {error}" where error is any error message from the execution. - code 400
    -- Exception: return JSON object with key "MESSAGE" and value
        f"Exception {e}" where e is the exception error. Code 500
    """
    # TODO
    raise NotImplementedError("PLease implement method and remove this line from code when done")


@app.route('/api/deletesensorinlocation/', methods=['DELETE'])
def delete_sensor_in_location():
    """
    Delete sensor in location
    Parameters:
    -- sensor_id --> The id of the sensor
    -- location_id --> The id of the location  
    Return:
    -- If sensor id or location id is missing, return JSON object with key "MESSAGE" and value
    "Failed: sensor id and/or location id parameters are missing" - code 400
    -- If the IDs are not a valid integer, return JSON object with key
    "MESSAGE" and value "Error: IDs are not a valid integer" - code 400
    -- If deletion succeeded, return JSON object with key "MESSAGE" and value
    "Succeeded: Sensor in location is deleted successfully" - code 200
    -- If failed: return JSON object with key "MESSAGE" and value
    "Failed to delete sensor in location {error}" where error is any error message from the execution. - code 400
    -- Exception: return JSON object with key "MESSAGE" and value
     f"Exception {e}" where e is the exception error. Code 500
    """
    # TODO
    raise NotImplementedError("PLease implement method and remove this line from code when done")


@app.route('/api/deletelogbylogid/', methods=['DELETE'])
def delete_log_entry_by_log_id():
    """
    Delete log entry by log id
    Parameters: 
    -- log_id --> Log ID to be deleted
    Returns:
    -- If no log_id parameter, return JSON object with key "MESSAGE" and value
     "Failed: log_id parameter is missing" - code 400
    -- If the ID is not a valid integer, return JSON object with key "MESSAGE" and value
    "Error: ID is not a valid integer" - code 400
    -- If deletion succeeded, return JSON object with key "MESSAGE" and value
    "Succeeded: log entry is deleted successfully" - code 200
    -- If failed: return JSON object with key "MESSAGE" and value
    "Failed to delete log entry {error}" where error is any error message from the execution. - code 400
    -- Exception: return JSON object with key "MESSAGE" and value
    f"Exception {e}" where e is the exception error. Code 500
    """
    # TODO
    raise NotImplementedError("PLease implement method and remove this line from code when done")


#####################################################
# Update data from server
#####################################################


@app.route('/api/movesensorinlocation/', methods=['PUT'])
def move_sensor_in_location():
    """
    Move sensor from location to another
    Parameters:
    --s_l_id : sensor_location id to be updated (Mandatory)
    --new_location: the new location to be used for the sensor (Mandatory)
    Returns:
    -- If any of the parameters is missing, return JSON object with key "MESSAGE" and value "Failed: sensor location id
     (s_l_id) and/or new location id parameters are missing" - code 400
    -- If the IDs are not a valid integer, return JSON object with key "MESSAGE" and value "Error: IDs are not a valid
    integer" - code 400
    -- If the change is done successfully,  return JSON object with key "MESSAGE" and value "Succeeded: Sensor moved
    successfully in location" - code 200
    or "Failed to move sensor {error}" where error is any error message from the execution. - code 400
    -- Exception: return JSON object with key "MESSAGE" and value f"Exception {e}" where e is the exception error.
     Code 500
    """
    # TODO
    raise NotImplementedError("PLease implement method and remove this line from code when done")
