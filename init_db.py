import os
import sys
from DBobj import DBobj
import dotenv


def create_db(dbobj, dbname):
    if not dbobj.create_db(dbname)[0]:
        sys.exit(1)


# TODO: (to TA!!!!) move this to db_seed
def create_tables(dbobj):
    ## sensors table
    tablestructure = \
        """(sensor_id serial PRIMARY KEY,
        name VARCHAR (50) NOT NULL,
        type VARCHAR (50) NOT NULL ,
        UNIQUE (name, type)
        )
        """

    if not dbobj.create_table("sensors", tablestructure)[0]:
        print("Error creating table: sensors")
        sys.exit(1)

    ## locations table
    tablestructure = \
        """(location_id serial PRIMARY KEY,
        location VARCHAR (50)
        )
        """

    if not dbobj.create_table("locations", tablestructure)[0]:
        print("Error creating table: locations")
        sys.exit(1)

    ## deployed sensors and their locations
    tablestructure = \
        """(s_l_id serial PRIMARY KEY,
        sensor_id INT NOT NULL,
        location_id INT NOT NULL,
        FOREIGN KEY (sensor_id) REFERENCES sensors (sensor_id),
        FOREIGN KEY (location_id) REFERENCES locations (location_id),
        UNIQUE (sensor_id, location_id)
        )
        """
    if not dbobj.create_table("sensors_locations", tablestructure)[0]:
        print("Error creating table: sensors_locations")
        sys.exit(1)

    ## logging sensors data
    tablestructure = \
        """(log_id serial PRIMARY KEY,
        s_l_id INT NOT NULL,
        timestamp timestamp NOT NULL DEFAULT NOW(),
        value VARCHAR(50) NOT NULL,
        FOREIGN KEY (s_l_id) REFERENCES sensors_locations (s_l_id)
        )"""

    if not dbobj.create_table("logging", tablestructure)[0]:
        print("Error creating table: logging")
        sys.exit(1)


def execute_seed(dbobj):
    # READ insertion statements from file
    with open("db_seed.txt", "r") as seed_file:
        for statement in seed_file.readlines():
            if statement.strip() == "":
                continue
            result = dbobj.execute_sql(statement)
            if not result[0]:
                print(result[1])
                sys.exit(1)


# to TA to do late: add function to check if tabkes exist on the start of app

if __name__ == "__main__":

    if len(sys.argv) == 3:
        username = sys.argv[1]
        password = sys.argv[2]
    else:
        dotenv.load_dotenv()
        username = os.environ.get("PGUSER")
        password = os.environ.get("PGPASSWORD")

    dbobj = DBobj("postgres", user=username, pwd=password)
    create_db(dbobj, "sensors_data")
    print("Creating db succeeded")
    dbobj.close_connection()

    # Connect to sensors_data db
    dbobj = DBobj("sensors_data", user=username, pwd=password)
    print("In sensors_data db")
    execute_seed(dbobj)
    # dbobj.close_connection()
    # print("Database connection closed")
