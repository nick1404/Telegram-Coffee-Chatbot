import telebot
import db_mysql
import config

# Initiate the bot
# token = '1152277849:AAH7nrOn2fqpL0ktVjSVpE9qUk9__M0oPWA'
bot = telebot.TeleBot(token=config.TOKEN)

#Connect to the database
db_mysql.init_db(force=True)

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

@bot.message_handler(regexp='Заказать кофе')
def choose_coffee(msg):
    keyboard = telebot.types.ReplyKeyboardMarkup()
    for key, value in coffee_dict.items():
        key = telebot.types.KeyboardButton(value)
        keyboard.add(key)
        
    bot.send_message(msg.chat.id, 'У нас в наличии зерновое кофе (100% Арабика) из множества стран. Закажите нужное вам кофе, нажав на кнопку.', reply_markup=keyboard)


# Loop through coffee dict to handle the buttons for each coffee
coffee_regex = "Бразилия Сантос \(250 грн - 1 кг\)|Эфиопия \(250 грн - 1кг\)|Колумбия Супремо \(300 грн - 1 кг\)|Гондурас \(300 грн - 1 кг\)|Сальвадор \(300 грн - 1 кг\)|Гватемала \(300 грн - 1 кг\)|70 арабики \+ 30 рабусты \(220 грн - 1 кг\)|50 арабики + 50 рабусты \(200 грн - 1 кг\)|30 арабики + 70 рабусты \(180 грн - 1 кг\)|Бурунди \(350 грн - 1 кг\)"
# coffee_regex = 'Бразилия\sСантос\s\(250\sгрн\s-\s1\sкг\)|Эфиопия\s\(250\sгрн\s-\s1\sкг\)|Колумбия\sСупремо\s\(300\sгрн\s-\s1\sкг\)|Гондурас\s\(300\sгрн\s-\s1\sкг\)|Сальвадор\s\(300\sгрн\s-\s1\sкг\)|Гватемала\s\(300\sгрн\s-\s1\sкг\)|70\sарабики\s\+\s30\sрабусты\s\(220\sгрн\s-\s1\sкг\)|50\sарабики\s\+\s50\sрабусты\s\(200\sгрн\s-\s1\sкг\)|30\sарабики\s\+\s70\sрабусты\s\(180\sгрн\s-\s1\sкг\)|Бурунди\s\(350\sгрн\s-\s1\sкг\)'
                                                       
@bot.message_handler(regexp=coffee_regex)
def coffee_purchase(msg):
    msg_text = msg.text.split(' (')[0]
    
    keyboard = telebot.types.ReplyKeyboardMarkup()
    # add = telebot.types.KeyboardButton('+')
    # delete = telebot.types.KeyboardButton('-')
    main = telebot.types.KeyboardButton('Главное Меню')
    basket = telebot.types.KeyboardButton('Корзина')
    keyboard.add(main, basket)#, delete, add)
    
    # Access the name and price of the good in the DB
    name_price = db_mysql.access_price_list(name=msg.text)
    
    bot.send_message(msg.chat.id, 'Вы выбрали кофе {}. Вы можете изменить количество с помощью кнопок + и -.'.format(msg_text), reply_markup=keyboard)
    
    # Add order to the database
    db_mysql.add_order(user_id=msg.chat.id, name=name_price[0], quantity=1, price=name_price[1]) # Add quantity controls


milk_dict = {
    'gal':'Галичина (900гр, 2,5%) - 285 грн/ящик',
    'sel':'Селянское (900гр, 2,5%) - 285 грн/ящик',
    'bar':'Бариста ТМ Галичина (1л, 2,5%) - 252 грн/ящик',
    'nez':'Нежинское (1л, 2,5%) - 252 грн/ящик',
    'alpro':'Молоко безлактозное Alpro - 90 грн/л',
    'main':'Главное Меню'
}

@bot.message_handler(regexp='Заказать молоко')
def choose_milk(msg):
    keyboard = telebot.types.ReplyKeyboardMarkup()
    for key, value in milk_dict.items():
        key = telebot.types.KeyboardButton(value)
        keyboard.add(key)

    bot.send_message(msg.chat.id, 'Вы можете заказать нужное вам молоко нажав на кнопки внизу.', reply_markup=keyboard)


# milk_regex = 'Галичина\s\(900гр,\s2,5\%\)\s-\s285\sгрн\/ящик|Селянское\s\(900гр,\s2,5\%\)\s-\s285\sгрн\/ящик|Бариста\sТМ\sГаличина\s\(1л,\s2,5\%\)\s-\s252\sгрн\/ящик|Нежинское\s\(1л,\s2,5%\)\s-\s252\sгрн\/ящик|Молоко\sбезлактозное\sAlpro\s90\sгрн/\л)'
milk_regex = 'Галичина \(900гр, 2,5\%\) - 285 грн\/ящик|Селянское \(900гр, 2,5\%\) - 285 грн\/ящик|Бариста ТМ Галичина \(1л, 2,5\%\) - 252 грн\/ящик|Нежинское \(1л, 2,5%\) - 252 грн\/ящик|Молоко безлактозное Alpro 90 грн/\л'


@bot.message_handler(regexp=milk_regex)
def milk_purchase(msg):
    msg_text = msg.text.split(' -')[0]
    keyboard = telebot.types.ReplyKeyboardMarkup()
    main = telebot.types.KeyboardButton('Главное Меню')
    basket = telebot.types.KeyboardButton('Корзина')
    
    # Access the name and price of the good in the DB   
    name_price = db_mysql.access_price_list(name=msg.text)

    keyboard.add(main, basket)
    bot.send_message(msg.chat.id, 'Вы выбрали {}. Вы можете изменить количество с помощью кнопок + и -.'.format(msg_text), reply_markup=keyboard)

    # Add the order to the DB
    db_mysql.add_order(user_id=msg.chat.id, name=name_price[0], quantity=1, price=name_price[1]) # Add quantity controls


@bot.message_handler(regexp='Доставка')
def delivery(msg):
    keyboard = telebot.types.ReplyKeyboardMarkup()
    address = telebot.types.KeyboardButton("Доставка по адресу", request_location=True) #Need to store the location somewhere
    post = telebot.types.KeyboardButton("Доставка Новой Почтой")
    drive = telebot.types.KeyboardButton('Самовывоз')
    main = telebot.types.KeyboardButton('Главное Меню')
    
    keyboard.add(address, post, main, drive)
    bot.send_message(msg.chat.id, 'Вы можете заказать доставку до 9 утра (День в День). Доставка по Киеву от 800 грн бесплатно. Заказ меньше 800 грн оплачивается дополнительно 75 грн. Доставка Новой Почтой за счет покупателя.', reply_markup=keyboard)


# Handle user location input
@bot.message_handler(content_types=['location'])
def handle_location(msg):
    keyboard = telebot.types.ReplyKeyboardMarkup()
    end = telebot.types.KeyboardButton('Закончить Заказ')
    main = telebot.types.KeyboardButton('Главное Меню')
    keyboard.add(end, main)
    
    # Write user location to the DB
    db_mysql.write_location(user_id=msg.chat.id, lat=msg.location.latitude, long=msg.location.longitude)
    bot.send_message(msg.chat.id, 'Ваш адрес был успешно добавлен в нашу систему!', reply_markup=keyboard)


# Handle Самовывоз
@bot.message_handler(regexp='Самовывоз')
def self_deliv(msg):
    keyboard = telebot.types.ReplyKeyboardMarkup()
    end = telebot.types.KeyboardButton('Закончить Заказ')
    main = telebot.types.KeyboardButton('Главное Меню')
    keyboard.add(end, main)
    
    # send our Location
    (lat, lon) = (50.496662, 30.470756)
    bot.send_message(msg.chat.id, 'Вы можете посетить наш склад по адресу ул. Марка Вовчка 14, г. Киев:', reply_markup=keyboard)
    bot.send_location(msg.chat.id, lat, lon)
    
    #Request username
    username = msg.from_user.username
    db_mysql.write_username(user_id=msg.chat.id, username=username)


@bot.message_handler(regexp="Доставка Новой Почтой")
def nova_pochta(msg):
    keyboard = telebot.types.ReplyKeyboardMarkup()
    end = telebot.types.KeyboardButton('Закончить Заказ')
    main = telebot.types.KeyboardButton('Главное Меню')
    keyboard.add(end, main)
    
    bot.send_message(msg.chat.id, 'Доставка Новой Почтой за счет покупателя. Наш менеджер свяжется с вами.', reply_markup=keyboard)
    #Request username
    username = msg.from_user.username
    db_mysql.write_username(user_id=msg.chat.id, username=username)


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


# Handle going back to main menu
@bot.message_handler(regexp='Главное Меню')
def go_back_to_main(msg):
    keyboard = telebot.types.ReplyKeyboardMarkup()
    coffee = telebot.types.KeyboardButton('Заказать Кофе')
    milk = telebot.types.KeyboardButton('Заказать молоко')
    deliv = telebot.types.KeyboardButton('Доставка')
    other = telebot.types.KeyboardButton('Заказать другие товары для кофейни')
    end = telebot.types.KeyboardButton('Закончить Заказ')
    keyboard.add(coffee, milk, deliv, other, end)
    
    bot.send_message(msg.chat.id, 'Вы вернулись в главное меню. Выберите что вы хотели бы заказать.', reply_markup=keyboard)

# Add Basket
@bot.message_handler(regexp='Корзина')
def show_order_basket(msg):
    keyboard = telebot.types.ReplyKeyboardMarkup()
    end = telebot.types.KeyboardButton('Закончить Заказ')
    main = telebot.types.KeyboardButton('Главное Меню')
    keyboard.add(end, main)
    
    bot.send_message(msg.chat.id, 'Ваш Заказ:', reply_markup=keyboard)
    
    '''Need this code to get all lists in the generator object
   returned by list_order()'''
    for product in db_mysql.list_order(user_id=msg.chat.id):
        bot.send_message(msg.chat.id, '{} - {} грн. Количетсво: {}'.format(product[0], product[2], product[1]))


@bot.message_handler(regexp='Закончить Заказ')
def end_order(msg):
    bot.send_message(msg.chat.id, 'Спасибо за то, что воспользовались нашим ботом. Наш менеджер свяжется с вами через пару минут. До скорых встреч!')
    exit() # Terminate program
    # Add method that deletes orders from the db??
    
    
bot.polling(none_stop=True)