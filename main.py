import logging
import os
import random
import telegram
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, Updater, PicklePersistence, CommandHandler, CallbackQueryHandler, \
    MessageHandler, ConversationHandler, Filters
import tensorflow as tf
from keras.preprocessing.text import Tokenizer

from config import HISticker, songList
from textAnalysisMl import predictText

PORT = int(os.environ.get('PORT', 5000))
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.setLevel(logging.DEBUG)

TOKEN="1713210432:AAHJykN7NlthYpx3YxxufPi0gzrwZEqL2wU"
bot = telegram.Bot(token=TOKEN)
def start(update: Update, context: CallbackContext) -> None:
    sticker = random.choice(HISticker)[0]
    bot.send_sticker(chat_id=update.effective_chat.id, sticker=sticker)
    update.message.reply_text('Hello Im Waku-waku tell me anything')



def reply(update: Update, context: CallbackContext):
    newT=update.message.text
    output=predictText(newT)
    print (output)
    update.message.reply_text(output[2])
    update.message.reply_text(random.choice(songList[output[1]]))



def main():
    """Start the bot."""
    updater = Updater(TOKEN, persistence=PicklePersistence(filename='bot_data'))
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(MessageHandler(Filters.text,reply))


    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
