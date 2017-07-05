from openweatherapi import OpenWeather
from meme import draw_text, ollify_text
import os
import sys

def main(out_file='forecast.jpg', auto_open=True, city=None):
    owapi = OpenWeather(api_file='api.json',
                        city_name=city)
    data, _ = owapi.get_weather({'type': 'id', 'id': owapi.city_id}, conditions='current')

    conditions = data['weather'][0]['long_description']
    draw_text(ollify_text(conditions), out_file)
    if auto_open:
        os.startfile(out_file)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == '-h':
            print('Ask Ollie what the weather is\n\n'
                  'usage:\n'
                  'ollie.py city_name\n'
                  'leave city_name blank and it will try to find you location')

        if sys.argv[1] != '-h':
            main(city=' '.join(sys.argv[1:]))
    else:
        main()
