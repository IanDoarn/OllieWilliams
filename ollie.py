from openweatherapi import OpenWeather


owapi = OpenWeather(api_file='api.json',
                    city_name='Memphis')


data, url = owapi.get_weather({'type': 'id', 'id': owapi.city_id}, conditions='current')

print(data)
print(url)