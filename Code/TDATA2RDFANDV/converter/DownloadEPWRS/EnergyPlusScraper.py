from bs4 import BeautifulSoup
import requests
import urllib.request
import time
import os
import re


def continentGetLink(continent):
    if continent == "Africa":
        continentLink = "/weather-region/africa_wmo_region_1"
    elif continent == "Asia":
        continentLink = "/weather-region/asia_wmo_region_2"
    elif continent == "South America":
        continentLink = "/weather-region/south_america_wmo_region_3"
    elif continent == "North and Central America":
        continentLink = "/weather-region/north_and_central_america_wmo_region_4"
    elif continent == "SouthwestPacific":
        continentLink = "/weather-region/southwest_pacific_wmo_region_5"
    elif continent == "Europe":
        continentLink = "/weather-region/europe_wmo_region_6"
    return continentLink


def scrapeEP(city,country,continentLink):

    epwLinkList = []

    link = "https://energyplus.net"

    responseContinent = requests.get(link+continentLink,timeout=10)
    continent = BeautifulSoup(responseContinent.content, "html.parser")

    for countryLink in continent.find_all('a', attrs={"class": "btn btn-default left-justify blue-btn"}, href=True):
        countryName = countryLink.get_text()
        #print(countryName)
        if country in countryName:
            countryName = countryLink['href']
            responseCountry = requests.get(link+countryName,timeout=10)
            countryData = BeautifulSoup(responseCountry.content, "html.parser")

            for cityLink in countryData.find_all('a', attrs={"class": "btn btn-default left-justify blue-btn"}, href=True):
                cityName = cityLink.get_text()
                #print(cityName)
                if city in cityName:
                    cityName = cityLink['href']
                    responseCity = requests.get(link+cityName,timeout=10)
                    cityData = BeautifulSoup(responseCity.content, "html.parser")

                    for downloadLink in cityData.find_all('a', attrs={"class": "btn btn-default left-justify blue-btn"}, href=True):
                        if downloadLink.text == 'epw':
                            epwLinkList.append(link+downloadLink['href'])
    #print(epwLinkList)
    return epwLinkList    

    #devuelve una lista con los links de los epw



#continentLink = continentGetLink(continent)
#scrapeEP(city,country,continentLink)