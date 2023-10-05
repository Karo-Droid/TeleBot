from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, Updater
import requests


TOKEN:Final = Updater('6599682307:AAGjPG6r3NMYV8NR-XF0pyXj13ifLCM6VLQ')
BOT_USERNAME: Final = '@InstaDdownloaderBot'


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('ss')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('hh')


async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('cc')


def handle_response(text: str) -> str:
    processed: str = text.lower()

    if 'hello' in processed:
        return 'hey'
    return 'what??'


async def handle_message(update: Update, bot):
    message_type: str = update.message.chat.type
    link = update.message.text

    media_id = link.split('/')[-1]

    media_response = requests.get(
        f'https://graph.instagram.com/v18.0/media/{media_id}?access_token=IGQWRQaVZASWEdwTmhiWk5aLWUwNl9QbGd6dW5idVp4QjUzUm1JTmdIZAHZAka3BkQlJROThMdDE2czdQUzdvT3BhTVJnUWoxNDl1WjkxTkdSbFE3ODhaa2NQcGdaQjJETzRKQm02UVg3aFJldwZDZD')
    media_data = media_response.json()
    print(f"User ({update.message.chat.id}) in {message_type}:'{update.message.text}'")

    media_url = media_data['media_url']
    media_response = requests.get(media_url)
    with open('media.jpg', 'wb') as f:
        f.write(media_response.content)

    # Send the media file to the user
    await bot.send_photo(update.message.chat_id, open('media.jpg', 'rb'), reply_to_message_id=update.message.message_id)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")


if __name__ == '__main__':
    print('Starting...')
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))

    # Message
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Errors
    app.add_error_handler(error)

    print('Polling...')
    app.run_polling(poll_interval=1)
