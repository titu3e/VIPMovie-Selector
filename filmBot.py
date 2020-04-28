#!/usr/bin/env python3

from telegram.ext import (Updater, CommandHandler)
import os, core, classes, msg


def Bot_function(command, argument='context', function='str'):
    function = function + '("""' + argument + '""")'
    function = function.replace('"""context"""', '" ".join(context.args)')

    def The_function(update, context):
        chat = classes.Chat(update.effective_chat.id)
        if not os.path.exists(chat.path):
            cmd = 'mkdir -p ' + chat.path
            os.system(cmd)
        core.chat = chat
        context.bot.send_message(chat_id=chat.Id, text=eval(function))

    dispatcher.add_handler(CommandHandler(command, The_function))


def Bot_special():

    def Export_function(update, context):
        chat = classes.Chat(update.effective_chat.id)
        if not os.path.exists(chat.path):
            cmd = 'mkdir -p ' + chat.path
            os.system(cmd)
        core.chat = chat
        exportSuccessful, archive = core.exportData('')
        if exportSuccessful:
            with open(archive, 'rb') as a:
                context.bot.send_document(chat_id=chat.Id, document=a)
        else:
            context.bot.send_message(chat_id=chat.Id, text=msg.gotnothing)

    dispatcher.add_handler(CommandHandler('export', Export_function))


def startBot():
    updater.start_polling()

    # BEGIN start
    Bot_function(command='start', argument=msg.start)
    Bot_function(command='help', argument=msg.start)
    Bot_function(command='h', argument=msg.start)

    Bot_function(command='random', argument=msg.random)
    Bot_function(command='r', argument=msg.random)

    Bot_function(command='manage', argument=msg.manage)
    Bot_function(command='m', argument=msg.manage)

    Bot_function(command='info', argument=msg.info)
    Bot_function(command='i', argument=msg.info)
    Bot_function(command='git', argument=msg.github)

    Bot_function(command='film', function='core.dbFind')
    Bot_function(command='find', function='core.dbFind')
    Bot_function(command='f', function='core.dbFind')
    Bot_function(command='who', function='core.dbFindPerson')

    Bot_function(command='check', function='core.checkDb')
    Bot_function(command='upgrade', function='core.upgradeDb')
    # END start

    # BEGIN random
    Bot_function(command='rr', argument='localrr', function='core.getRand')
    Bot_function(command='rw', argument='watchlist', function='core.getRand')
    Bot_function(command='rt', argument='local', function='core.getRand')
    Bot_function(command='re', argument='direct', function='core.recommend')

    Bot_function(command='r100', argument='ratings100k', function='core.getRand')
    Bot_function(command='r10', argument='ratings10k', function='core.getRand')
    Bot_function(command='r1', argument='ratings1k', function='core.getRand')
    Bot_function(command='ra', argument='nonempty', function='core.getRand')
    Bot_function(command='tr', argument='anymovie', function='core.getRand')
    # END random

    # BEGIN manage
    Bot_function(command='like', function='core.like')
    Bot_function(command='l', function='core.like')
    Bot_function(command='save', function='core.save')
    Bot_function(command='s', function='core.save')
    Bot_function(command='erase', function='core.erase')

    Bot_function(command='last', function='core.showLast')
    Bot_function(command='watch', function='core.watchList')
    Bot_function(command='w', function='core.watchList')
    Bot_function(command='top', function='core.readCharts')

    Bot_function(command='import', function='core.massLike')
    Bot_function(command='how2i', argument=msg.how2i)
    Bot_special() # export
    Bot_function(command='forget', function='core.forget')
    # END manage


if __name__ == '__main__':
    import logging
    logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level=logging.INFO
            )

    with open('TOKEN') as f: TOKEN = f.read().rstrip()

    core.upgradeDb()

    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    startBot()
