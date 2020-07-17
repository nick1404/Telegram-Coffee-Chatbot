import telebot
import db

# Initiate the bot
token = '1152277849:AAH7nrOn2fqpL0ktVjSVpE9qUk9__M0oPWA'
bot = telebot.TeleBot(token=token)

#Connect to the database
db.init_db()

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
    add = telebot.types.KeyboardButton('+')
    delete = telebot.types.KeyboardButton('-')
    main = telebot.types.KeyboardButton('Главное Меню')
    basket = telebot.types.KeyboardButton('Корзина')
    keyboard.add(main, basket, delete, add)
    
    # Access the name and price of the good in the DB
    name_price = db.access_price_list(name=msg.text)
    
    bot.send_message(msg.chat.id, 'Вы выбрали кофе {}. Вы можете изменить количество с помощью кнопок + и -.'.format(msg_text), reply_markup=keyboard)
    
    # Add order to the database
    db.add_order(user_id=msg.chat.id, name=name_price[0], quantity=1, price=name_price[1]) # Add quantity controls

# @bot.callback_query_handler(func=lambda call: True)
# def callback_query(call):
milk_dict = {
    'gal':'Галичина (900гр, 2,5%) - 285 грн/ящик',
    'sel':'Селянское (900гр, 2,5%) - 285 грн/ящик',
    'bar':'Бариста ТМ Галичина (1л, 2,5%) - 252 грн/ящик',
    'nez':'Нежинское (1л, 2,5%) - 252 грн/ящик',
    'alpro':'Молоко безлактозное Alpro 90 грн/л',
    'main':'Главное Меню'
}

@bot.message_handler(regexp='Заказать молоко')
def choose_milk(msg):
    keyboard = telebot.types.ReplyKeyboardMarkup()
    for key, value in milk_dict.items():
        key = telebot.types.KeyboardButton(value)
        keyboard.add(key)

    bot.send_message(msg.chat.id, 'Вы можете заказать нужное вам молоко нажав на кнопки внизу.', reply_markup=keyboard)


# milk_regex = 'Галичина\s\(900гр,\s2,5\%\)\s-\s285\sгрн/ящик|Селянское\s\(900гр,\s2,5\%\)\s-\s285\sгрн/ящик|Бариста\sТМ\sГаличина\s\(1л,\s2,5\%\)\s-\s252\sгрн/ящик|Нежинское\s\(1л,\s2,5%\)\s-\s252\sгрн/ящик|Молоко\sбезлактозное\sAlpro\s90\sгрн/л)'

# @bot.message_handler(regexp=milk_regex)
# def milk_purchase(msg):
#     msg_text = msg.text.split(' -')[0]
#     keyboard = telebot.types.ReplyKeyboardMarkup()
#     buy = telebot.types.KeyboardButton('Купить')
#     main = telebot.types.KeyboardButton('Главное Меню')
    
#     # Access the name and price of the good in the DB   
#     name_price = db.access_price_list(name=msg_text)

#     keyboard.add(buy, main)
#     bot.send_message(msg.chat.id, 'Вы выбрали {}. Вы можете изменить количество с помощью кнопок + и -.'.format(msg_text), reply_markup=keyboard)

#     # Add the order to the DB
#     db.add_order(user_id=msg.chat.id, name=name_price[0], quantity=1, price=name_price[1]) # Add quantity controls


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
@bot.message_handler(regexp="Доставка по адресу")
def deliver(msg):
    pass


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
    for key, value in others_dict.items():
        key = telebot.types.KeyboardButton(value)
        keyboard.add(key)
    
    bot.send_message(msg.chat.id, 'У нас в наличии есть широкий ассортимент товаров для вашей кофейни. Выберите нужное из списка внизу.', reply_markup=keyboard)

# Handle going back to main menu
@bot.message_handler(regexp='Главное Меню')
def go_back_to_main(msg):
    keyboard = telebot.types.ReplyKeyboardMarkup()
    coffee = telebot.types.KeyboardButton('Заказать Кофе')
    milk = telebot.types.KeyboardButton('Заказать молоко')
    deliv = telebot.types.KeyboardButton('Доставка')
    other = telebot.types.KeyboardButton('Заказать другие товары для кофейни')
    keyboard.add(coffee, milk, deliv, other)
    
    bot.send_message(msg.chat.id, 'Вы вернулись в главное меню. Выберите что вы хотели бы заказать.', reply_markup=keyboard)

# Add Basket
@bot.message_handler(regexp='Корзина')
def show_order_basket(msg):
    bot.send_message(msg.chat.id, 'Ваш Заказ:')
    
    '''Need this code to get all lists in the generator object
   returned by list_order()'''
    for product in db.list_order(user_id=msg.chat.id):
        bot.send_message(msg.chat.id, '{} - {} грн.'.format(product[0], product[1]))
    
bot.polling(none_stop=True)