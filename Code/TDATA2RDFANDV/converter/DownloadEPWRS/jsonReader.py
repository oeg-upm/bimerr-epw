import json

data = {
        "city" : "Madrid",
        "country" : "Spain",
        "continent" : "Europe",
        "year" : 1984,
        "source" : "EnergyPlus",
        "output" : "link" # "output" : "file"
        }

def jsonReader(data):
    city = data["city"]
    country = data["country"]
    continent = data["continent"]
    year = data["year"]
    source = data["source"]
    out = data["output"]
    return city, country, continent, year, source, out

def jsonReaderYears(data):
    city = data["city"]
    country = data["country"]
    continent = data["continent"]
    source = data["source"]
    return city, country, continent, source
    

#city, country, continent, year, source = jsonReader(data)
