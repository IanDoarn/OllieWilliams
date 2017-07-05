# OllieWilliams

Generate an image of Family Guy's Ollie Williams telling you the weather

## Requirements
----
go to https://openweathermap.org/ and create an api key.

create a file called api.json, it should look like this:
```json
{
  "key": "YOUR_API_KEY_HERE"
}
```

## Usage
-----

If you want it to find your location automatically
```commandline
python ollie.py
```

If you want a specific city
```commandline
python ollie.py Memphis
```

## Examples
----

OpenWeather's API response for Memphis, TN on 7/5/2017:
```json
{  
   'main':{  
      'humidity':42,
      'temp_max':302.15,
      'temp':301.23,
      'temp_min':300.15,
      'pressure':1023
   },
   'sys':{  
      'message':0.0049,
      'sunrise':1499247173,
      'country':'US',
      'id':1969,
      'sunset':1499301060,
      'type':1
   },
   'visibility':16093,
   'id':5098358,
   'name':'Garwood',
   'clouds':{  
      'all':1
   },
   'cod':200,
   'coord':{  
      'lon':-74.32,
      'lat':40.65
   },
   'wind':{  
      'speed':5.1,
      'gust':7.2,
      'deg':170
   },
   'base':'stations',
   'weather':[  
      {  
         'main':'Clear',
         'description':'clear sky',
         'long_description':'clear sky',
         'id':800,
         'icon_info':{  
            'icon_url':'http://openweathermap.org/img/w/01d.png',
            'icon_description':'sunny'
         },
         'icon':'01d'
      }
   ],
   'dt':1499284500

```

Ollie's response:
![alt text](http://i.imgur.com/jUeN4sf.jpg)