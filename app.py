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


@app.route('/api/getsensors/', methods=['GET'])
def getsensors():
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
            cur = db_obj.execute_sql("SELECT * FROM SENSORS")
        else:
            cur = db_obj.execute_sql(f"SELECT * FROM SENSORS WHERE type='{type}'")
        result = cur.fetchall()
        response["RESULT"] = []
        for row in result:
            response["RESULT"].append({"sensor name": row[1], "type": row[2]})
        status = 200

    # Return the response in json format with status code
    return jsonify(response), status

'''
get locations should return a json format with all the locations and their IDs
Return:
- If there is an error in retrieving the locations, return json with MESSAGE key and value "Error retrieving locations" - code 400
- If succeeded, return json with RESULT and a list of the returned data - code 200
'''
@app.route('/api/getlocations/', methods=['GET'])
def getlocations():
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
def getsensorsinlocations():
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
@app.route('/api/getlogsbydate', method=["GET"])
def getlogs():
    ## TODO
    pass

'''
add sensors should have arguments name and type.
Return: 
--If no sensor available in the table with same name and type, return message: Sensor added successfully - code 200
--If an argument is missing, return "Argument is missing, please pass name and type for the sesnor as argument" - code 400
--If sensor exists, return "Failed: Sensor exists in the database"- code 400
'''
@app.route('/api/addsensors/', methods=['PUT'])
def addsensors():
    ## TODO
    pass

'''
add sensor in location should allow you to specify a location id 
'''
@app.route('/api/addsensorinlocation/', methods=['PUT'])
def addsensorinlocation():
    ## TODO
    pass


def main():
    '''The threaded option for concurrent accesses, 0.0.0.0 host says listen to all network interfaces (leaving this off changes this to local (same host) only access, port is the port listened on -- this must be open in your firewall or mapped out if within a Docker container. In Heroku, the heroku runtime sets this value via the PORT environment variable (you are not allowed to hard code it) so set it from this variable and give a default value (8118) for when we execute locally.  Python will tell us if the port is in use.  Start by using a value > 8000 as these are likely to be available.
    '''
    localport = int(os.getenv("PORT", 8000))
    app.run(threaded=True, host='0.0.0.0', port=localport)

if __name__ == '__main__':
    main()