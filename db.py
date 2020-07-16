import sqlite3
import pandas as pd

# Create a decorator that connects to the DB and closes the connection once the function is done
def ensure_connection(func):
    
    def inner(*args, **kwargs):
        with sqlite3.connect('orders.db') as conn:
            kwargs['conn'] = conn
            res = func(*args, **kwargs)
        return res

    return inner

@ensure_connection
def init_db(conn, force=False): # Create individual tables for each user?
    
    ''' Check that the required tables exist, else create themё
    :param force: Create tables again'''
    cursor = conn.cursor()
    if force:
        cursor.execute('DROP TABLE IF EXISTS order_basket')
        cursor.execute('DROP TABLE IF EXISTS addresses')
    
    # Create a table in DB to store a user's order basket
    cursor.execute('''CREATE TABLE IF NOT EXISTS order_basket (
                        id INTEGER PRIMARY KEY,
                        user_id INTEGER NOT NULL,
                        name TEXT NOT NULL,
                        quantity INTEGER NOT NULL,
                        price FLOAT NOT NULL
                        )'''
                        )
    # Create a table in DB to store user addresses
    cursor.execute('''CREATE TABLE IF NOT EXISTS addresses (
                        id INTEGER PRIMARY KEY,
                        user_id INTEGER NOT NULL, 
                        address TEXT NOT NULL
                        )'''
                        )
    conn.commit()
 
@ensure_connection   
def add_order(conn, user_id, name, quantity, price):
    ''' Добавляет единицу товара в таблицу'''
    cursor = conn.cursor()
    cursor.execute('INSERT INTO order_basket (user_id, name, quantity, price) VALUES (?, ?, ?, ?)', (user_id, name, quantity, price))
    conn.commit()
    
@ensure_connection
def list_order(conn, user_id):
    '''List the basket to the user'''
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM order_basket WHERE user_id = ?', (user_id, ))
    results_tuples = cursor.fetchall()
    # Unpack a list of tuples and append to a new list of strings
    results_list = []
    for res in results_tuples:
        res_untuple = ''.join(res)
        results_list.append(res_untuple)
    return results_list

# Now transform the Excel price list into a table in the database
conn = sqlite3.connect('orders.db')
c = conn.cursor()
prices = pd.read_excel('prices.xlsx', header=0)
prices.to_sql('prices', conn, if_exists='replace', index=False)
conn.commit()

@ensure_connection
def access_price_list(conn, name):
    '''Access a required position in the price list'''
    cursor = conn.cursor()
    cursor.execute('SELECT name, price FROM prices WHERE name = ?', (name, ))    
    (name, price) = cursor.fetchone()
    return name, price