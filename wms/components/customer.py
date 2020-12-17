"""All Customer API methods."""
import sqlite3


def insert(connection, customer_id, customer_name):
    """Add a new Customer to the database.

    Args:
        connection (sqlite3.Connection)
        customer_id (str)
        customer_name (str)
    """

    cur = connection.cursor()
    cur.execute('''INSERT INTO Customer (customerID, customerName) VALUES (?,?)''', (customer_id, customer_name))
    connection.commit()
    return cur.lastrowid


def delete_by_id(connection, customer_id):
    cur = connection.cursor()
    cur.execute('''DELETE FROM Customer WHERE customerID = ?''', (customer_id,))
    connection.commit()


def search_by_id(connection, customer_id=None, show_columns=None):
    cur = connection.cursor()
    columns = ", ".join(show_columns) if show_columns else "*"
    if customer_id is None:
        return _get_none(connection, columns)
    return cur.execute(f'''SELECT {columns} FROM Customer WHERE customerID = ?''', (customer_id,)).fetchall()


def search_by_name(connection, customer_name="", show_columns=None):
    cur = connection.cursor()
    columns = ", ".join(show_columns) if show_columns else "*"
    if customer_name == "":
        return _get_none(connection, columns)
    if customer_name == "*":
        return _get_all(connection, columns)
    return cur.execute(f'''SELECT {columns} FROM Customer WHERE customerName LIKE ?''',
                       ('%' + customer_name + '%',)).fetchall()


def max_id(connection):
    cur = connection.cursor()
    cur.execute('''SELECT MAX (customerID) FROM Customer''')
    _id = None
    try:
        _id = cur.fetchone()[0]
    except TypeError:
        pass
    return _id


def columns_names(connection):
    cur = connection.cursor()
    cur.execute('''SELECT * FROM Customer LIMIT 0''')
    columns = [i[0] for i in cur.description]
    return columns


def _get_all(connection, columns):
    cur = connection.cursor()
    cur.execute(f'''SELECT {columns} FROM Customer''')
    return cur.fetchall()


def _get_none(connection, columns):
    cur = connection.cursor()
    cur.execute(f'''SELECT {columns} FROM Customer LIMIT 0''')
    return cur.fetchall()

