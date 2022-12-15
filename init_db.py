import sys
from DBobj import DBobj

def create_db(dbobj, dbname):
    if not dbobj.create_db(dbname)[0]:
        sys.exit(1)
    

def create_tables(dbobj):
    ## sensors table
    tablestructure = \
    """(sensor_id serial PRIMARY KEY,
    name VARCHAR (50) NOT NULL,
    type VARCHAR (50) NOT NULL 
    )
    """

    if not dbobj.create_table("sensors", tablestructure)[0]:
        print("Error creating table: sensors")
        sys.exit(1)

    ## locations table
    tablestructure =\
    """(location_id serial PRIMARY KEY,
    location VARCHAR (50)
    )
    """

    if not dbobj.create_table("locations", tablestructure)[0]:
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
    if not dbobj.create_table("sensors_locations", tablestructure)[0]:
        print("Error creating table: sensors_locations")
        sys.exit(1)

    ## logging sensors data
    tablestructure =\
    """(log_id serial PRIMARY KEY,
    s_l_id INT NOT NULL,
    timestamp timestamp NOT NULL DEFAULT NOW(),
    value VARCHAR(50) NOT NULL,
    FOREIGN KEY (s_l_id) REFERENCES sensors_locations (s_l_id)
    )"""

    if not dbobj.create_table("logging", tablestructure)[0]:
        print("Error creating table: logging")
        sys.exit(1)
    
    


def add_data(dbobj):
    # READ insertion statements from file
    with open ("db_seed.txt", "r") as seed_file:
        for statement in seed_file.readlines():
            if statement.strip() == "":
                continue
            result = dbobj.execute_sql(statement)
            if not result[0]:
                print("Insertion failed")
                sys.exit(1)

if __name__ == "__main__":
    
    username =  "postgres"
    password = "postgres"
    
    if len(sys.argv) == 3:
        username = sys.argv[1]
        password = sys.argv[2]
    
    
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
    print("data inserted successfully")
    dbobj.closeConnection()
    print("Database connection closed")
    
