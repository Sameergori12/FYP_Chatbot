# importing the telegram bot
import time

import telegram
from telegram import *
from telegram.ext import *
# importing the items and prices from Menu
from Menu import item_list
# importing json
import json

# helps us connect to the telegram with the
Token = "5153310535:AAEOuGqyquD2a5rnW49nR8q8p5pK3iiPQlE"

print("Restaurant bot started...")

admin_ids = [967864205]


def order(update: Update, context: CallbackContext):
    if update.message.from_user.id in admin_ids:
        while True:
            f = open("orders.txt", 'r+')
            content = f.read()
            if len(content) >= 5:
                f.truncate(0)
            else:
                continue
            update.message.reply_text(f" New Order Recieved \n"
                                      f"{content}")
            time.sleep(5)
    else:
        update.message.reply_text('You are not authorized to access this BOT')


def action(update: Update, context: CallbackContext):
    if update.message.from_user.id in admin_ids:
        pass
    else:
        update.message.reply_text("You are not authorized to access this Bot")


def main():
    # Start the bot
    # accessing the file for the received feedbacks.
    # get the updater to register handlers to the particular bot using token
    updater = Updater(Token)
    dp = updater.dispatcher

    # reacting to the commands - according to the commands

    dp.add_handler(CommandHandler('orders', order))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, action))

    # connect to telegram and wait for the messages.
    updater.start_polling()

    # keep the program running until interrupted.
    updater.idle()


# starting the bot
if __name__ == '__main__':
    main()


