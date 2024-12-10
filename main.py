from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import requests

#API:
API_Key = ""

#TELEGRAM BOT:
TOKEN = ""
BOT_USERNAME: Final = ''

# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! Welcome in chat with weather BOT!')
    
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! Tell me location and I will tell you the weather here!')
    
# Responses

def handle_response(text: str) -> str:
    city_name: str = text.lower().strip()
    
    try:
        city_coordinates = {}
        response = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=5&appid={API_Key}")
        if response.status_code == 200:
            data = response.json()
            city_coordinates.update({'lat':data[0]['lat'], 'lon': data[0]['lon']})
            
            response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={city_coordinates['lat']}&lon={city_coordinates['lon']}&appid={API_Key}&units=metric")

            if response.status_code == 200:
                data = response.json()
                message = "In " + city_name.capitalize() + " the currenly weather is: " + str(data['weather'][0]['description']) + ".\nTemperature is: " + str(data['main']['temp']) + " C°"
                return message
        else:
            message = "Site is not working, response code: " + str(response.status_code)
            return message
    except IndexError:
            message = "Wrong city name, please enter correct one!"
            return message

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text
    
    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')
    
    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)
        
    print('Bot:', response)
    await update.message.reply_text(response)
    
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} cause error {context.error}')
    
if __name__ == '__main__':
    print('Starting bot...')
    app = Application.builder().token(TOKEN).build()
    
    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    
    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    
    # Errors
    app.add_error_handler(error)
    
    # Polls the bot
    print('Polling...')
    app.run_polling(poll_interval=3) # how often you want to check for updates(3 s)