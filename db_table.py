"""
Boiler plate from my past python projects. Adapted to fit the needs of this one.
"""

# sqlite db communication
import sqlite3

# Very basic SQLite wrapper
#
# Creates table from schema
# Provides small set of utility functions to query the database
#
#
class db_table:
    # SQLite database filename
    DB_NAME = "commodity_prices.db"

    #
    # model initialization
    # records table name and schema
    # creates the table if it does not exist yet in DB
    #
    # \param name    string                name of the DB table
    # \param schema  dict<string, string>  schema of DB table, mapping column name to their DB type & constraint
    #
    # Example: table("users", { "id": "integer PRIMARY KEY", "name": "text" })
    #
    def __init__(self, name, schema):
        # error handling
        if not name:
            raise RuntimeError("invalid table name")
        if not schema:
            raise RuntimeError("invalid database schema")

        # init fields and initiate database connection
        self.name = name
        self.schema = schema
        self.db_conn = sqlite3.connect(self.DB_NAME)

        # ensure the table is created
        self.create_table()

    #
    # CREATE TABLE IF NOT EXISTS wrapper
    # Create the database table based on self.name and self.schema
    # If table already exists, nothing is done even if the schema has changed
    #
    def create_table(self):
        # { "id": "integer", "name": "text" } -> "id integer, name text"
        columns_query_string = ', '.join(["%s %s" % (k, v) for k, v in self.schema.items()])

        # CREATE TABLE IF NOT EXISTS users (id integer PRIMARY KEY, name text)
        self.db_conn.execute("CREATE TABLE IF NOT EXISTS %s (%s)" % (self.name, columns_query_string))
        self.db_conn.commit()

    #
    # SELECT wrapper
    # Query the database by applying the specified filters
    #
    # \param columns  array<string>         columns to be fetched. if empty, will query all the columns
    # \param where    dict<string, string>  where filters to be applied. only combine them using AND and only check for strict equality
    #
    # \return [ { col1: val1, col2: val2, col3: val3 } ]
    #
    # Example table.select(["name"], { "id": "42" })
    #         table.select()
    #         table.select(where={ "name": "John" })
    #
    def select(self, columns=[], where={}):
        # by default, query all columns
        if not columns:
            columns = [k for k in self.schema]

        # build query string
        columns_query_string = ", ".join(columns)
        query = "SELECT %s FROM %s" % (columns_query_string, self.name)

        # build where query string
        if where:
            where_query_string = ["%s = '%s'" % (k, v) for k, v in where.items()]
            query += " WHERE " + ' AND '.join(where_query_string)

        result = []
        # SELECT id, name FROM users [ WHERE id=42 AND name=John ]
        for row in self.db_conn.execute(query):
            result_row = {}
            # convert from (val1, val2, val3) to { col1: val1, col2: val2, col3: val3 }
            for i in range(0, len(columns)):
                result_row[columns[i]] = row[i]
            result.append(result_row)

        return result

    #
    # INSERT INTO wrapper
    # insert the given item into database
    #
    # \param item  dict<string, string>   item to be insert in DB, mapping column to value
    #
    # \return id of the created record
    #
    # Example table.insert({ "id": "42", "name": "John" })
    #
    def insert(self, item):
        # build columns & values queries
        columns_query = ", ".join(item.keys())
        values_query = ", ".join(["'%s'" % v for v in item.values()])

        # INSERT INTO users(id, name) values (42, John)
        cursor = self.db_conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO %s(%s) values (%s)" % (self.name, columns_query, values_query))
        cursor.close()
        self.db_conn.commit()
        return cursor.lastrowid

    #
    # UPDATE wrapper
    # update multiple rows matching the specified condition
    #
    # \param values  dict<string, string>  values to be updates, mapping column to value
    # \param where   dict<string, string>  where filters to be applied. only combine them using AND and only check for strict equality
    #
    # \return number of updated records
    #
    # Example table.update({ "name": "Simon" }, { "id": 42 })
    #
    def update(self, values, where):
        # build set & where queries
        set_query = ", ".join(["%s = '%s'" % (k, v) for k, v in values.items()])
        where_query = " AND ".join(["%s = '%s'" % (k, v) for k, v in where.items()])

        # UPDATE users SET name = Simon WHERE id = 42
        cursor = self.db_conn.cursor()
        cursor.execute("UPDATE %s SET %s WHERE %s" % (self.name, set_query, where_query))
        cursor.close()
        self.db_conn.commit()
        return cursor.rowcount

    def select_prices_between_dates(self, start_date, end_date, commodity_type):
        sql = "SELECT Date, %s FROM Prices WHERE Date BETWEEN %s AND %s" %(commodity_type, start_date, end_date)

        results = []
        print(start_date)
        print(end_date)
        for result in self.db_conn.execute(sql):
            results.append(result)

        return results
    #
    # Close the database connection
    #
    def close(self):
        self.db_conn.close()
