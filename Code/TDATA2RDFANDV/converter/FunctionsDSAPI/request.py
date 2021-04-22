import requests
import json
import re


def makeRequest(latitude,longitude):

    latitude = re.sub("[^0-9-.]", "", latitude)

    longitude = re.sub("[^0-9-.]", "", longitude)

    url = 'https://api.darksky.net/forecast/e6af5b5feb891b272e18f5e2fc0370a6/' + latitude + ',' + longitude

    url = 'https://api.openweathermap.org/data/2.5/onecall?lat='+ latitude + '&lon='+ longitude +'&appid=cea086b745dd21cfbe694e9beb28a8c7&units=imperial'

    response = requests.get(url)

    json_data = json.loads(response.text)

    timezone = json_data['timezone'].replace('/','--')
    new_latitude = str(json_data['lat'])
    new_longitude = str(json_data['lon'])

    city = timezone.split('--')[-1]

    timezone = timezone.replace('--','-')

    json_name = timezone + '(' + new_latitude + '_' + new_longitude + ')'

    json_path = 'converter/DSAPIDataStorage/' + json_name + '.json'

    json_file=open(json_path, "w")
    json_data = manageJsonData(json_data, city, new_latitude, new_longitude, timezone)
    json.dump(json_data,json_file,indent=4)

    return json_data, json_name, json_path

def manageJsonData(json_data, city, new_latitude, new_longitude, timezone):

    json_data.update({
        "city" : city
    })

    data2 = {
            "latitude" : float(new_latitude),
            "longitude" : float(new_longitude),
            "city" : city
            }

    json_data.update({
        "location": [
            data2
        ]
    })

    if 'current' in json_data:
        json_data['current'].update({
            "latitude" : float(new_latitude),
            "longitude" : float(new_longitude),
            "city" : city,
            "timezone" : timezone
        })

        if 'weather' in json_data['current']:
            del json_data['current']['weather']

        if 'rain' in json_data['current']:
            if type(json_data['current']['rain']) == dict:
                try:
                    res = list(json_data['current']['rain'].keys())[0] 
                    rain = json_data['current']['rain'][res]
                    del json_data['current']['rain']
                    json_data['current'].update({
                        "rain" : rain
                    })
                except:
                    pass

        if 'snow' in json_data['current']:
            if type(json_data['current']['snow']) == dict:
                try:
                    res = list(json_data['current']['snow'].keys())[0] 
                    snow = json_data['current']['snow'][res]
                    del json_data['current']['snow']
                    json_data['current'].update({
                        "snow" : snow
                    })
                except:
                    pass

        makeTempModel(json_data['current'])

        data = json_data['current']

        del json_data['current']

        json_data.update({
            "current" : [
                data
                ]
        })
    
    if 'minutely' in json_data:
        [elem.update({
            "latitude" : float(new_latitude),
            "longitude" : float(new_longitude),
            "city" : city,
            "timezone" : timezone
        })
        for elem in json_data['minutely']]

        for elem in json_data['minutely']:
            if 'weather' in elem:
                del elem['weather']
            
            if 'rain' in elem:
                if type(elem['rain']) == dict:
                    try:
                        res = list(elem['rain'].keys())[0] 
                        rain = elem['rain'][res]
                        del elem['rain']
                        elem.update({
                            "rain" : rain
                        })
                    except:
                        pass
            
            if 'snow' in elem:
                if type(elem['snow']) == dict:
                    try:
                        res = list(elem['snow'].keys())[0] 
                        snow = elem['snow'][res]
                        del elem['snow']
                        elem.update({
                            "snow" : snow
                        })
                    except:
                        pass

            makeTempModel(elem)

    if 'hourly' in json_data:
        [elem.update({
            "latitude" : float(new_latitude),
            "longitude" : float(new_longitude),
            "city" : city,
            "timezone" : timezone
        })
        for elem in json_data['hourly']]

        for elem in json_data['hourly']:
            if 'weather' in elem:
                del elem['weather']
            
            if 'rain' in elem:
                if type(elem['rain']) == dict:
                    try:
                        res = list(elem['rain'].keys())[0] 
                        rain = elem['rain'][res]
                        del elem['rain']
                        elem.update({
                            "rain" : rain
                        })
                    except:
                        pass

            if 'snow' in elem:
                if type(elem['snow']) == dict:
                    try:
                        res = list(elem['snow'].keys())[0] 
                        snow = elem['snow'][res]
                        del elem['snow']
                        elem.update({
                            "snow" : snow
                        })
                    except:
                        pass

            makeTempModel(elem)
    
    if 'daily' in json_data:
        [elem.update({
            "latitude" : float(new_latitude),
            "longitude" : float(new_longitude),
            "city" : city,
            "timezone" : timezone
        })
        for elem in json_data['daily']]

        for elem in json_data['daily']:
            if 'weather' in elem:
                del elem['weather']

            if 'rain' in elem:
                if type(elem['rain']) == dict:
                    try:
                        res = list(elem['rain'].keys())[0] 
                        rain = elem['rain'][res]
                        del elem['rain']
                        elem.update({
                            "rain" : rain
                        })
                    except:
                        pass

            if 'snow' in elem:
                if type(elem['snow']) == dict:
                    try:
                        res = list(elem['snow'].keys())[0] 
                        snow = elem['snow'][res]
                        del elem['snow']
                        elem.update({
                            "snow" : snow
                        })
                    except:
                        pass
            
            makeTempModel(elem)
    
    return json_data


def makeTempModel(json_dict):

    if 'temp' in json_dict:
        if type(json_dict['temp']) == dict:
            if 'day' in json_dict['temp']:
                day = json_dict['temp']['day']
            if 'night' in json_dict['temp']:
                night = json_dict['temp']['night']
            if 'max' in json_dict['temp']:
                maxi = json_dict['temp']['max']
            if 'min' in json_dict['temp']:
                mini = json_dict['temp']['min']
            del json_dict['temp']

            json_dict.update({
                "temp_day" : day,
                "temp_night" : night,
                "temp_max" : maxi,
                "temp_min" : mini
            })
    
    if 'feels_like' in json_dict:
        if type(json_dict['feels_like']) == dict:
            if 'day' in json_dict['feels_like']:
                day = json_dict['feels_like']['day']
            if 'night' in json_dict['feels_like']:
                night = json_dict['feels_like']['night']
            del json_dict['feels_like']

            json_dict.update({
                "feels_like_day" : day,
                "feels_like_night" : night
            })