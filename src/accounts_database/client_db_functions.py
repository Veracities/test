import sqlite3
import sys
sys.path.insert(0, "../database")
import database_methods
import password_hash

def insert_user(username, email, name, password, account_type):
    '''
    Inserts a new user into the database (table User) and returns whether it
    was successfully input or not
    '''
    # time is stored as UNIX timestap in INT
    new_password = password_hash.hash_password(password)
    query = "INSERT INTO User values (?, ?, ?, ?, ?, strftime('%s','now'));"
    fields = (username, email, name, new_password, account_type)
    
    if (not(database_methods.execute_query(query, fields, 'users.db'))):
        insert_account(username, account_type)
        return True
    return False

def check_duplicate(username, email):
    '''
    Checks if there are duplicate keys which should be unique in the database.
    Returns list, bool for success, username, email
    '''
    (conn, cur) = database_methods.connection('users.db')
    query1 = "SELECT Username from User where Username = ?"
    fields1 = (username,)
    query2 = "SELECT Email from User where Email = ?"
    fields2 = (email,)
    
    try:
        cur.execute(query1, fields1)
        usernames = cur.fetchall()
        cur.execute(query2, fields2)
        emails = cur.fetchall()
        error = 0
    except sqlite3.Error as e:
        print(format(e))
        error = 1

    if (usernames and emails):
        return [False, usernames[0][0], emails[0][0]]
    elif (usernames):
        return [False, usernames[0][0], ""]
    elif (emails):
        return [False, "", emails[0][0]]
    else:
        return [True, "", ""]

def insert_account(username, account_type):
    if (account_type == "Agency"):
        status = "Active"
        query = "INSERT INTO Agency_User values (?, ?)"
        fields = (username, status)
        database_methods.execute_query(query, fields, 'users.db')
        
def login(username, password):
    '''
    Returns the name of the user and the type if login information is correct.
    '''
    (conn, cur) = database_methods.connection('users.db')
    query = ("SELECT Name, Type, Password from User where Username = ?")
    fields = (username,)

    try:
        cur.execute(query, fields)
        error = 0
    except sqlite3.Error as e:
        print(format(e))
        error = 1

    name = cur.fetchall()
    if (not(error) and name):
        correct_password = password_hash.verify_password(password, name[0][2])
        if (len(name) != 0 and correct_password):
            return (name[0][0], name[0][1])
        
    return (None, None)

def insert_file_info(num, username, filename, service, month, year):
    '''
    Inserts a record of a file submission into the database.
    '''
    query = ("INSERT INTO Submission_History "
            + "values (?, ?, ?, ?, ?, ?, strftime('%s','now'))")
    fields = (num, username, filename, service, month, year)
    database_methods.execute_query(query, fields, 'users.db')
    
def insert_request(num, username, desc):
    '''
    Insert a request from the TEQ staff into table Request.
    '''
    status = "Pending"
    query = ("INSERT INTO Request (ID, Username, Description, Status, "
             "Date_Submitted) values (?, ?, ?, ?, strftime('%s','now'))")
    fields = (num, username, desc, status)
    database_methods.execute_query(query, fields, 'users.db')

def accepted_request(num, username):
    '''
    An admin accepted a request for change in data fields.
    '''
    status = "Accepted"
    query = ("UPDATE Request SET Admin_Username = ?, Status = ?, "
             "Date_Accepted = strftime('%s','now') WHERE ID = ?")
    fields = (username, status, num)
    database_methods.execute_query(query, fields, 'users.db')

def update_agency_status(username, status):
    '''
    Update an agency's status.
    '''
    query = "Update Agency_User SET Status = ? WHERE Username = ?"
    fields = (status, username)
    database_methods.execute_query(query, fields, 'users.db')
    
def get_tables_names():
    '''
    A function which gets all the table names of a database.
    Returns a list of table names.
    '''
    (conn, curr) = connection() 
    curr.execute("SELECT name FROM sqlite_master WHERE type='table';")
    result = [row[0] for row in curr.fetchall()]
    return result

def check_email(email):
    '''
    Checks if an email exists in the database and returns True if it exists,
    False otherwise.
    '''
    (conn, cur) = database_methods.connection('users.db')
    query = ("SELECT email from User where Email = ?")
    fields = (email,)

    try:
        cur.execute(query, fields)
        error = 0
    except sqlite3.Error as e:
        print(format(e))
        error = 1

    if (not(error)):
        email = cur.fetchall()
        if (len(email) != 0):
            return True

    return False

def get_username(email):
    '''
    (str) -> (str, str)
    
    Getting username when given email
    '''
    (conn, cur) = database_methods.connection('users.db')
    query = ("SELECT Username, Name from User where Email = ?")
    fields = (email,)

    try:
        cur.execute(query, fields)
        error = 0
    except sqlite3.Error as e:
        print(format(e))
        error = 1

    if (not(error)):
        recieved = cur.fetchall()
        if (len(recieved) != 0):
            return (recieved[0][0], recieved[0][1])

    return (None, None)

def check_temp_pass(username, temp_pass):
    '''
    (str, str) -> (bool, bool)

    Checks if the user input a correct temporary password and returns whether
    the account has a temp_pass and if it matches to the input as a tuple
    '''
    (conn, cur) = database_methods.connection('users.db')
    query = ("SELECT Temp_Pass from Temp_Passcode where Username = ?")
    fields = (username,)

    try:
        cur.execute(query, fields)
        error = 0
    except sqlite3.Error as e:
        print(format(e))
        error = 1

    received = cur.fetchall()
    if (not(error) and received):
        correct_password = password_hash.verify_password(temp_pass,
                                                         received[0][0])
        if (len(received) != 0):
            return (True, correct_password)

    return (False, False)

def insert_temp_pass(username, temp_pass):
    '''
    Inserts a temporary passcode into the database, or updates it if it
    already exists
    '''
    hash_temp = password_hash.hash_password(temp_pass)
    query = ("INSERT OR REPLACE INTO Temp_Passcode (Username, Temp_Pass)" +
             " values (?, ?)")
    fields = (username, hash_temp)
    database_methods.execute_query(query, fields, 'users.db')

def remove_temp(username):
    '''
    Removes the temporary password after a new one is created
    '''
    query = ("DELETE FROM Temp_Passcode WHERE Username = ?")
    fields = (username,)
    database_methods.execute_query(query, fields, 'users.db')

def update_pass(username, password):
    '''
    Updates the user's password with the new one that was entered
    '''
    hash_temp = password_hash.hash_password(password)
    query = ("UPDATE User SET Password = ? WHERE Username = ?")
    fields = (hash_temp, username)
    database_methods.execute_query(query, fields, 'users.db')
