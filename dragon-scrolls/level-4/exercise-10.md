[Previous](exercise-9.md)
## Moving to a Persistent Datastore: Part 2
Now that we've created our database and a series of functions to interact with 
it, we need to incorporate that in the various functions of `api.py`. 

#### Step 1: Make a Datastore Connection Available to `api.py` Functions
Add the following code just after the definition of `FRIEND_RESOURCE_ELEMENTS`:
    
```python
@app.before_request
def connect_to_datastore():
    """
    Establish a connection to the store for each request.

    Make the connection available on Flask's special 'g' object.
    """
    g.datastore = sqlite3.connect("/tmp/friends.db")

@app.teardown_request
def disconnect_from_datastore(exception):
    """
    Close the connection to the datastore after each request.
    """
    datastore = getattr(g, 'datastore', None)
    if datastore is not None:
        datastore.close()
```

* The decorators `@app.before_request` and `@app.teardown_request` can be 
applied to any function that you want to execute before and after every
incoming request is processed by of our other functions.

* We're going to use these methods to open/close unique connections to our 
SQLite datastore so that they'll be available during request processing but
released after processing is completed for a given request.

* We attach the connection to a special flask object simply (and unfortunately)
called `g`.  This special object holds data that only persists for a 
single request lifecycle and allows multiple functions access to shared data
needed for request processing.

#### Step 2: Update `get_friends`
Change `get_friends` so that it looks like this:
```python
@app.route('/api/v1/friends', methods=['GET'])
def get_friends():
    """Return a representation of the collection of friend resources."""
    friends_collection = datastore.get_friends(g.datastore)
    return jsonify({"friends": friends_collection})
```

#### Step 3: Create Replace the Contents of `datastore.py`
Previously, this module held the record of our friends and a
helper function.  Going forward it will hold functions that interact
with our datastore - SQLite.

* Add the a new module docstring and `sqllite` import statement.
    ```python
    """
    This modules provides functions to interact with our SQLite datastore.
    """
    
    import sqlite3
    ```

    > ![info](../images/information.png) Note that `sqllite` module is 
    actually part of the standard library.  No need to download additional 
    libraries.
    
* Add a function that returns information on all your friends:
    ```python
    def get_friends(ds_connection: sqlite3.Connection) -> dict:
    """
    Return a representation of all rows in the friends table.

    Args:
        ds_connection (sqllite3.Connection): An active connection to a
            sqllite datastore containing a friends table.

    Returns
        A JSON ready dictionary representing all rows of the friends table.
    """
    cursor = ds_connection.execute(
        'select id, first_name, last_name, telephone, email, notes '
        'from friends')

    friends_collection = list()
    for friend_row in cursor.fetchall():
        friends_collection.append(
            {"id": friend_row[0],
             "first_name": friend_row[1],
             "last_name": friend_row[2],
             "telephone": friend_row[3],
             "email": friend_row[4],
             "notes": friend_row[5]})

    return friends_collection
    ```
    
    * `sqlite3.Connection` objects have a method called `execute` which allows
    you to, unsurprising, execute SQL statements against the datastore.  You
    can see here that we are doing a `select` statement to get data on all
    the rows in the friends table.
    
    * Because our data is no longer automatically structured for us the 
    way it was before in `datastore.friends`, an empty list is created and 
    populated with entries in a format that the API will be able to return as 
    JSON. 
    
* Add a function that returns information on a specific friend:
    ```python
    def get_friend(ds_connection: sqlite3.Connection, id: str) -> dict:
        """
        Obtain a specific friend record and return a representation of it.
    
        Args:
            ds_connection (sqllite3.Connection): An active connection to a
                sqllite datastore containing a friends table.
            id (str): An `id` value which will be used to find a specific
                datastore row.
    
        Returns
            A JSON ready dictionary representing a specific
            row of the friends table.
        """
        cursor = ds_connection.execute(
            'select id, first_name, last_name, telephone, email, notes '
            'from friends where lower(id) = ?',
            [id.lower()])
    
        friend_row = cursor.fetchone()
    
        if friend_row:
            return {
                "id": friend_row[0],
                "first_name": friend_row[1],
                "last_name": friend_row[2],
                "telephone": friend_row[3],
                "email": friend_row[4],
                "notes": friend_row[5]}
    ```
    * This function is similiar to the previous one.  There are a few differences however:
        * The `select` statement uses the function parameter `id` to lookup a 
        specific friend.  Much our old `datastore.existing_friend` function did.
            * Notice that a non-standard form of string interpolation is used 
            here (no use of the `format` method).  Instead `?` symbols in the
            SQL statement are replaced by values of a list given as the second 
            parameter of the method call.
            
                > ![alert]("../images/alert.png") This non-standard way of 
                string interpolation is actually a security feature.  Behind
                the scenes, the sqllite library inspects the values of the list
                to ensure that your code doesn't become a victim of SQL injection.
                
        * Since only one row should be returned from the `execute` call, only
        one record is pulled out from resulting `cursor` object.
        
        * A single dictionary is returned instead of a list of dictionaries. 
        This makes the return value of the function the same as `datastore.existing_friend`
        which means that we won't have to make significant changes to `api.py`
        
* Add a function to create a new friend record:
    ```python
    def add_friend(ds_connection: sqlite3.Connection, entry_data: dict):
        """
        Create a new row in the friends table.
    
        Args:
            ds_connection (sqllite3.Connection): An active connection to a
                sqllite datastore containing a friends table.
            entry_data (dict): The data needed to created a new entry.
        """
        ds_connection.execute(
            "insert into friends (id, first_name, last_name, telephone, email, notes) "
            "values (?, ?, ?, ?, ?, ?)",
            [entry_data['id'],
             entry_data['firstName'],
             entry_data['lastName'],
             entry_data['telephone'],
             entry_data['email'],
             entry_data['notes']])
        ds_connection.commit()
    ```
    * This function performs an SQL `insert` statement, which is used to create
    new rows in a given table. 
    * It also uses the `ds_connection.commit` method.  This effectively makes 
    your new row permanent in the datastore.
    
* Add a function to update an existing friend record:
    ```python
    def fully_update_friend(ds_connection: sqlite3.Connection, entry_data: dict):
        """
        Update all aspects of given row in the friends table.
    
        Args:
            ds_connection (sqllite3.Connection): An active connection to a
                sqllite datastore containing a friends table.
            entry_data (dict): The data needed to update a given entry.  The
                `id` value of this dictionary is used to identify the entry
                to update.
        """
        ds_connection.execute(
            "UPDATE friends "
            "SET id=?, first_name=?, last_name=?, telephone=?, email=?, notes=? "
            "WHERE lower(id) = ?",
            [entry_data['id'],
             entry_data['firstName'],
             entry_data['lastName'],
             entry_data['telephone'],
             entry_data['email'],
             entry_data['notes'],
             entry_data['id'].lower()])
        ds_connection.commit()
    ```
    * This function is almost identical to the previous one except:
        * It uses the sql `update` command and associated syntax.
        * `entry_data['id']` is injected into the statement twice, both as a 
        value to update and as a key for the `WHERE` clause of the statement 
        to lookup the existing entry.
        
* Add a function to delete an existing friend record:
    ```python
    def delete_friend(ds_connection: sqlite3.Connection, id: str) -> dict:
    """
        Delete a given entry from the friends table in a given SQLite connection.
    
        Args:
            ds_connection (sqllite3.Connection): An active connection to a
                sqllite datastore containing a friends table.
            id (str): An `id` value which will be used to find a specific
                datastore row to delete.
        """
        cursor = ds_connection.execute(
            'DELETE  '
            'from friends where lower(id) = ?',
            [id.lower()])
    
        if not cursor.rowcount:
            raise ValueError()
    
        ds_connection.commit()
    ```
    
    * Note that this function checks to see if there is a non-zero value
    for `cursor.rowcount`.  If not, it raises a `ValueError` exception.  
        * As a reminder, this type of exception is raised when a given parameter 
        is of the correct type, but a invalid value.
        * This will occur in this function when the value of the `id` parameter
        is set to something that has no match in the datastore, and therefore
        can not be deleted.
    