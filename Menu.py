import types
from datetime import datetime

import telegram.inline.inlinekeyboardmarkup
from telegram import *
from telegram.ext import *


# menu prices
item_list = ['Chicken Pakodi', 'Roasted Chicken', 'Mix Platters', 'Chicken Steak', 'Chicken Steak Kebab', 'Fish Steak',
             'Chicken Mandi', 'Mutton Mandi', 'Fish Mandi', 'Veg Mandi', 'Gulab Jamun', 'Quarbani Ka Meetha',
             'Double Ka Meetha',
             'Chicken Mandi, Chicken Stick Kebab, Coke', 'Chicken Mandi, Fish , Coke',
             'Mutton Mandi, Chicken Pakodi, Coke',
             'Mutton Mandi, Chicken Steak, Fish', 'Chicken Mandi, Fish Steak, Roasted Chicken',
             'Fish Mandi, Roasted Chicken, Coke',
             'Fish Mandi, Chicken Pakodi, Coke', 'Mayonnaise', 'Fried Onions', 'Mandi Rice', 'Chicken', 'Mutton',
             'Fish', 'Fruit Punch',
             'Watermelon Cooler', 'Lichi Sparkel', 'Vargin Mojito', 'Juicy Mutton Mandi', 'Raan Mandi',
             'Jumbo Mutton Mandi',
             'Juicy Mutton Curry', 'Arabina Heleem', 'Basbousa', 'Cucumber Mint', 'Coco Colada', 'Kiwi Punch',
             'Ambur Mandi',
             'Juicy Chicken Mandi', 'Fish Fry', 'Hummus', 'Blue Star']


# displays the three options.
def random(update: Update, context: CallbackContext) -> None:
    # inputting the options in the buttons.
    reply_buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("Menu", callback_data="menu")],
        [InlineKeyboardButton("Inquires", callback_data='inquiry')]
    ])

    # sends the message with three option buttons attached.
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hi there, please choose an option",
                             reply_markup=reply_buttons)


def inquiries(update: Update, context: CallbackContext):
    reply_buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton('Store Address', callback_data='store_address')],
        [InlineKeyboardButton('Customer care Number', callback_data='customer_care_number')],
        [InlineKeyboardButton('Store Open Timings', callback_data='open_timings')],
        [InlineKeyboardButton('Online Delivery Time', callback_data='delivery_time')],
        [InlineKeyboardButton('Pick-Up Time', callback_data='pickup-time')]
    ])
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hi there, please choose an option",
                             reply_markup=reply_buttons)


def menu(update: Update, context: CallbackContext) -> None:
    day = datetime.today().strftime('%A')
    linespace = '\t \t'

    default_or_not(update, context)

    context.bot.sendPhoto(chat_id=update.effective_chat.id, photo=open('images/dailymenu.png', 'rb'))
    if day == 'Monday':
        context.bot.sendPhoto(chat_id=update.effective_chat.id, photo=open('images/friday.png', 'rb'))
    elif day == 'Sunday':
        context.bot.sendPhoto(chat_id=update.effective_chat.id, photo=open('images/sunday.png', 'rb'))

    menu_list = InlineKeyboardMarkup(
        [[InlineKeyboardButton('P1', callback_data='Chicken Pakodi'),
          InlineKeyboardButton('P2', callback_data='Chicken Pakodi'),
          InlineKeyboardButton('P3', callback_data='Mix Platters'),
          InlineKeyboardButton('P4', callback_data='Chicken Steak'),
          InlineKeyboardButton('P5', callback_data='Chicken Steak Kebab'),
          InlineKeyboardButton('P6', callback_data='Fish Steak')],

         [InlineKeyboardButton("R1", callback_data='Chicken Mandi'),
          InlineKeyboardButton("R2", callback_data='Mutton Mandi'),
          InlineKeyboardButton("R3", callback_data='Fish Mandi'),
          InlineKeyboardButton("R4", callback_data='Fish Mandi')],

         [InlineKeyboardButton('T1', callback_data='Gulab Jamun'),
          InlineKeyboardButton('T2', callback_data='Quarbani Ka Meetha'),
          InlineKeyboardButton('T3', callback_data='Double Ka Meetha'),
          InlineKeyboardButton('T4', callback_data='Fruit Punch'),
          InlineKeyboardButton('T5', callback_data='Watermelon Cooler'),
          InlineKeyboardButton('T6', callback_data='Lichi Sparkel'),
          InlineKeyboardButton('T7', callback_data='Vargin Mojito')],

         [InlineKeyboardButton('O1', callback_data='Chicken Mandi, Chicken Stick Kebab, Coke'),
          InlineKeyboardButton('O2', callback_data='Chicken Mandi, Fish , Coke'),
          InlineKeyboardButton('O3', callback_data='Mutton Mandi, Chicken Pakodi, Coke'),
          InlineKeyboardButton('O4', callback_data='Mutton Mandi, Chicken Steak, Fish'),
          InlineKeyboardButton('O5', callback_data='Chicken Mandi, Fish Steak, Roasted Chicken'),
          InlineKeyboardButton('O6', callback_data='Fish Mandi, Roasted Chicken, Coke'),
          InlineKeyboardButton('O7', callback_data='Fish Mandi, Chicken Pakodi, Coke')],

         [InlineKeyboardButton("M1", callback_data='Mandi Rice'),
          InlineKeyboardButton("M2", callback_data='Chicken'),
          InlineKeyboardButton("M3", callback_data='Mutton'),
          InlineKeyboardButton("M4", callback_data='Fish')],

         [InlineKeyboardButton("A1", callback_data='Mayonnaise'),
          InlineKeyboardButton("A2", callback_data='Fried Onions')],

         [InlineKeyboardButton("Back", callback_data='back')]
         ])

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f'Press the code button to add the item to cart:',
                             reply_markup=menu_list)

    if day == "Friday":
        friday_specials = InlineKeyboardMarkup([[InlineKeyboardButton("F1", callback_data='Juicy Mutton Mandi'),
                                                 InlineKeyboardButton("F2", callback_data='Raan Mandi'),
                                                 InlineKeyboardButton("F3", callback_data='Jumbo Mutton Mandi'),
                                                 InlineKeyboardButton("F4", callback_data='Juicy Mutton Curry'),
                                                 InlineKeyboardButton("F5", callback_data='Arabina Heleem'),
                                                 InlineKeyboardButton("F6", callback_data='Basbousa')],
                                                [InlineKeyboardButton("F7", callback_data='Cucumber Mint'),
                                                 InlineKeyboardButton("F8", callback_data='Coco Colada'),
                                                 InlineKeyboardButton("F9", callback_data='Kiwi Punch')]])

        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=f'Friday Specials',
                                 reply_markup=friday_specials)

    elif day == 'Sunday':
        sunday_specials = InlineKeyboardMarkup([[InlineKeyboardButton("S1", callback_data='Ambur Mandi'),
                                                 InlineKeyboardButton("S2", callback_data='Juicy Chicken Mandi'),
                                                 InlineKeyboardButton("S3", callback_data='Fish Fry'),
                                                 InlineKeyboardButton("S4", callback_data='Juicy Mutton Curry'),
                                                 InlineKeyboardButton("S5", callback_data='Arabina Heleem'),
                                                 InlineKeyboardButton("S6", callback_data='Hummus')],
                                                [InlineKeyboardButton("S7", callback_data='Blue Star'),
                                                 InlineKeyboardButton("S8", callback_data='Coco Colada'),
                                                 InlineKeyboardButton("S9", callback_data='Kiwi Punch')]])

        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=f'Sunday Specials',
                                 reply_markup=sunday_specials)
'''

def specials(update: Update, context: CallbackContext) -> None:
    day = datetime.today().strftime('%A')
    daily_specials = []
    line_space = '\t \t'

    if day == "Sunday":
        daily_specials = InlineKeyboardMarkup(
            [[InlineKeyboardButton(f"BBQ/Fahm Dajaj {line_space} ₹{item_list.get('fahm dajaj')}",
                                   callback_data='fahm dajaj')],
             [InlineKeyboardButton(f"Steak Dajaj {line_space} ₹{item_list.get('steak dajaj')}",
                                   callback_data="steak dajaj")],
             [InlineKeyboardButton(f"Breaded Dajaj {line_space} ₹{item_list.get('breaded dajaj')}",
                                   callback_data="breaded dajaj")],
             [InlineKeyboardButton("Back", callback_data='back')]])
    elif day == "Monday":
        daily_specials = InlineKeyboardMarkup(
            [[InlineKeyboardButton(f"Arabic Special Fish {line_space} ₹{item_list.get('Arabic Special Fish')}",
                                   callback_data='Arabic Special Fish')],
             [InlineKeyboardButton(f"Arabic Fish Mandi-Mini {line_space} ₹{item_list.get('Arabic Fish Mandi-Mini')}",
                                   callback_data="Arabic Fish Mandi-Mini")],
             [InlineKeyboardButton(f"Arabic Fish Mandi-Full {line_space} ₹{item_list.get('Arabic Fish Mandi-Full')}",
                                   callback_data="Arabic Fish Mandi-Full")],
             [InlineKeyboardButton(f"Chicken Wings {line_space} ₹{item_list.get('Chicken Wings')}",
                                   callback_data="Chicken Wings")],
             [InlineKeyboardButton("Back", callback_data='back')]])
    elif day == "Tuesday":
        daily_specials = InlineKeyboardMarkup(
            [[InlineKeyboardButton(f"Chilli Chicken {line_space} ₹{item_list.get('Chilli Chicken')}",
                                   callback_data='Chilli Chicken')],
             [InlineKeyboardButton(f"Butter Garlic Chicken {line_space} ₹{item_list.get('Butter Garlic Chicken')}",
                                   callback_data="Butter Garlic Chicken")],
             [InlineKeyboardButton(f"Chicken Tikka {line_space} ₹{item_list.get('Chicken Tikka')}",
                                   callback_data="Chicken Tikka")],
             [InlineKeyboardButton("Back", callback_data='back')]])
    elif day == "Thursday":
        daily_specials = InlineKeyboardMarkup(
            [[InlineKeyboardButton(
                f"Arabic Mutton Juicy Mandi-mini {line_space} ₹{item_list.get('Arabic Mutton Juicy Mandi-mini')}",
                callback_data='Arabic Mutton Juicy Mandi-mini')],
                [InlineKeyboardButton(
                    f"Arabic Mutton Juicy Mandi-Full {line_space} ₹{item_list.get('Arabic Mutton Juicy Mandi-full')}",
                    callback_data="Arabic Mutton Juicy Mandi-full")],
                [InlineKeyboardButton(
                    f"Arabic Mutton Fry Mandi-mini {line_space} ₹{item_list.get('Arabic Mutton Fry Mandi-mini')}",
                    callback_data="Arabic Mutton Fry Mandi-mini")],
                [InlineKeyboardButton(
                    f"Arabic Mutton Fry Mandi-Full {line_space} ₹{item_list.get('Arabic Mutton Fry Mandi-full')}",
                    callback_data="Arabic Mutton Fry Mandi-full")],
                [InlineKeyboardButton(
                    f"Mutton Hand Piece Mandi-Full {line_space} ₹{item_list.get('mutton hand piece mandi')}",
                    callback_data="mutton hand piece mandi")],
                [InlineKeyboardButton("Back", callback_data='back')]])
    elif day == "Wednesday":
        daily_specials = InlineKeyboardMarkup(
            [[InlineKeyboardButton(f'Arabic Mixed Mandi-Full {line_space} ₹{item_list.get("Arabic Mixed Mandi")}',
                                   callback_data='Arabic Mixed Mandi')],
             [InlineKeyboardButton(f'Roasted Chicken {line_space} ₹{item_list.get("Roasted Chicken")}',
                                   callback_data="Roasted Chicken")],
             [InlineKeyboardButton(f'Mixed Veg Mandi-Mini {line_space} ₹{item_list.get("Mixed Veg Mandi")}',
                                   callback_data="Mixed Veg Mandi")],
             [InlineKeyboardButton("Back", callback_data='back')]])
    elif day == "Friday":
        daily_specials = InlineKeyboardMarkup(
            [[InlineKeyboardButton(f"Dajaj BBQ Mandi-Mini  {line_space} ₹{item_list.get('Dajaj BBQ Mandi-Mini')}",
                                   callback_data='Dajaj BBQ Mandi-Mini')],
             [InlineKeyboardButton(f"Dajaj BBQ Mandi-Full  {line_space} ₹{item_list.get('Dajaj BBQ Mandi-Full')}",
                                   callback_data='Dajaj BBQ Mandi-Full')],
             [InlineKeyboardButton(f"Dajaj Fahm Mandi-Mini  {line_space} ₹{item_list.get('Dajaj Fahm Mandi-Mini')}",
                                   callback_data="Dajaj Fahm Mandi-Mini")],
             [InlineKeyboardButton(f"Dajaj Fahm Mandi-Full  {line_space} ₹{item_list.get('Dajaj Fahm Mandi-Full')}",
                                   callback_data="Dajaj Fahm Mandi-Full")],
             [InlineKeyboardButton(
                 f"Dajaj Streak Mandi-Mini {line_space} ₹{item_list.get('Dajaj Streak Mandi-Mini')}",
                 callback_data="Dajaj Streak Mandi-Mini")],
             [InlineKeyboardButton(
                 f"Dajaj Streak Mandi-Full {line_space} ₹{item_list.get('Dajaj Streak Mandi-Full')}",
                 callback_data="Dajaj Streak Mandi-Full")],
             [InlineKeyboardButton("Back", callback_data='back')]])
    elif day == "Saturday":
        daily_specials = InlineKeyboardMarkup(
            [[InlineKeyboardButton(f"Dajaj Tikka Mandi-Mini {line_space} ₹{item_list.get('Dajaj Tikka Mandi-Mini')}",
                                   callback_data='Dajaj Tikka Mandi-Mini')],
             [InlineKeyboardButton(f"Dajaj Tikka Mandi-Full {line_space} ₹{item_list.get('Dajaj Tikka Mandi-Full')}",
                                   callback_data="Dajaj Tikka Mandi-Full")],
             [InlineKeyboardButton(f"Dajaj Wings Mandi-Mini {line_space} ₹{item_list.get('Dajaj Wings Mandi-Mini')}",
                                   callback_data="Dajaj Wings Mandi-Mini")],
             [InlineKeyboardButton(f"Dajaj Wings Mandi-Full {line_space} ₹{item_list.get('Dajaj Wings Mandi-Full')}",
                                   callback_data="Dajaj Wings Mandi-Full")],
             [InlineKeyboardButton(f"Healthy Mutton Soup {line_space} ₹{item_list.get('Healthy Mutton Soup')}",
                                   callback_data="Healthy Mutton Soup")],
             [InlineKeyboardButton("Back", callback_data='back')]])

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f'{day} Specials: ',
                             reply_markup=daily_specials)
'''


def prices(item):
    item_prices = {}
    with open("temp_menuitems.txt") as f:
        for line in f:
            (k, v) = line.replace(':', ':').replace('-', ':').split(':')
            item_prices[k] = float(v)

    return item_prices[item]


def default_or_not(update: Update, context: CallbackContext):
    item_prices = {}
    with open("temp_menuitems.txt") as f:
        for line in f:
            (k, v) = line.replace(':', ':').replace('-', ':').split(':')
            item_prices[k] = float(v)

    if 0 in item_prices.values():
        update.message.reply_text("Try your Luck🎯!!!.... Few items are will be handover-ed without any bill")
    else:
        pass




