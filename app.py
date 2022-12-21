import os
from DBobj import DBobj
from flask import Flask, request, jsonify, make_response


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
    db_obj = DBobj("sensors_data")

@app.route('/')
def hello():
    return 'Welcome to CS190B Sensors Hub'

#####################################################
### Get data from server
#####################################################
''' Get sensors in our database
Parameters:
--type --> values: temperature/air_quality/humidity/gas/all
Returns:
List of sensors according to the type in JSON in "RESULT" key or the error msg in "MESSAGE"
'''
@app.route('/api/getsensors/', methods=['GET'])
def get_sensors():
    # Retrieve the msg from url parameter of GET request 
    # and return MESSAGE response (or error or success)
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
            
            execution_result = result[1].fetchall()
            response["RESULT"] = []
            for row in execution_result:
                response["RESULT"].append({"sensor name": row[1], "type": row[2]})
            status = 200
        else:
            response['MESSAGE'] = f"Error executing sql {result[1]}"
            status = 400

    # Return the response in json format with status code
    return jsonify(response), status

'''
get locations should return a json format with all the locations and their IDs
Return:
- If there is an error in retrieving the locations, return json with MESSAGE key and value "Error retrieving locations" - code 400
- If succeeded, return json with RESULT and a list of the returned data - code 200
'''
@app.route('/api/getlocations/', methods=['GET'])
def get_locations():
    ## TODO
    pass

'''
get sensors in location api takes sensor id or location id and returns a list
Parameters: 
-sensor_id --> sensor id (optional)
-location_id-> location id(optional)
Returns:
- If none of the sensor or location id were specified, returned all from the sensors
- If sensor id is specified and no location: return the rows where the sensor id is available
- If location id is specified and no sensor id: return the rows where the location is available
- If both are specified, return the row where they are both avaiable 
- The return format is always JSON:
--- in case of successful data retrieval, RESULT key with value a list of the retrieved data - code 200
--- in case of failure in retrieving data, MESSAGE key with value "Error: failed to retrieve data"
'''
@app.route('/api/getsensorsinlocations', methods=['GET'])
def get_sensors_in_locations():
    ## TODO
    pass


'''
get logs by date takes a start and/or end dates and returns the logs in this period
Parameters:
- start --> date only (no time) in this format mm_dd_YYYY (optional)
- end --> date only (no time) in this format mm_dd_YYYY (optional)
Return:
- If start is specified and no end, return all logs from this date till the most recent entry
- If end is specified and no start, return all logs from the beginning till the end date
- If both, then return logs in this period
- If none, return the last 20 log entries
If data retrie

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
Return: 
--If no sensor available in the table with same name and type, return message: Sensor added successfully - code 200
--If an argument is missing, return "Argument is missing, please pass name and type for the sesnor as argument" - code 400
--If sensor exists, return "Failed: Sensor exists in the database"- code 400
'''
@app.route('/api/addsensors/', methods=['PUT'])
def add_sensors():
    ## TODO
    pass

'''
add sensor in location should allow you to specify a location id 
'''
@app.route('/api/addsensorinlocation/', methods=['PUT'])
def add_sensor_in_location():
    ## TODO
    pass


'''
add log entry
Parameters:
s_l_id --> sensor location id
value --> value of the sensor reading
Return:
-- If a parameter is missing, return json with key "Message" and value 
    "Parameter is missing, expecting sensor location id (s_l_id) and value" - code 400
-- If both parameters are available, insertion is successful: return json with key "Message" and value
    "Transaction succeeded" and code 200. If failed then the message value is "Transaction failed {error}" 
    and error is any error returned from the transaction. code 400
'''
@app.route('/api/addlogentry/', methods=['PUT'])
def add_log_entry():
    ## TODO
    pass

#####################################################
### Delete data from server
#####################################################
'''
delete a sensor by name 
Parameters:
name --> name of the sensor to be deleted (Mandatory)
Returns:
-- if name is missing, return JSON with key "Message" and value "Parameter name is missing" - code 400
-- else, return JSON with key "Message" and value "Transaction succeeded" - code 200
or "Transaction failed {error}" where error is any error message from the execution. - code 400
Hint:
The sensor you are deleting is a foreign key in other tables ...
All occurences of this sensor in the DB should be deleted 
'''
@app.route('/api/deletesensor/', methods=['DELETE'])
def delete_sensor():
    ## TODO
    pass

#####################################################
### Update data from server
#####################################################
@app.route('/api/deletesensorinlocation', methods=['PUT'])
def delete_sensor_in_location():
    ## TODO 
    pass

def main():
    '''The threaded option for concurrent accesses, 0.0.0.0 host says listen to all network interfaces 
    (leaving this off changes this to local (same host) only access, port is the port listened on
    -- this must be open in your firewall or mapped out if within a Docker container. 
    '''
    localport = int(os.getenv("PORT", 8000))
    app.run(threaded=True, host='0.0.0.0', port=localport)

if __name__ == '__main__':
    main()