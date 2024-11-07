from django.shortcuts import render
import json
import urllib.request
import urllib.parse


# Create your views here.
# def index(request):
#     if request.method == 'POST':
#         city = request.POST.get('city')
#         if city:
#             encoded_city = urllib.parse.quote(city)
#             res = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q='+encoded_city+'&appid=5c1296bad970de5c2c950702d87ec0e5').read()
#             json_data = json.loads(res)
#             temperature_kelvin = json_data['main']['temp']
#             temperature_celsius = temperature_kelvin - 273.15
#             temperature_celsius_str = str(round(temperature_celsius, 2))
            
#             data = {
#                 'temperature': temperature_celsius_str,
#                 'humidity' : str(json_data['main']['humidity']),
#                 'pressure' : str(json_data['main']['pressure']),
#             }

#     else:
#         data = None
#         city = 'hello'
       
#     return render(request, 'weather.html', {'city': city, 'data': data})

def index(request):
    data = None
    city = None

    if request.method == 'POST':
        city = request.POST.get('city')
        if city:
            try:
                encoded_city = urllib.parse.quote(city)
                
                api_url = (
                    'http://api.openweathermap.org/data/2.5/weather?q='+ encoded_city + '&appid=5c1296bad970de5c2c950702d87ec0e5'
                )
                res = urllib.request.urlopen(api_url).read()
                json_data = json.loads(res)
                
                if 'main' in json_data:
                    temperature_kelvin = json_data['main']['temp']
                    temperature_celsius = temperature_kelvin - 273.15
                    temperature_celsius_str = str(round(temperature_celsius, 2))

                    data = {
                        'temperature': temperature_celsius_str,
                        'humidity': str(json_data['main']['humidity']),
                        'pressure': str(json_data['main']['pressure']),
                    }
                else:
                    data = None
            
            except urllib.error.HTTPError as e:
                # Handle HTTP errors from the API
                data = {"error": f"City not found. Please try again."}
            except urllib.error.URLError as e:
                # Handle URL errors, such as connection issues
                data = {"error": "Network error. Please check your connection."}
            except Exception as e:
                # Handle any other exceptions
                data = {"error": "An unexpected error occurred. Please try again."}

    else:
        city = ""

    return render(request, 'weather.html', {'city': city, 'data': data})