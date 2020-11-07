import telebot
import db_mysql
import config

# Initiate the bot
bot = telebot.TeleBot(config.TOKEN)

#Connect to the database
db_mysql.init_db() # Specify force=True to create fresh tables

@bot.message_handler(commands=['start'])
def main_menu(msg):
    
    keyboard = telebot.types.ReplyKeyboardMarkup()
    coffee = telebot.types.KeyboardButton('Заказать Кофе')
    milk = telebot.types.KeyboardButton('Заказать молоко')
    deliv = telebot.types.KeyboardButton('Доставка')
    other = telebot.types.KeyboardButton('Заказать другие товары для кофейни')
    keyboard.add(coffee, milk, deliv, other)
    bot.send_message(msg.chat.id, 'Вас приветствует CoffeePeopleBot! Здесь вы можете заказать все что вам нужно для вашей кофейни!', reply_markup=keyboard)

coffee_dict = {
    'brasil':'Бразилия Сантос (250 грн - 1 кг)', 
    'ef':'Эфиопия (250 грн - 1 кг)',
    'col':'Колумбия Супремо (300 грн - 1 кг)',
    'gond':'Гондурас (300 грн - 1 кг)',
    'sal':'Сальвадор (300 грн - 1 кг)',
    'gv':'Гватемала (300 грн - 1 кг)',
    'bur':'Бурунди (350 грн - 1 кг)',
    's_30':'70 арабики + 30 рабусты (220 грн - 1 кг)',
    'f_50':'50 арабики + 50 рабусты (200 грн - 1 кг)',
    't_70':'30 арабики + 70 рабусты (185 грн - 1 кг)',
    'main':'Главное Меню'
    }

@bot.message_handler(regexp='Заказать Кофе')
def choose_coffee(msg):
    keyboard = telebot.types.ReplyKeyboardMarkup()
    for key, value in coffee_dict.items():
        key = telebot.types.KeyboardButton(value)
        keyboard.add(key)
        
    bot.send_message(msg.chat.id, 'У нас в наличии зерновое кофе (100% Арабика) из множества стран. Закажите нужное вам кофе, нажав на кнопку.', reply_markup=keyboard)


# Loop through coffee dict to handle the buttons for each coffee
coffee_regex = "Бразилия Сантос \(250 грн - 1 кг\)|Эфиопия \(250 грн - 1 кг\)|Колумбия Супремо \(300 грн - 1 кг\)|Гондурас \(300 грн - 1 кг\)|Сальвадор \(300 грн - 1 кг\)|Гватемала \(300 грн - 1 кг\)|70 арабики \+ 30 рабусты \(220 грн - 1 кг\)|50 арабики \+ 50 рабусты \(200 грн - 1 кг\)|30 арабики \+ 70 рабусты \(185 грн - 1 кг\)|Бурунди \(350 грн - 1 кг\)" # pylint: disable=anomalous-backslash-in-string
                
@bot.message_handler(regexp=coffee_regex)
def coffee_purchase(msg):
    msg_text = msg.text.split(' (')[0]
    
    keyboard = telebot.types.ReplyKeyboardMarkup()
    add = telebot.types.KeyboardButton('+')
    delete = telebot.types.KeyboardButton('-')
    main = telebot.types.KeyboardButton('Главное Меню')
    basket = telebot.types.KeyboardButton('Корзина')
    keyboard.add(delete, add, main, basket)
    
    # Access the name and price of the good in the DB
    name_price = db_mysql.access_price_list(name=msg.text)
    
    bot.send_message(msg.chat.id, 'Вы выбрали Кофе {}. Вы можете изменить количество с помощью кнопок + и -.'.format(msg_text), reply_markup=keyboard)
    
    # Add order to the database
    db_mysql.add_order(user_id=msg.chat.id, name=name_price[0], quantity=1, price=name_price[1]) # Add quantity controls


milk_dict = {
    'gal':'Галичина (900гр, 2,5%) - 285 грн/ящик',
    'sel':'Селянское (900гр, 2,5%) - 285 грн/ящик',
    'bar':'Бариста ТМ Галичина (1л, 2,5%) - 252 грн/ящик',
    'nez':'Нежинское (1л, 2,5%) - 252 грн/ящик',
    'alpro':'Безлактозное "Alpro" - 90 грн/л',
    'main':'Главное Меню'
}

@bot.message_handler(regexp='Заказать молоко')
def choose_milk(msg):
    keyboard = telebot.types.ReplyKeyboardMarkup()
    for key, value in milk_dict.items():
        key = telebot.types.KeyboardButton(value)
        keyboard.add(key)

    bot.send_message(msg.chat.id, 'Вы можете заказать нужное вам молоко нажав на кнопки внизу.', reply_markup=keyboard)

milk_regex = 'Галичина \(900гр, 2,5\%\) - 285 грн\/ящик|Селянское \(900гр, 2,5\%\) - 285 грн\/ящик|Бариста ТМ Галичина \(1л, 2,5\%\) - 252 грн\/ящик|Нежинское \(1л, 2,5\%\) - 252 грн\/ящик|Безлактозное \"Alpro\" 90 грн\/л' # pylint: disable=anomalous-backslash-in-string


@bot.message_handler(regexp=milk_regex)
def milk_purchase(msg):
    msg_text = msg.text.split(' -')[0]
    keyboard = telebot.types.ReplyKeyboardMarkup()
    main = telebot.types.KeyboardButton('Главное Меню')
    basket = telebot.types.KeyboardButton('Корзина')
    add = telebot.types.KeyboardButton('+')
    delete = telebot.types.KeyboardButton('-')
    
    # Access the name and price of the good in the DB   
    name_price = db_mysql.access_price_list(name=msg.text)

    keyboard.add(delete, add, main, basket)
    bot.send_message(msg.chat.id, 'Вы выбрали Молоко {}. Вы можете изменить количество с помощью кнопок + и -.'.format(msg_text), reply_markup=keyboard)

    # Add the order to the DB
    db_mysql.add_order(user_id=msg.chat.id, name=name_price[0], quantity=1, price=name_price[1])


@bot.message_handler(regexp='Доставка')
def delivery(msg):
    keyboard = telebot.types.ReplyKeyboardMarkup()
    geo = telebot.types.KeyboardButton("На текущее местоположение", request_location=True)
    address = telebot.types.KeyboardButton('На другой адрес')
    post = telebot.types.KeyboardButton("Новой Почтой")
    drive = telebot.types.KeyboardButton('Самовывоз')
    main = telebot.types.KeyboardButton('Главное Меню')
    
    keyboard.add(geo, address, post, main, drive)
    bot.send_message(msg.chat.id, 'Вы можете заказать доставку до 9 утра (День в День). Доставка по Киеву от 800 грн бесплатно. Заказ меньше 800 грн оплачивается дополнительно 75 грн. Доставка Новой Почтой за счет покупателя.', reply_markup=keyboard)


# Handle user location input
@bot.message_handler(content_types=['location'])
def handle_geolocation(msg):
    keyboard = telebot.types.ReplyKeyboardMarkup()
    end = telebot.types.KeyboardButton('Закончить Заказ', request_contact=True)
    main = telebot.types.KeyboardButton('Главное Меню')
    keyboard.add(end, main)
    
    # Write user location to the DB
    db_mysql.write_geolocation(user_id=msg.chat.id, lat=msg.location.latitude, long=msg.location.longitude)
    bot.send_message(msg.chat.id, 'Ваш адрес был успешно добавлен в нашу систему!', reply_markup=keyboard)


# Handle user-inputted address
@bot.message_handler(regexp='На другой адрес')
def handle_adress(msg):
    bot.send_message(msg.chat.id, 'Введите адрес для доставки в формате: "УЛИЦА, НОМЕР ДОМА"')
    
@bot.message_handler(regexp='.+,?\s?\d+') # Regex for addresses
def accept_adress(msg):
    keyboard = telebot.types.ReplyKeyboardMarkup()
    end = telebot.types.KeyboardButton('Закончить Заказ', request_contact=True)
    main = telebot.types.KeyboardButton('Главное Меню')
    keyboard.add(end, main)
    
    # Write user address to DB
    db_mysql.write_adress(user_id=msg.chat.id, address=msg.text)
    bot.send_message(msg.chat.id, 'Ваш Адрес был успешно записан!', reply_markup=keyboard)


# Handle Самовывоз
@bot.message_handler(regexp='Самовывоз')
def self_deliv(msg):
    keyboard = telebot.types.ReplyKeyboardMarkup()
    end = telebot.types.KeyboardButton('Закончить Заказ', request_contact=True)
    main = telebot.types.KeyboardButton('Главное Меню')
    keyboard.add(end, main)
    
    # send our Location
    (lat, lon) = (50.496662, 30.470756)
    bot.send_message(msg.chat.id, 'Вы можете посетить наш склад по адресу ул. Марка Вовчка 14, г. Киев:', reply_markup=keyboard)
    bot.send_location(msg.chat.id, lat, lon)


@bot.message_handler(regexp="Новой Почтой")
def nova_pochta(msg):
    keyboard = telebot.types.ReplyKeyboardMarkup()
    end = telebot.types.KeyboardButton('Закончить Заказ', request_contact=True)
    main = telebot.types.KeyboardButton('Главное Меню')
    keyboard.add(end, main)
    
    bot.send_message(msg.chat.id, 'Доставка Новой Почтой за счет покупателя. Наш менеджер свяжется с вами.', reply_markup=keyboard)


others_dict = {
    'i1':'Стаканы однослойные',
    'i2':'Стаканы гофрированные',
    'i3':'Стаканы купольные',
    'i4':'Крышки',
    'i5':'Трубочки',
    'i6':'Сиропы',
    'i7':'Мешалки',
    'i8':'Салфетки',
    'i9':'Шоколад',
    'i10':'Какао',
    'main':'Главное Меню'
}


@bot.message_handler(regexp='Заказать другие товары для кофейни')
def other(msg):
    keyboard = telebot.types.ReplyKeyboardMarkup()
    main = telebot.types.KeyboardButton('Главное Меню')
    for key, value in others_dict.items():
        key = telebot.types.KeyboardButton(value)
        keyboard.add(key)
    keyboard.add(main)
    bot.send_message(msg.chat.id, 'У нас в наличии есть широкий ассортимент товаров для вашей кофейни. Выберите нужное из списка внизу.', reply_markup=keyboard)


# Handle adding one more of the product
@bot.message_handler(regexp='\+')
def added(msg):
    keyboard = telebot.types.ReplyKeyboardMarkup()
    main = telebot.types.KeyboardButton('Главное Меню')
    basket = telebot.types.KeyboardButton('Корзина')
    add = telebot.types.KeyboardButton('+')
    delete = telebot.types.KeyboardButton('-')
    keyboard.add(delete, add, main, basket)
    
    # Record to the DB
    db_mysql.add_one(user_id=msg.chat.id)
    tup = db_mysql.select_last(user_id=msg.chat.id) # Tuple (name, quantity, total)
    bot.send_message(msg.chat.id, 'Вы измененили кол-во товара: {} - {} грн. Количество: {}'.format(tup[0], tup[2], tup[1]), reply_markup=keyboard)
    

# Handle deleting one of the last product
@bot.message_handler(regexp='-')
def deleted(msg):
    keyboard = telebot.types.ReplyKeyboardMarkup()
    main = telebot.types.KeyboardButton('Главное Меню')
    basket = telebot.types.KeyboardButton('Корзина')
    add = telebot.types.KeyboardButton('+')
    delete = telebot.types.KeyboardButton('-')
    keyboard.add(delete, add, main, basket)
    
    # Record to the DB
    db_mysql.delete_one(user_id=msg.chat.id)
    tup = db_mysql.select_last(user_id=msg.chat.id) # Tuple (name, quantity, total)
    if tup[1] == 0:
        bot.send_message(msg.chat.id,'Товар был удален из вашего заказа.', reply_markup=keyboard)
    else:
        bot.send_message(msg.chat.id, 'Вы измененили кол-во товара: {} - {} грн. Количество: {}'.format(tup[0], tup[2], tup[1]), reply_markup=keyboard)    
        
        
# Handle going back to main menu
@bot.message_handler(regexp='Главное Меню')
def go_back_to_main(msg):
    keyboard = telebot.types.ReplyKeyboardMarkup()
    coffee = telebot.types.KeyboardButton('Заказать Кофе')
    milk = telebot.types.KeyboardButton('Заказать молоко')
    deliv = telebot.types.KeyboardButton('Доставка')
    other = telebot.types.KeyboardButton('Заказать другие товары для кофейни')
    end = telebot.types.KeyboardButton('Закончить Заказ', request_contact=True)
    keyboard.add(coffee, milk, deliv, other, end)
    
    bot.send_message(msg.chat.id, 'Вы вернулись в главное меню. Выберите что вы хотели бы заказать.', reply_markup=keyboard)

# Add Basket
@bot.message_handler(regexp='Корзина')
def show_order_basket(msg):
    keyboard = telebot.types.ReplyKeyboardMarkup()
    end = telebot.types.KeyboardButton('Закончить Заказ', request_contact=True)
    main = telebot.types.KeyboardButton('Главное Меню')
    keyboard.add(end, main)
    
    # Handle if the basket is empty
    if not db_mysql.list_order(user_id=msg.chat.id):
        bot.send_message(msg.chat.id, 'Ваша Корзина пустая!', reply_markup=keyboard)
    else:
        bot.send_message(msg.chat.id, 'Ваш Заказ:', reply_markup=keyboard)
    
        '''Need this code to get all lists in the generator object
        returned by list_order()'''
        for product in db_mysql.list_order(user_id=msg.chat.id):
            bot.send_message(msg.chat.id, '{} - {} грн. Количество: {}'.format(product[0].split(' (')[0], product[2], product[1]))
            
        # Count the total sum for all products in the basket
        total_sum = db_mysql.count_total(user_id=msg.chat.id)
        bot.send_message(msg.chat.id, 'Сумма вашего заказа: {} грн.'.format(total_sum[0]))


# End of the order
@bot.message_handler(content_types=['contact'])
def end_order(msg):
    phone_number=msg.contact.phone_number
    
    keyboard = telebot.types.ReplyKeyboardMarkup()
    main = telebot.types.KeyboardButton('Главное Меню')
    keyboard.add(main)
    
    # Record phone number into DB and Add pending order to the actual orders table
    db_mysql.write_phone(user_id=msg.chat.id, phone_number=phone_number)
    db_mysql.complete_order(user_id=msg.chat.id, phone_number=phone_number)
    
    bot.send_message(msg.chat.id, 'Спасибо за то, что воспользовались нашим ботом. Наш менеджер свяжется с вами через пару минут. До скорых встреч!', reply_markup=keyboard)
    
    
# Add possibility to clear the tables in DB
@bot.message_handler(commands=['new'])
def clear_tables(msg):
    keyboard = telebot.types.ReplyKeyboardMarkup()
    main = telebot.types.KeyboardButton('Главное Меню')
    keyboard.add(main)
    
    # Give admin access to required users
    if msg.from_user.id == '401482102': # Денис
        db_mysql.init_db(force=True)
        bot.send_message(msg.chat.id, 'Вы успешно обновили таблицы в Базе Данных!', reply_markup=keyboard)
        
    elif msg.from_user.id == '389802270': # Я
        db_mysql.init_db(force=True)
        bot.send_message(msg.chat.id, 'Вы успешно обновили таблицы в Базе Данных!', reply_markup=keyboard)
    else:
        bot.send_message(msg.chat.id, 'У вас нет доступа к данной команде!', reply_markup=keyboard)
        
        
bot.polling(none_stop=True)
