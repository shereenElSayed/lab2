from DBobj import DBobj

def create_tables(dbobj):
    ## sensors table
    tablestructure = \
    """(sensor_id serial PRIMARY KEY,
    name VARCHAR (50) NOT NULL,
    type VARCHAR (50) NOT NULL 
    )
    """

    dbobj.create_table("sensors", tablestructure)

    ## locations table
    tablestructure =\
    """(location_id serial PRIMARY KEY,
    location VARCHAR (50)
    )
    """

    dbobj.create_table("locations", tablestructure)

    ## deployed sensors and their locations
    tablestructure =\
    """(s_l_id serial PRIMARY KEY,
    sensor_id INT NOT NULL,
    location_id INT NOT NULL,
    FOREIGN KEY (sensor_id) REFERENCES sensors (sensor_id),
    FOREIGN KEY (location_id) REFERENCES locations (location_id)
    )
    """
    dbobj.create_table("sensors_locations", tablestructure)

    ## logging sensors data
    tablestructure =\
    """(log_id serial PRIMARY KEY,
    s_l_id INT NOT NULL,
    timestamp timestamp NOT NULL,
    value VARCHAR(50) NOT NULL,
    FOREIGN KEY (s_l_id) REFERENCES sensors_locations (s_l_id)
    )"""

    dbobj.create_table("logging", tablestructure)


def add_data(dbobj):
    # READ insertion statements from file
    with open ("db_seed.txt", "r") as seed_file:
        for statement in seed_file.readlines():
            if statement.strip() == "":
                continue
            dbobj.execute_sql(statement)

if __name__ == "__main__":
    dbobj = DBobj("sensors_data")
    # create_tables(dbobj)
    add_data(dbobj)
    

