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
    
    ''' Check that the required tables exist, else create them'''
    ''':param force: Create tables again'''
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
    cursor.execute('SELECT name, SUM(price) FROM order_basket WHERE user_id = ? GROUP BY price', (user_id, ))
    list_of_tuples = cursor.fetchall()
    
    # Unpack a list of tuples and add each tuple into a list
    res_list = []
    for count, tup in enumerate(list_of_tuples):
        tup = list(tup)
        res_list.append(tup)
        yield res_list[count]
    
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
    tup = cursor.fetchone()
    return tup # Returns a tuple of (name, price) type
    

'''Need this code to get all lists in the generator object
   returned by list_order()'''
# for lst in list_order(user_id=1488):
#     print(lst)