import json
import requests
import zlib
import os


class OpenWeather:

    def __init__(self, api_file=None, api_key=None,
                 city_list_file='city.list.min.json',
                 city_name=None, country_code='US'):

        if api_file is None:
            if api_key is None:
                raise ValueError('Must supply api_key if no api_file')
            self.api_file = None
            self.api_key = api_key
        else:
            if not os.path.isfile(api_file):
                raise FileNotFoundError(api_file)
            self.api_file = self._load_api_file(api_file)
            self.api_key = self.api_file['key']

        if not os.path.isfile(city_list_file):
            self._get_city_list()

        self.city_name = city_name
        self.country_code = country_code
        self.city_data = self._get_city_data()
        self.city_id = self.city_data['id']

        self._call_types = {'current': 'weather',
                            '5day': 'forecast',
                            '16day': r'forecast/daily'}
        self._call_modes = ['xml', 'html']
        self._token_types = ['q', 'id', 'latlon', 'zip']

    @staticmethod
    def _load_api_file(file):
        with open(file, 'r')as f:
            data = json.load(f)
        return data

    @staticmethod
    def _get_local_info(url='http://ipinfo.io/json'):
        info = requests.get(url)
        return info.json()

    @staticmethod
    def _get_city_list(url=r'http://bulk.openweathermap.org/sample/',
                       file=r'city.list.min.json.gz'):

        g_file = requests.get('{}{}'.format(url, file))

        if g_file.status_code == 404:
            raise FileNotFoundError('Could get {} from {}. Response: [{}]'.format(file, url,
                                                                                  g_file.status_code))
        if g_file.status_code == 200:
            data = zlib.decompress(g_file.content, zlib.MAX_WBITS | 32)
            with open('city.list.min.json', 'wb') as f:
                f.write(data)
            f.close()
            return True
        else:
            return False

    def _get_city_data(self, file='city.list.min.json'):

        if not os.path.isfile(file):
            self._get_city_list()

        with open('city.list.min.json', encoding="utf8")as f:
            data = json.load(f)

        if self.city_name is None:
            self.city_name = self._get_local_info()['city']
            self.country_code = self._get_local_info()['country'].upper()

        for city in data:
            if city['country'] == self.country_code and city['name'] == self.city_name:
                return city

    def _query_token(self, data):
        _type = data['type']
        if _type not in self._token_types:
            raise ValueError('[{}] invalid token type. Expected 1 from: {}'.format(_type,
                                                                            str(self._token_types)))
        if _type == 'q':
            return 'q={},{}'.format(self.city_name, self.country_code.lower())
        elif _type == 'id':
            if 'id' not in data.keys():
                raise KeyError('id must be in location data when using id')
            return 'id={}'.format(data['id'])
        elif _type == 'latlon':
            if 'latlon' not in data.keys():
                raise KeyError('latlon must be in location data when using latitude and longitude')
            if type(data['latlon']) is not list:
                raise ValueError('latlon must be a list not {}'.format(str(type(data['latlon']))))
            if 'cnt' not in data.keys():
                raise KeyError('cnt must be in location data when using latitude and longitude')
            return "lat={d['lat']}&lon={d['lon']}&cnt={d['cnt']}".format(d={'lat': data['latlon'][0],
                                                                            'lon': data['latlon'][1],
                                                                            'cnt': data['cnt']})
        elif _type == 'zip':
            if 'zip' not in data.keys():
                raise KeyError('zip must be in location data')
            return 'zip={},{}'.format(data['zip'], self.country_code.lower())

    def _build_call_url(self, base_url=r'http://api.openweathermap.org/data/2.5/',
                        token=None, call_mode=None, call_type='weather'):

        if token is None:
            raise ValueError('Invalid api token: [{}]'.format(token))

        if call_type not in self._call_types.keys():
            raise ValueError('call type [{}] invalid. must be None or {}'.format(call_type,
                                                                                 str(self._call_types)))

        if call_mode is not None and call_mode not in self._call_modes:
            raise ValueError('call mode [{}] invalid. must be None or {}'.format(call_mode,
                                                                                 str(self._call_modes)))

        _key = '&APPID=' + self.api_key
        _call_type = self._call_types[call_type] + "?"

        if call_mode is None:
            return '{}{}{}{}'.format(base_url, _call_type, token, _key)

        elif call_mode is not None and call_mode in ['xml', 'html']:
            mode = '&mode=' + str(call_mode)
            return '{}{}{}{}{}'.format(base_url, _call_type, token, mode, _key)

    @staticmethod
    def _call_api(url, stream=False):
        return requests.get(url, stream=stream).json()

    def get_weather(self, location_data, call_mode=None, conditions=None):
        token = self._query_token(location_data)

        if conditions not in self._call_types.keys():
            raise KeyError('[{}] invalid key. Expected 1 from: {}'.format(conditions,
                                                                   str([k for k in self._call_types.keys()])))
        url = self._build_call_url(token=token, call_mode=call_mode, call_type=conditions)
        response = self._call_api(url)
        return response, url
