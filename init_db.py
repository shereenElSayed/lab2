import sys
from DBobj import DBobj

def create_db(dbobj, dbname):
    if not dbobj.create_db(dbname):
        sys.exit(1)
    

def create_tables(dbobj):
    ## sensors table
    tablestructure = \
    """(sensor_id serial PRIMARY KEY,
    name VARCHAR (50) NOT NULL,
    type VARCHAR (50) NOT NULL 
    )
    """

    if not dbobj.create_table("sensors", tablestructure):
        print("Error creating table: sensors")
        sys.exit(1)

    ## locations table
    tablestructure =\
    """(location_id serial PRIMARY KEY,
    location VARCHAR (50)
    )
    """

    if not dbobj.create_table("locations", tablestructure):
        print("Error creating table: locations")
        sys.exit(1)

    ## deployed sensors and their locations
    tablestructure =\
    """(s_l_id serial PRIMARY KEY,
    sensor_id INT NOT NULL,
    location_id INT NOT NULL,
    FOREIGN KEY (sensor_id) REFERENCES sensors (sensor_id),
    FOREIGN KEY (location_id) REFERENCES locations (location_id)
    )
    """
    if not dbobj.create_table("sensors_locations", tablestructure):
        print("Error creating table: sensors_locations")
        sys.exit(1)

    ## logging sensors data
    tablestructure =\
    """(log_id serial PRIMARY KEY,
    s_l_id INT NOT NULL,
    timestamp timestamp NOT NULL,
    value VARCHAR(50) NOT NULL,
    FOREIGN KEY (s_l_id) REFERENCES sensors_locations (s_l_id)
    )"""

    if not dbobj.create_table("logging", tablestructure):
        print("Error creating table: logging")
        sys.exit(1)


def add_data(dbobj):
    # READ insertion statements from file
    with open ("db_seed.txt", "r") as seed_file:
        for statement in seed_file.readlines():
            if statement.strip() == "":
                continue
            dbobj.execute_sql(statement)

if __name__ == "__main__":
    
    username =  "postgres"
    password = "postgres"
    
    if len(sys.argv) == 3:
        username = sys.argv[1]
        password = sys.argv[2]
    
    elif len(sys.argv) == 2:
        username = sys.argv[1]
        password = ""
    
    dbobj = DBobj("postgres", user=username, pwd=password)
    create_db(dbobj, "sensors_data")
    print("Creating db succeeded")
    dbobj.closeConnection()
    
    #Connect to sensors_data db
    dbobj = DBobj("sensors_data", user=username, pwd=password)
    print("In sensors_data db")
    create_tables(dbobj)
    print("create table succeeded")
    add_data(dbobj)
    dbobj.closeConnection()
    

