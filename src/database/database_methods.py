import sqlite3

def connection(database):
    '''
    Creates a connection to the database.
    '''
    try:
        conn = sqlite3.connect(database)
        cur = conn.cursor()
        # enable foreign key constraint
        cur.execute("PRAGMA foreign_keys = ON")
    except sqlite3.Error as e:
        print(format(e))
        
    return (conn, cur)

def execute_query(query, fields, database):
    '''
    Executes a SQL command using the query and fields.
    '''
    error = 1
    (conn, cur) = connection(database)
    try:
        cur.execute(query, fields)
        conn.commit()
        error = 0
    except sqlite3.Error as e:
        print(e)
        conn.rollback()
    
    return error 
    
def get_id(table):
    '''
    Gets maximum ID in the table.
    '''
    (conn, cur) = connection('client_data.db')
    query = ("select max(ID) from " + table)
    try:
        cur.execute(query)
        error = 0
    except sqlite3.Error as e:
        print(format(e))
        error = 1
    
    if (not(error)):
        val = cur.fetchone()
        if (val is not None and val[0] is not None):
            return val[0]
        else:
            return 0


def check_client(client_id, database):
    '''
    Checks if there is a row for the client with client_id. Returns 1 if yes
    and 0 otherwise.
    '''
    query = "SELECT 1 FROM Client WHERE Unique_ID_Value = " + str(client_id)
    
    (conn, cur) = connection(database)
    try:
        error = 0
        cur.execute(query)
    except sqlite3.Error as e:
        print(e)
        error = 1
    
    if (not(error)):
        val = cur.fetchone()
        if (val is not None and val[0] == 1):
            return 1
        else:
            return 0


def fetch_values(start, end, row_values, lst):
    '''
    Returns a list of the values extracted from a row in the excel file.
    '''
    i = start
    ret = lst
    while (i < end):
        value = row_values[i]
        ret.append(value)
        i += 1
    
    return ret

# General method for inserting with a list of indices
def fetch_values_list(row_values, index_list, val):
    i = 0
    while (i < len(index_list)):
        start = index_list[i][0]
        end = index_list[i][1]
        while (start < end):
            val.append(row_values[start])
            start += 1
        i += 1
    
    return val
