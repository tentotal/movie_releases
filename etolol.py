#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
"""

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from movie_data_handler import *
from db_handler import *
from keys import TOKEN

def start(update, context):
    update.message.reply_text('I can help you get digital/physical release date of a movie. You can start by sending /findmovie command.')
    add_user(update.message.from_user.id)
    set_stage('start', update.message.from_user.id)

def findmovie(update, context):
    update.message.reply_text('Give me the title of a movie')
    add_user(update.message.from_user.id)
    set_stage('findmovie', update.message.from_user.id)

def texthandler(update, context):
    stage = get_stage(update.message.from_user.id)
    if stage == 'start':
        update.message.reply_text('I can help you get digital/physical release date of a movie. You can start by sending /findmovie command.')
        return

    if stage == 'findmovie':
        try:
            movies = get_movie_ids_by_title(update.message.text)
            output = ['Select your movie:']
            movie_list = []
            for m in movies:
                output.append(str(movies.index(m)+1) + ') ' + m['title'] + ', premiere: ' + m['release_date'])
                movie_list.append(str(m['id']))
            movie_list = "\n".join(movie_list)
            update_movie_list(movie_list, update.message.from_user.id)
            output = "\n".join(output)
            update.message.reply_text(output)
            set_stage('selectmovie', update.message.from_user.id)
        except Exception as e: 
            print(e)
            update.message.reply_text('Incorrect title')
            set_stage('findmovie', update.message.from_user.id)
        return
    
    if stage == 'selectmovie':
        try:
            movies = get_movie_list(update.message.from_user.id).split('\n')
            date = get_release_date(movies[int(update.message.text)-1])
            if date != 0:
                update.message.reply_text('Digital/physical release date: ' + date)
            else:
                update.message.reply_text('Digital/physical release date is unavailable')
            set_stage('start', update.message.from_user.id)
        except Exception as e: 
            print(e)
            update.message.reply_text('Wrong number (out of range)')
            set_stage('selectmovie', update.message.from_user.id)
        return

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("findmovie", findmovie))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, texthandler))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()