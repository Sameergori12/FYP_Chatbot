# importing the telegram bot
import time

import telegram
from telegram import *
from telegram.ext import *
# importing the items and prices from Menu
from Menu import item_list
# to copy the content from one file to another file
import shutil
# importing json
import json

# helps us connect to the telegram with the
Token1 = '5131675223:AAH_9GqSF3RMtCaUEiALwcbr3ly869oTMls'

print("Restaurant bot started...")

order_items = ''

admin_ids = [967864205]


# displays the current Menu with the prices.
def Menu(update: Update, context: CallbackContext):
    if update.message.from_user.id in admin_ids:
        items = str(item_list)
        stir = items.replace(",", "\n")
        # displaying the items in the bot.
        update.message.reply_text(f'Current Item list: \n \n{stir[1:-1]}')
    else:
        update.message.reply_text('You are not authorized to access this BOT')


# displays the feedbacks received.
def feedback(update: Update, context: CallbackContext):
    if update.message.from_user.id in admin_ids:
        # opening the feedbacks from a file.
        with open("feedbacks.txt", 'r', encoding='utf-8') as f:
            feed_string = f.read()
        # displaying the result in the Restaurant bot
        update.message.reply_text(feed_string)
    else:
        update.message.reply_text('You are not authorized to access this BOT')


# shows the useful commands during the session with a short description.
def help_commands(update: Update, context: CallbackContext):
    if update.message.from_user.id in admin_ids:
        update.message.reply_text("You can control me by sending these commands: \n \n"
                                  "/menu - shows the menu list \n"
                                  "/feedback - shows all the received feedbacks \n")
    else:
        update.message.reply_text('You are not authorized to access this BOT')


def action(update: Update, context: CallbackContext):
    if update.message.from_user.id in admin_ids:
        update.message.reply_text("Try to communicate using the following commands with the Bot. "
                                  "I cannot understand any other language besides the following commands")
        help_commands(update, context)
        pass
    else:
        update.message.reply_text("You are not authorized to access this Bot")


def price_change(update: Update, context: CallbackContext):
    if update.message.from_user.id in admin_ids:
        change = update.effective_message.text
        edit = change[8:].strip()
        if edit == 'default':
            shutil.copyfile('original_menuitems.txt', 'temp_menuitems.txt')
            update.message.reply_text("Item Prices have been set to their default values")
        else:
            # to capitalize the first letter of each word of item.
            edit = edit.title()
            fan, nan = edit.replace(':', ':').replace('-', ':').split(':')

            menu_items = {}
            with open("temp_menuitems.txt") as f:
                for line in f:
                    (k, v) = line.replace(':', ':').replace('-', ':').split(':')
                    menu_items[k] = float(v)

            menu_items[fan] = nan

            with open("temp_menuitems.txt", 'w') as f:
                for key, value in menu_items.items():
                    f.write('%s: %.2f\n' % (key, float(value)))
            update.message.reply_text("Price changes have been made.")
    else:
        update.message.reply_text("You are not authorized to access this Bot")


def main():
    # Start the bot
    # accessing the file for the received feedbacks.
    persistence = PicklePersistence(filename="feedbacks")

    # get the updater to register handlers to the particular bot using token
    updater = Updater(Token1, persistence=persistence)
    dp = updater.dispatcher

    # reacting to the commands - according to the commands
    dp.add_handler(CommandHandler('feedback', feedback))
    dp.add_handler(CommandHandler('menu', Menu))
    dp.add_handler(CommandHandler('help', help_commands))
    dp.add_handler(CommandHandler('change', price_change))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, action))

    # connect to telegram and wait for the messages.
    updater.start_polling()

    # keep the program running until interrupted.
    updater.idle()


# starting the bot
if __name__ == '__main__':
    main()
