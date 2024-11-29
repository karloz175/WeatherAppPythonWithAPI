import requests

API_Key = ""


city_coordinates = {}

do_we_check_another_city = True
while(do_we_check_another_city):
    try:
        city_name = input("In which city you would like to check temperature?")
        response = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=5&appid={API_Key}")
        if response.status_code == 200:
            data = response.json()
            city_coordinates.update({'lat':data[0]['lat'], 'lon': data[0]['lon']})
            
            response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={city_coordinates['lat']}&lon={city_coordinates['lon']}&appid={API_Key}&units=metric")

            if response.status_code == 200:
                data = response.json()
                print("In " + str(data['name']) + " the currenly weather is: " + str(data['weather'][0]['description']) + ".")
                print("Temperature is: " + str(data['main']['temp']) + " C°")
        else:
            print("Site is not working, response code: " + str(response.status_code))
        check = input("Do you want to check another's city weather?(Type \"no\" to end the program)")
        if check == "no":
            do_we_check_another_city = False
    except IndexError:
        print("Wrong city name, please enter correct one!")
        