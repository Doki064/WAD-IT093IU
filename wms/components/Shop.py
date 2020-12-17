"""All Shop API methods."""
import sqlite3


def insert(connection, shop_id, shop_name):
    """Add a new shop to the database.

    Args:
        connection (sqlite3.Connection)
        shop_id (str)
        shop_name (str)
    """

    cur = connection.cursor()
    cur.execute('''INSERT INTO Shop (shopID, shopName) VALUES (?,?)''', (shop_id, shop_name))
    connection.commit()
    return cur.lastrowid


def delete_by_id(connection, shop_id):
    cur = connection.cursor()
    removed = cur.execute('''SELECT * FROM Shop WHERE shopID = ?''', (shop_id,))
    cur.execute('''DELETE FROM Shop WHERE shopID = ?''', (shop_id,))
    connection.commit()
    return removed.fetchall()


def search_by_id(connection, shop_id=None, show_columns=None):
    cur = connection.cursor()
    columns = ", ".join(show_columns) if show_columns else "*"
    if shop_id is None:
        return _get_none(connection, columns)
    return cur.execute(f'''SELECT {columns} FROM Shop WHERE shopID = ?''', (shop_id,)).fetchall()


def search_by_name(connection, shop_name="", show_columns=None):
    cur = connection.cursor()
    columns = ", ".join(show_columns) if show_columns else "*"
    if shop_name == "":
        return _get_none(connection, columns)
    if shop_name == "*":
        return _get_all(connection, columns)
    return cur.execute(f'''SELECT {columns} FROM Shop WHERE shopName LIKE ?''', ('%' + shop_name + '%',)).fetchall()


def search_all(connection):
    return _get_all(connection, "*")


def max_id(connection):
    cur = connection.cursor()
    cur.execute('''SELECT MAX (shopID) FROM Shop''')
    _id = None
    try:
        _id = cur.fetchone()[0]
    except TypeError:
        pass
    return _id


def columns_names(connection):
    cur = connection.cursor()
    cur.execute('''SELECT * FROM Shop LIMIT 0''')
    columns = [i[0] for i in cur.description]
    return columns


def _get_all(connection, columns):
    cur = connection.cursor()
    cur.execute(f'''SELECT {columns} FROM Shop''')
    get_all = None
    try:
        get_all = cur.fetchall()
    except TypeError:
        pass
    return get_all


def _get_none(connection, columns):
    cur = connection.cursor()
    cur.execute(f'''SELECT {columns} FROM Shop LIMIT 0''')
    return cur.fetchall()
