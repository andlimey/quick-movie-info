from telegram.ext import Updater, Filters
from telegram.ext import CommandHandler, MessageHandler, CallbackQueryHandler
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from collections import OrderedDict
from dotenv import load_dotenv
import logging
import movies_scraper
import os

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Hello. I am bot that gives bite-sized information regarding movies.\nType /info to find out how to use me!")

def info(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="1. Type /find\n2. Enter movie name. E.g. /find Fast and Furious.\n3. Select the movie you're looking for.")

def reply(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Please use the /find command to search for movies")

def find(bot, update):
    chat_id = update.message.chat_id
    # We want the message after /find.
    user_message = update.message.text[5:].strip()
    if user_message == "":
        bot.send_message(chat_id=chat_id, text="Please input a movie name after /find")
    else:
        bot.send_message(chat_id=chat_id, text="Your query is: {}".format(user_message))
        bot.send_message(chat_id=chat_id, text="Wait while we retrieve data...")
        movies_dictionary = get_movies_dictionary(user_message)
        button_list = []
        for movie_name in movies_dictionary:
            movie_slug = movies_dictionary[movie_name]
            button_list.append(InlineKeyboardButton(movie_name, callback_data=movie_slug))
        reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=1))
        bot.send_message(chat_id, text="Click on one of the movies below, or type /find to search for another movie.", reply_markup=reply_markup)

def search_movie_details(bot, update):
    movie_slug = update.callback_query.data
    info_dictionary = movies_scraper.get_movie_info(movie_slug)
    print_information(bot, update, info_dictionary)

def get_movies_dictionary(movie_name):
    movies_dictionary = OrderedDict(movies_scraper.get_search_results(movie_name))
    return movies_dictionary

def print_information(bot, update, info_dictionary):
    title = info_dictionary["title"]
    movie_synopsis = info_dictionary["movie_synopsis"]
    consensus = info_dictionary["consensus"]
    tomato_meter = info_dictionary["tomato_meter"]
    tomato_total_count = info_dictionary["tomato_total_count"]
    audience_score = info_dictionary["audience_score"]
    audience_verified_ratings = info_dictionary["audience_verified_ratings"]
    url = info_dictionary["url"]
    bot.send_message(chat_id=update.callback_query.message.chat_id, text="Title: {}".format(title))
    bot.send_message(chat_id=update.callback_query.message.chat_id, text="Synopsis: {}".format(movie_synopsis))
    bot.send_message(chat_id=update.callback_query.message.chat_id, text="Critics Consensus: {}".format(consensus))
    bot.send_message(chat_id=update.callback_query.message.chat_id, text="Tomatometer: {}. Total Count: {}".format(tomato_meter, tomato_total_count))
    bot.send_message(chat_id=update.callback_query.message.chat_id, text="Audience Score: {}. Number of Verified Ratings: {}".format(audience_score, audience_verified_ratings))
    bot.send_message(chat_id=update.callback_query.message.chat_id, text="For more information, go to {}".format(url))

def build_menu(buttons,
               n_cols,
               header_buttons=None,
               footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu

def main():
    # Adds handlers and register in the dispatcher.
    start_handler = CommandHandler("start", start)
    info_handler = CommandHandler("info", info)
    find_handler = CommandHandler("find", find)
    callback_handler = CallbackQueryHandler(search_movie_details)
    reply_handler = MessageHandler(Filters.text, reply)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(info_handler)
    dispatcher.add_handler(find_handler)
    dispatcher.add_handler(callback_handler)
    dispatcher.add_handler(reply_handler)
    run(updater)

# Used to load .env file
load_dotenv()
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
TOKEN = os.getenv("TOKEN")
MODE = os.getenv("MODE")
updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher

if MODE == "dev":
    def run(updater):
        updater.start_polling()
        updater.idle()
elif MODE == "prod":
    def run(updater):
        # Standard config if bot is hosted on heroku
        PORT = int(os.environ.get('PORT', '8443'))
        HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME")
        updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN)
        updater.bot.set_webhook("https://{}.herokuapp.com/{}".format(HEROKU_APP_NAME, TOKEN))
        updater.idle()
else:
    logger.error("No mode specified")
    sys.exit(1)

main()