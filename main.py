import requests

#API:
API_Key = ""

#TELEGRAM BOT:
TOKEN = ""
CHAT_ID = ""

# Checking chat id:
url = f"https://api.telegram.org/bot{TOKEN}/getUpdates" 
result = requests.get(url).json()['result']
city_name = result[len(result)-1]['message']['text'] # - taking city name from last telegram message to bot
city_coordinates = {}

def send_message(mssg):
    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={mssg}")


try:
    #city_name = input("In which city you would like to check temperature?") # - checking name of city from console
    response = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=5&appid={API_Key}")
    if response.status_code == 200:
        data = response.json()
        city_coordinates.update({'lat':data[0]['lat'], 'lon': data[0]['lon']})
        
        response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={city_coordinates['lat']}&lon={city_coordinates['lon']}&appid={API_Key}&units=metric")

        if response.status_code == 200:
            data = response.json()
            message = "In " + city_name + " the currenly weather is: " + str(data['weather'][0]['description']) + ".\nTemperature is: " + str(data['main']['temp']) + " C°"
            send_message(message)
    else:
        message = "Site is not working, response code: " + str(response.status_code)
        send_message(message)
except IndexError:
    message = "Wrong city name, please enter correct one!"
    send_message(message)
        