"""
Checks if sensor ID exists in sensors table and is an integer
Parameters:
--sensor_id: The sensor ID
Returns:
--True: if sesnor with this id exists in sensors table
--False: if sensor does not exist with this ID in sensors table
"""
def is_sensor_exist(sensor_id):
    ## TODO
    pass

"""
Checks if location ID exists in locations table and is an integer
Parameters:
--location_id: The location ID
Returns:
--True: if location with this id exists in locations table
--False: if location does not exist with this ID in location table
"""
def is_location_exist(location_id):
    ## TODO
    pass

"""
Checks if a sensor is installed in this location (from table sensors_locations)
Parameters:
--sensor_id: The sensor ID
--location_id: The location ID
Returns:
--True: if this sensor with the given ID is installed in the location with this ID
--False: else wise 
"""
def is_sensor_in_location(sensor_id, location_id):
    ## TODO
    pass

"""
Checks if the date and time in the timestamp are valid and in correct format as required
i.e the month is not 13 :D
Parameters:
--timestamp: The timestamp to be validated (a string with the format mm-dd-yyyyThh:mm:ss)
Return:
--True: if the timestamp is valid and in correct format
--False: else wise
NOTE: You can use any package for date validation, just be ready to justify your choice 
"""
def is_valid_timestamp(timestamp):
    ## TODO
    pass

"""
Checks if the date is valid and in correct format as required
i.e the month is not 13 :D
Parameters:
--date: The date to be validated (a string with the format mm-dd-yyyy)
Return:
--True: if the date is valid and in correct format
--False: else wise
NOTE: You can use any package for date validation, just be ready to justify your choice 
"""
def is_valid_date(date):
    ## TODO
    pass

