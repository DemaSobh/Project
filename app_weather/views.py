from datetime import datetime
from django.shortcuts import redirect, render
import requests

# Create your views here.


def welcome(request):
    return render(request, 'welcome.html')

def today_weather(request):
    city = request.GET.get('city', '')
    
    try:
        url = "https://community-open-weather-map.p.rapidapi.com/weather?units=metric&q={}".format(city)
        result = requests.get(url,headers={'X-RapidAPI-Key':'5da4349f1amsh54606aa17ba5089p16dbfcjsncf260c9da9d1','X-RapidAPI-Host':'community-open-weather-map.p.rapidapi.com'})
        
        if result.status_code != 200:
            return redirect('/error')
        else:
            data = result.json()
            weather_status = data['weather'][0]['description']
            image = data['weather'][0]['icon']
            temp = data['main']['temp']
            humidity = data['main']['humidity']
            speed = data['wind']['speed']
            pressure = data['main']['pressure']
            
            template_data ={'city':city,'weather_status':weather_status, 'temp':temp, 'humidity':humidity, 'speed': speed, 'pressure':pressure, 'image':image}
            return render(request, 'today.html', template_data)
    except:
        return redirect('/error')

def month_weather(request):
    city = request.GET.get('city', '')
    
    try:
        url = "https://community-open-weather-map.p.rapidapi.com/climate/month?units=metric&q={}".format(city)
        result = requests.get(url,headers={'X-RapidAPI-Key':'5da4349f1amsh54606aa17ba5089p16dbfcjsncf260c9da9d1','X-RapidAPI-Host':'community-open-weather-map.p.rapidapi.com'})
        
        class WeatherData:
            pass
        
        if result.status_code != 200:
            return redirect('/error')
        else:
            data = result.json()
            weather_list = []
            
            for item in data['list']:
                d = WeatherData()
                dt = datetime.fromtimestamp(item['dt'])
                d.dt = dt.strftime('%Y-%m-%d')
                d.humidity = item['humidity']
                d.pressure = item['pressure']
                d.min_temp = item['temp']['average_min']
                d.max_temp = item['temp']['average_max']
                d.wind_speed = item['wind_speed']
                weather_list.append(d)
            
            template_data ={'list':weather_list, 'city':city}
            return render(request, 'month.html', template_data)
    except:
        return redirect('/error')

def ip_weather(request):
    # get user id from request
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        ip = request.META['HTTP_X_FORWARDED_FOR']
    elif 'REMOTE_ADDR' in request.META:
        ip = request.META['REMOTE_ADDR']
    else:
        return redirect('/error')
    
    # get city from ip
    
    try:
        result = requests.get('https://ipinfo.io/{}/json'.format(ip))
        if(result.status_code == 200):
            data = result.json()
            if 'city' in data:
                city=data['city']
                return redirect('/weather/today?city={}'.format(city))
            else:
                return redirect('/error')
    except:
        return redirect('/error')

def error(request):
    return render(request, 'error.html')
