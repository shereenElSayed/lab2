import psycopg2, sys, argparse
import os


class DBobj(object):

    def __init__(self, dbname, user, pwd, host="localhost") -> None:

        args = "dbname='{0}' user='{1}' host='{2}' password='{3}'".format(dbname, user, host, pwd)
        try:
            self.conn = psycopg2.connect(args)
        except Exception as e:
            print(e)
            print('Problem connecting to DB')
            sys.exit(1)

    def change_connection(self, dbname, user, pwd, host="localhost") -> tuple:
        args = "dbname='{0}' user='{1}' host='{2}' password='{3}'".format(dbname, user, host, pwd)
        try:
            self.conn = psycopg2.connect(args)
        except Exception as e:
            print(e)
            print('Problem connecting to DB')
            return False, e

    def create_db(self, dbname):
        if dbname == "":
            error = "DB name cannot be empty"
            print(error)
            return [False, error]
        sql = f'CREATE database {dbname}'
        self.conn.autocommit = True

        curs = self.conn.cursor()
        try:
            curs.execute(sql)
        except Exception as e:
            print(e)
            print(f"Unable to create database {dbname}")
            return False, e
        self.conn.autocommit = False
        return True, None

    def get_cursor(self, svrcursor=None):
        if svrcursor:
            return self.conn.cursor(svrcursor)
        return self.conn.cursor()

    def commit(self):
        if self.conn:
            self.conn.commit()

            # create a table

    def create_table(self, tablename, tablestructure):
        curs = self.conn.cursor()
        try:
            curs.execute("DROP TABLE IF EXISTS {0}".format(tablename))
            curs.execute("CREATE TABLE {0} {1}".format(tablename, tablestructure))
        except Exception as e:
            print(e)
            print(
                'Error: unable to create table {0}, in exceptional case. Type: \n{1}'.format(tablename, tablestructure))
            return False, e
        self.conn.commit()
        return True, None

    # delete a table
    def rm_table(self, tablename):
        curs = self.conn.cursor()
        try:
            curs.execute("DROP TABLE IF EXISTS {0}".format(tablename))
        except Exception as e:
            print(f"Unexpected issue in dropping table {e}")
        self.conn.commit()

    # invoke an SQL query on the db
    def execute_sql(self, sql):
        cur = self.conn.cursor()
        try:
            cur.execute(sql)
            self.conn.commit()
            if sql.lower().startswith("create"):
                return True, None
            if sql.lower().startswith("select"):
                return True, cur
            if cur.rowcount > 0:
                return True, cur
            else:
                return False, f"Number of affected rows: {cur.rowcount} rows"
        except Exception as e:
            print(e)
            print('execute_sql: SQL problem:\n\t{0}'.format(sql))
            self.conn.rollback()
            return False, e
        
            # sys.exit(1)

    # close the DB connection
    def close_connection(self):
        if self.conn:
            self.conn.commit()
            self.conn.close()
