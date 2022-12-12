import psycopg2, sys, argparse

class DBobj(object):
    
    def __init__(self, dbname, user="postgres", pwd="postgres", host="localhost") -> None:
        args = "dbname='{0}' user='{1}' host='{2}' password='{3}'".format(dbname,user,host,pwd)
        try:
            self.conn = psycopg2.connect(args)
        except Exception as e:
            print(e)
            print('Problem connecting to DB')
            sys.exit(1)
    
    def get_cursor(self,svrcursor=None):
        if svrcursor:
            return self.conn.cursor(svrcursor)
        return self.conn.cursor()

    def commit(self):
        if self.conn:
            self.conn.commit() 
    
    #create a table
    def create_table(self,tablename,tablestructure):
        curs = self.conn.cursor()
        try:
            curs.execute("DROP TABLE IF EXISTS {0}".format(tablename))
            curs.execute("CREATE TABLE {0} {1}".format(tablename,tablestructure))
        except Exception as e:
            print(e)
            print('Error: unable to create table {0}, in exceptional case. Type: \n{1}'.format(tablename,tablestructure))
            return False
        self.conn.commit()
        return True
    
        #delete a table
    def rm_table(self,tablename):
        curs = self.conn.cursor()
        try:
            curs.execute("DROP TABLE {0}".format(tablename))
        except:
            pass
        self.conn.commit()

        #invoke an SQL query on the db
    def execute_sql(self,sql):
        cur = self.conn.cursor()
        try:
            cur.execute(sql)
            self.conn.commit()
        except Exception as e:
            print(e)
            print('execute_sql: SQL problem:\n\t{0}'.format(sql))
            sys.exit(1)
        return cur

    #close the DB connection
    def closeConnection(self):
        if self.conn:
            self.conn.commit()
            self.conn.close()