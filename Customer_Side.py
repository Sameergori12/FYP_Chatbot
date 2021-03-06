# importing the telegram bot
import logging

import telegram
from telegram import *
from telegram.ext import *

import re
import io
# to know the date and time
import datetime

# importing the token
from key import *

import emoji

from geopy.geocoders import Nominatim
from geopy import distance

# necessary variables, def's  from menu
from Menu import random, menu, item_list, prices, inquiries

TOKEN = Token
print("Customer bot started...")
cart_dict = {}
Location = ''
Order_type = ''
pNumber = ''

session_started = False

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)
print("cation 📍 Just like this:")


def start(update: Update, context: CallbackContext):
    user = update.message.from_user
    logger.info("User %s has started the Session chat_id: %s", user.first_name, update.message.from_user.id)
    update.message.reply_text(text="I can help you place and manage your order. Below commands will guide you \n \n"
                                   "You can control me by sending these commands: \n \n"
                                   "/start_session - starts the session \n"
                                   "/cart - shows the cart items \n"
                                   "/delete [item_no] - enter number of item \n"
                                   "/feedback [Enter the feedback] - to submit the feedback\n"
                                   "/checkout - check out of the session and place order\n")


# user should choose an option among three (Menu, Day to Day Specials, Inquires)
def menu_list(update: Update, context: CallbackContext):
    start_session = True
    currentTime = datetime.datetime.now().time()
    f = open("maintenance.txt", 'r+')
    content = f.read()
    if content == 'Maintenance':
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Bot is under Maintenance. Sorry for the inconvenience")
    elif len(content) == 0:
        if time_in_range(currentTime):
            reply_buttons = InlineKeyboardMarkup([
                [InlineKeyboardButton("Online Delivery", callback_data="Online")],
                [InlineKeyboardButton("Pickup", callback_data='Pickup')]
            ])

            # sends the message with three option buttons attached.
            context.bot.send_message(chat_id=update.effective_chat.id, text="Hi there, please choose your order type.",
                                     reply_markup=reply_buttons)
        else:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text="Sorry we are closed for orders. You can make orders from \n"
                                          "10AM - 10PM everyday. Thank you and visit again.")


def time_in_range(current):
    # Returns whether current is in the range [start, end]
    start = datetime.time(10, 0, 0)
    end = datetime.time(23, 30, 0)
    return start <= current <= end

    return start <= current <= end


# displays the cart list
def cart_list(update: Update, context: CallbackContext):
    user = update.message.from_user
    logger.info("User %s is in the cart", user.first_name)
    # "cart is empty" will be displayed if nothing in the cart
    if len(cart_dict) == 0:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Cart is empty")
    else:
        # calling the organize method to get the cart organized to display format
        car, order_amt = organize()
        line_space = '\n'
        stir = ' \n'.join(car)
        stir += "\n \n" + "Total amount: " + "\t     ₹" + str(order_amt)
        # cart list will be displayed in the bot
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Your Cart: {line_space}{stir}")


# to delete the item from cart
def delete(update: Update, context: CallbackContext):
    user = update.message.from_user
    # getting the text from the user
    delete_item = update.message.text
    # finding the number to delete
    item_no = delete_item[7:].strip()
    logger.info("User %s wants to delete", user.first_name)

    # checking if it's numeric or not
    if item_no.isnumeric():
        # if numeric and below the length of cart list - deleting the item
        if len(cart_dict) >= int(item_no) >= 1:
            li = list(cart_dict.keys())
            # deleting the item from the cart
            del cart_dict[li[int(item_no) - 1]]
            # displaying the deleted message
            context.bot.send_message(chat_id=update.effective_chat.id, text="item has been deleted from your cart.")
        # if intent number is beyond the cart length
        elif int(item_no) >= len(cart_dict) or int(item_no) == 0:
            # if the cart length is 0
            if len(cart_dict) == 0:
                # displaying the cart is empty - no items
                context.bot.send_message(chat_id=update.effective_chat.id, text="Your cart is empty!!")
            # if the inputted number is beyond
            else:
                # displaying the user to check their input.
                context.bot.send_message(chat_id=update.effective_chat.id,
                                         text="your input is wrong. please check your input.")
    # if the command is not clear. Displaying the correct format
    elif type(item_no) == str or len(item_no) == 0:
        context.bot.send_message(chat_id=update.effective_chat.id, text="your command is unclear. please try to be "
                                                                        "clear.\n "
                                                                        "No item number present\n"
                                                                        "format is /delete [your item Number] \n"
                                                                        "Example: /delete 1 - will delete the 1st "
                                                                        "item from your cart")


# will be triggered on entering queries or to solve them.
def action(update: Update, context: CallbackContext):
    global Order_type, pNumber, Location
    # getting the text from the bot.
    update.callback_query.answer()
    choice = update.callback_query.data

    # if the text is menu, calling the menu
    if choice == "menu":
        update.callback_query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup([]))
        menu(update, context)
    # if the text is from the menu items, adding the item to the cart
    elif choice in item_list:
        if choice in cart_dict:
            cart_dict.update({choice: (int(cart_dict.get(choice)) + 1)})
        else:
            cart_dict.update({choice: 1})
        context.bot.send_message(chat_id=update.effective_chat.id, text="added to the cart")
    # if the text is back, going back to random
    elif choice == "back":
        update.callback_query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup([]))
        random(update, context)
    elif choice == 'no':
        context.bot.send_message(chat_id=update.effective_chat.id, text="Ok")
    elif choice == 'inquiry':
        inquiries(update, context)
    elif choice == 'store_address':
        context.bot.send_message(chat_id=update.effective_chat.id, text="Gismat restaurants, 1st floor,"
                                                                        "1217/A Shreshtra Aura,RoadNo-36,"
                                                                        "Jubilee Hills, Hyderabad,"
                                                                        "Telangana- 5000033, INDIA")
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="This is the store Location: https://maps.app.goo.gl/5NofNcVCg7jLaM4t6")
    elif choice == 'customer_care_number':
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="You can contact +91 7075234341 for any inquiries")
    elif choice == 'open_timings':
        context.bot.send_message(chat_id=update.effective_chat.id, text="Store Timings - 10:00 AM to 11:00 PM\n"
                                                                        "Bot Order Timings - 10:00 AM to 10:00 PM")
    elif choice == "delivery_time":
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="You will receive your order within 35-40 mins from ordered time.")
    elif choice == "pickup-time":
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="You can collect the after 20-25 mins from ordered time.")
    elif choice == "Pickup":
        Order_type = 'Pickup'
        random(update, context)
    elif choice == "Online":
        Order_type = 'Online'
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="please type in your location coordinates using /locate (lat),(long) using this format.")
    elif choice == "change_Pickup":
        Order_type = 'Pickup'
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Your Order type has been successfully updated to Pickup.")
    elif choice == "change_Online":
        Order_type = 'Online'
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Your Order type has been successfully updated to Online Delivery.")
    elif choice == 'Yes_checkout':
        if len(cart_dict) == 0:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Cart is empty")
        else:
            with io.open('orders.txt', "a", encoding="utf-8") as f:

                if len(pNumber) == 0:
                    context.bot.send_message(chat_id=update.effective_chat.id,
                                             text="Sorry! you cannot checkout without providing your phone number")

                elif  len(Order_type) == 0:
                    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry! you cannot checkout without choosing your order type")
                    changeOrderType(update, context)

                elif Order_type == 'Pickup':
                    car, order_amt = organize()
                    stir = f'Name: {update.effective_user.full_name} \n' \
                           f'phone Number: {pNumber} \n' \
                           f'Order type: {Order_type}\n'
                    stir += ' \n'.join(car)
                    stir += "\n \n" + "Total amount: " + "\t     ₹" + str(order_amt)
                    f.write(stir)
                    f.write("\n####\n")
                    f.close()
                    cart_dict.clear()
                    context.bot.send_message(chat_id=update.effective_chat.id, text="Your Meal is on the way.\n"
                                                                                    "PickUp Location: https://maps.app.goo.gl/5NofNcVCg7jLaM4t6")

                elif Order_type == 'Online':
                    if not len(Location) == 0:
                        car, order_amt = organize()
                        stir = f'Name: {update.effective_user.full_name} \n' \
                               f'Location: {Location} \n' \
                               f'phone Number: {pNumber} \n' \
                               f'Order type: {Order_type}\n'
                        stir += ' \n'.join(car)
                        stir += "\n \n" + "Total amount: " + "\t     ₹" + str(order_amt)
                        f.write(stir)
                        f.write("\n####\n")
                        f.close()
                        cart_dict.clear()
                        context.bot.send_message(chat_id=update.effective_chat.id, text="Your Meal is on the way.")
                    else:
                        context.bot.send_message(chat_id=update.effective_chat.id,
                                                 text="Sorry! you cannot checkout providing your delivery coordinates.")
                    clear(update, context)

    elif choice == 'No_checkout':
        context.bot.send_message(chat_id=update.effective_chat.id, text="Checked Out")
        clear(update, context)

    elif choice == 'cancel':
        context.bot.send_message(chat_id=update.effective_chat.id,text = 'Your order has been successfully cancelled.')
        clear(update,context)
    # if input is anything beyond the above choices, asking the user regarding their problem.
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="What's your problem")


def clear(update: Update, context: CallbackContext):
    global pNumber, Location, Order_type

    pNumber = ''
    Location = ''
    Order_type = ''
    cart_dict.clear()



def phoneNumber(update: Update, context: CallbackContext):
    global pNumber

    user_message = update.message.from_user
    user_number = update.effective_message.text

    number = user_number[7:].strip()

    if number.isdigit() and len(number) == 10:
        pNumber = number
        context.bot.send_message(chat_id=update.effective_chat.id, text="Number has been successfully stored")
    elif not number.isdigit():
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Please enter only 10 digit phone number")
    elif len(number) > 10 or len(number) < 10:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Inputted number should be only of 10 digits!")


def location(update: Update, context: CallbackContext):
    global Location
    user_message = update.message.from_user
    # getting the feedback form the bot
    user_coordinates = update.effective_message.text
    coordinates = user_coordinates[8:].strip()

    if len(coordinates) == 0:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="There are no coordinates\n"
                                      "format is : /locate [lat], [long] \n"
                                      "Example: /locate 1.2342, 8.345")

    user_lat, user_long = coordinates.replace(':', ',').replace('-', ',').split(',')

    geolocator = Nominatim(user_agent='geoapiExercises')
    rest_lat, rest_long = 17.4299296940903, 78.41130927055349
    rest_location = (rest_lat, rest_long)
    user_location = (user_lat, user_long)
    locname = geolocator.reverse(user_location)

    dist = distance.distance(rest_location, user_location).km


    if dist <= 10:
        Location = locname.address
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Location confirmed")
        random(update, context)
    elif dist > 10:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Delivery Service is only available within the 10KM radius due to the distant issues.")


# to submit your feedback.
def feedback(update: Update, context: CallbackContext):
    user = update.message.from_user
    # getting the feedback form the bot
    feed = update.effective_message.text
    edit = feed[9:].strip()

    logger.info("User %s sent the feedback", user.first_name)

    # if the feedback is empty - displaying the format
    if len(edit) == 0:
        update.message.reply_text("feedback is empty.... \n"
                                  "format is /feedback [your feedback] \n"
                                  "Example: /feedback your service is awesome")
    # if feedback is not empty
    else:
        # storing the feedback in the file with user-ID, Full Name and date time.
        with open("feedbacks.txt", 'a', encoding='utf-8') as f:
            f.write(
                f'ID: {update.effective_user.id}, Fullname: {update.effective_user.full_name}, Date_Time: {datetime.now()}  \n'
                f'{edit}\n \n ')
        update.message.reply_text('feedback submitted')
        f.close()


def cancelOrder(update: Update, context: CallbackContext):
    reply_buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("Yes", callback_data="cancel"),
         InlineKeyboardButton("No", callback_data='no')]
    ])

    context.bot.send_message(chat_id=update.effective_chat.id, text="Are you sure you want to cancel the order", reply_markup=reply_buttons)


# shows the useful commands during the session with a short description.
def help_commands(update: Update, context: CallbackContext):
    update.message.reply_text("You can control me by sending these commands: \n \n"
                              "/start_session - starts the session \n"
                              "/cart - shows the cart items \n"
                              "/delete [item_no] - enter number of item \n"
                              "/feedback [Enter the feedback] - to submit the feedback\n"
                              "/checkout - check out of the session and place order")


# places the order on checking out. if no order, displays the "no order placed" text.
def checkout(update: Update, context: CallbackContext):
    # if cart is empty - just checks out without placing any order
    if len(cart_dict) == 0:
        reply_button = InlineKeyboardMarkup([
            [InlineKeyboardButton("Yes", callback_data="No_checkout"),
             InlineKeyboardButton("No", callback_data='no')]
        ])
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Your cart is empty. Do you still wanna checkout?"
                                 , reply_markup=reply_button)
        # context.bot.deleteMessage(chat_id=update.effective_chat.id, message_id= )
    # if cart is not empty - asks the user final time to place the order or not.
    else:
        reply_buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("Yes", callback_data="Yes_checkout"),
             InlineKeyboardButton("No", callback_data='No_checkout')]
        ])
        '''cart_final, order_amt = organize()
        line_space = '\n'
        stir = ' \n'.join(cart_final)
        stir += "\n \n" + "Total amount: " + "\t     " + str(order_amt)'''

        if len(pNumber) == 0:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text="Please provide your phone number to checkout")

        elif len(Order_type) == 0:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Please choose your Order type")
            changeOrderType(update, context)

        elif Order_type == 'Pickup':
            car, order_amt = organize()
            stir = f'Name: {update.effective_user.full_name} \n' \
                   f'phone Number: {pNumber} \n' \
                   f'Order type: {Order_type}\n\n'
            stir += ' \n'.join(car)
            stir += "\n \n" + "Total amount: " + "\t     ₹" + str(order_amt)
            context.bot.send_message(chat_id=update.effective_chat.id, text=stir, reply_markup=reply_buttons)

        elif Order_type == 'Online':
            if not len(Location) == 0:
                car, order_amt = organize()
                stir = f'Name: {update.effective_user.full_name} \n' \
                       f'Location: {Location} \n' \
                       f'phone Number: {pNumber} \n' \
                       f'Order type: {Order_type}\n\n'
                stir += ' \n'.join(car)
                stir += "\n \n" + "Total amount: " + "\t     ₹" + str(order_amt)
                context.bot.send_message(chat_id=update.effective_chat.id, text=stir, reply_markup=reply_buttons)
            elif len(Location)==0:
                context.bot.send_message(chat_id=update.effective_chat.id,
                                         text="Please provide your delivery coordinates")


# organizing the cart into displayable format.
def organize():
    car = []
    order_amt = 0.0
    for key, value in cart_dict.items():
        car.append(key + "\t     " + str(value) + "*" + str(prices(key)))
        order_amt += float(float(value) * float(prices(key)))
    return car, order_amt


def changeOrderType(update: Update, context: CallbackContext):
    reply_buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("Online Delivery", callback_data="change_Online")],
        [InlineKeyboardButton("Pickup", callback_data='change_Pickup')]
    ])

    # sends the message with three option buttons attached.
    context.bot.send_message(chat_id=update.effective_chat.id, text="choose your Order type.",
                             reply_markup=reply_buttons)


reg = r'(Menu|menu)'


def hi(update: Update, context: CallbackContext):
    menu(update, context)


regg = r'( hi|Hi|hello|Hello)'


def hello(update: Update, context: CallbackContext):
    update.message.reply_text("Hi there..👋 GISMAT RESTAURANT welcomes you")


def error(bot, update):
    logger.error("Shit!! Update {} caused error {}".format(update, update.error))


reggi = r'(J1)'


def dan(update: Update, context: CallbackContext):
    update.message.reply_text("Item added")


def main():
    # Start the bot

    # storing the feedback into the feedbacks file.
    persistence = PicklePersistence(filename="feedbacks")

    # get the updater to register handlers to the particular bot using token
    updater = Updater(TOKEN, persistence=persistence)
    dp = updater.dispatcher

    # reacting to the commands - according to the commands
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('start_session', menu_list))
    dp.add_handler(CommandHandler('feedback', feedback))
    dp.add_handler(CommandHandler('locate', location))
    dp.add_handler(CommandHandler('cart', cart_list))
    dp.add_handler(CommandHandler('checkout', checkout))
    dp.add_handler(CommandHandler('help', help_commands))
    dp.add_handler(CommandHandler('order_type', changeOrderType))
    dp.add_handler(CommandHandler('delete', delete))
    dp.add_handler(CommandHandler('cancel', cancelOrder))
    dp.add_handler(CommandHandler('number', phoneNumber))
    dp.add_handler(CallbackQueryHandler(action))

    location_handler = MessageHandler(Filters.location, location)
    dp.add_handler(location_handler)

    # updater.dispatcher.add_handler(MessageHandler(Filters.regex(reg), hi))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex(regg), hello))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex(reggi), dan))
    dp.add_error_handler(error)
    # connect to telegram and wait for the messages.
    updater.start_polling()

    # keep the program running until interrupted.
    updater.idle()


# starting the bot
if __name__ == '__main__':
    main()
