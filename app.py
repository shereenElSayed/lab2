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
        # response["MESSAGE"] = f"Welcome {msg}!"
        status = 200

    # Return the response in json format with status code
    return jsonify(response), status

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




def main():
    '''The threaded option for concurrent accesses, 0.0.0.0 host says listen to all network interfaces (leaving this off changes this to local (same host) only access, port is the port listened on -- this must be open in your firewall or mapped out if within a Docker container. In Heroku, the heroku runtime sets this value via the PORT environment variable (you are not allowed to hard code it) so set it from this variable and give a default value (8118) for when we execute locally.  Python will tell us if the port is in use.  Start by using a value > 8000 as these are likely to be available.
    '''
    localport = int(os.getenv("PORT", 8000))
    app.run(threaded=True, host='0.0.0.0', port=localport)

if __name__ == '__main__':
    main()