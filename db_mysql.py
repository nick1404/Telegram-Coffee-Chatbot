import mysql.connector as connection
import pandas as pd
from sqlalchemy import create_engine
import pymysql

# Create a decorator that connects to the DB and closes the connection once the function is done
def start_connection():
    # For server use:
    conn = connection.connect(user='nick', password='usalud35',
                              host='localhost',
                              database='orders')
    # conn = connection.connect(user='nick', password='usalud35',
    #                           host='mysql-11179-0.cloudclusters.net', port=11179,
    #                           database='orders')
    cursor = conn.cursor()
    return conn, cursor
    
def stop_connection(conn, cursor):
    cursor.close()
    conn.close()
    
def init_db(force=False):
    conn, cursor = start_connection()
    ''' Check that the required tables exist, else create them'''
    ''':param force: Create tables again'''
    if force:
        cursor.execute('DROP TABLE IF EXISTS order_basket')
        cursor.execute('DROP TABLE IF EXISTS client_info')
        cursor.execute('DROP TABLE IF EXISTS pending_orders')
    
    # Create a table in DB to store a user's order basket
    cursor.execute('''CREATE TABLE IF NOT EXISTS order_basket (
                        id INTEGER AUTO_INCREMENT PRIMARY KEY,
                        user_id INTEGER NOT NULL,
                        name TEXT NOT NULL,
                        quantity INTEGER NOT NULL,
                        price FLOAT NOT NULL,
                        total FLOAT,
                        ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                        ) DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci 
                        '''
                        )
    
    # Create a table in DB to store user addresses
    cursor.execute('''CREATE TABLE IF NOT EXISTS client_info (
                        user_id INTEGER NOT NULL,
                        latitude TEXT,
                        longitude TEXT, 
                        phone_number TEXT,
                        address TEXT
                        ) DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci '''
                        )
    
    # Create a table for pending orders
    cursor.execute('''CREATE TABLE IF NOT EXISTS pending_orders (
                        id INTEGER AUTO_INCREMENT PRIMARY KEY,
                        user_id INTEGER NOT NULL,
                        name TEXT NOT NULL,
                        quantity INTEGER NOT NULL,
                        price FLOAT NOT NULL,
                        total FLOAT,
                        ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                        ) DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci 
                        '''
                        )
    conn.commit()
    stop_connection(conn, cursor)
    
def add_order(user_id, name, quantity, price):
    ''' Добавляет единицу товара в таблицу'''
    conn, cursor = start_connection()
    cursor.execute('INSERT INTO pending_orders (user_id, name, quantity, price) VALUES (%s, %s, %s, %s)', (user_id, name, quantity, price))
    conn.commit()
    stop_connection(conn, cursor)

    
def list_order(user_id):
    '''List the basket to the user'''
    conn, cursor = start_connection()
    cursor.execute('UPDATE pending_orders SET total = quantity * price WHERE user_id = %s ', (user_id, ))
    cursor.execute('SELECT name, quantity, total FROM pending_orders WHERE user_id = %s', (user_id, ))
    list_of_tuples = cursor.fetchall()
    
    # Unpack a list of tuples and add each tuple into a list
    res_list = []
    for count, tup in enumerate(list_of_tuples):
        tup = list(tup)
        res_list.append(tup)
        yield res_list[count]
    stop_connection(conn, cursor)


def access_price_list(name):
    '''Access a required position in the price list'''
    conn, cursor = start_connection()
    cursor.execute('SELECT name, price FROM prices WHERE name = %s', (name, ))
    tup = cursor.fetchone()
    stop_connection(conn, cursor)
    return tup # Returns a tuple of (name, price) type

def write_geolocation(user_id, lat, long):
    conn, cursor = start_connection()
    cursor.execute('INSERT INTO client_info (user_id, latitude, longitude) VALUES (%s, %s, %s)', (user_id, lat, long))
    conn.commit()
    stop_connection(conn, cursor)
    
def write_phone(user_id, phone_number):
    conn, cursor = start_connection()
    cursor.execute('INSERT INTO client_info (user_id, phone_number) VALUES (%s, %s)', (user_id, phone_number))
    conn.commit()
    stop_connection(conn, cursor)
    
def write_adress(user_id, address):
    conn, cursor = start_connection()
    cursor.execute('INSERT INTO client_info (user_id, address) VALUES (%s, %s)', (user_id, address))
    conn.commit()
    stop_connection(conn, cursor)


def complete_order(user_id):
    '''Add pending order to the real order (once the "End Order" button is pressed by the user)'''
    conn, cursor = start_connection()
    cursor.execute('''INSERT INTO order_basket (user_id, name, quantity, price, total, ts)
                      SELECT user_id, name, quantity, price, total, ts FROM pending_orders WHERE user_id = %s''', (user_id, ))
    
    cursor.execute('UPDATE order_basket SET total = quantity * price WHERE user_id = %s ', (user_id, ))
    cursor.execute('DELETE FROM pending_orders WHERE user_id = %s', (user_id, )) # Delete rows from pending table
    conn.commit()
    stop_connection(conn, cursor)


def add_one(user_id):
    ''' Add one more quantity of the last good in the "pending" table'''
    conn, cursor = start_connection()
    cursor.execute('''UPDATE pending_orders SET quantity = quantity + 1, 
                                                total = quantity * price
                                                WHERE user_id = %s 
                                                order by id desc limit 1''', (user_id, ))
    conn.commit()
    stop_connection(conn, cursor)
    
def delete_one(user_id):
    ''' Delete one quantity of the last good in the "pending" table'''
    conn, cursor = start_connection()
    cursor.execute('''UPDATE pending_orders SET quantity = quantity - 1, 
                                                total = quantity * price
                                                WHERE user_id = %s 
                                                order by id desc limit 1''', (user_id, ))
    # cursor.execute('''DELETE FROM pending_orders WHERE quantity = 0''')
    conn.commit()
    stop_connection(conn, cursor) 
    
    
def select_last(user_id):
    '''Returns (name, quantity, total) of the last added product by the user'''
    conn, cursor = start_connection()
    cursor.execute('SELECT name, quantity, total FROM pending_orders WHERE user_id = %s ORDER BY id DESC LIMIT 1', (user_id, ))
    tup = cursor.fetchone()
    cursor.execute('DELETE FROM pending_orders WHERE quantity = 0')
    conn.commit()
    stop_connection(conn, cursor)
    return tup


def count_total(user_id):
    '''Count and return the total sum fopr all goods in the basket.'''
    conn, cursor = start_connection()
    cursor.execute('UPDATE pending_orders SET total = quantity * price WHERE user_id = %s ', (user_id, ))
    cursor.execute('SELECT SUM(total) FROM pending_orders WHERE user_id = %s', (user_id, ))
    total = cursor.fetchone()
    stop_connection(conn, cursor)
    return total

# Function that deletes user's order from DB after pressed "DONE" ??