import sqlite3
import os

SQL_dir = os.getcwd() + 'Keylogger.db'


def SQLquery(query, params, one=False):
    """
    Using for insert data to database
    :param query:   SQL query string
    :param params:  SQL query string parameters
    :param one:     fetch one result or all results
    :return:        query result
    """
    conn = sqlite3.connect(SQL_dir)
    c = conn.cursor()
    cursor = c.execute(query, params)
    res = cursor.fetchall()
    conn.close()
    return (res[0] if res else None) if one else res


def SQLupdate(query, params):
    """
    Using for update (insert, update, delete) data in database
    :param query:   SQL string
    :param params:  SQL string parameters
    :return:        tuple id
    """
    conn = sqlite3.connect(SQL_dir)
    c = conn.cursor()
    c.execute(query, params)
    tuple_id = c.lastrowid
    conn.commit()
    conn.close()
    return tuple_id
