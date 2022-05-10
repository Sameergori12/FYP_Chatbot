import telegram
from telegram import *
from telegram.ext import *
from datetime import date
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
                # get current date and time
                current_datetime = date.today()

                # convert datetime obj to string
                str_current_datetime = str(current_datetime)

                # create a file object along with extension
                file_name = str_current_datetime + ".txt"
                file = open(file_name, 'a')
                file.write(content + "\n\n")
                f.truncate(0)
                file.close()
                f.close()
            else:
                continue
            update.message.reply_text(f" New Order Recieved \n\n"
                                      f"{content}")
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


