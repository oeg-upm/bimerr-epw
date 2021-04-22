from bs4 import BeautifulSoup
import requests
import urllib.request
import time
import os
import re

def continentLinker(continent):
    if continent == "Africa":
        continentLink = "/WMO_Region_1_Africa/"
    elif continent == "Asia":
        continentLink = "/WMO_Region_2_Asia/"
    elif continent == "South America":
        continentLink = "/WMO_Region_3_South_America/"
    elif continent == "North and Central America":
        continentLink = "/WMO_Region_4_North_and_Central_America/"
    elif continent == "SouthwestPacific":
        continentLink = "/WMO_Region_5_Southwest_Pacific/"
    elif continent == "Europe":
        continentLink = "/WMO_Region_6_Europe/"
    elif continent == "Antarctica":
        continentLink = "/WMO_Region_7_Antarctica/"
    return continentLink


def scrapeOB(city,country,continentLink):
    epwLinkList = []

    link = "http://climate.onebuilding.org"

    responseContinent = requests.get(link+continentLink,timeout=10)
    continentData = BeautifulSoup(responseContinent.content, "html.parser")

    for countryLink in continentData.find_all('a', attrs={"href":""}, href=True):
        countryName = countryLink.get_text()
        #countryName.split('_')
        #print(countryName)
        if country in countryName:
            #print(countryName)
            countryName = countryLink['href']
            #countryName = countryName.replace('/index.html','/')
            responseCountry = requests.get(link+continentLink+countryName,timeout=10)
            countryData = BeautifulSoup(responseCountry.content, "html.parser")

            for cityLink in countryData.find_all('a', attrs={"href":""}, href=True):
                cityName = cityLink.get_text()
                if city in cityName:
                    cityName = cityLink['href']
                    if cityName.endswith('.zip'):
                        epwLinkList.append(link+continentLink+countryName.replace('/index.html','/')+cityName)

    return epwLinkList
    #devuelve una lista con los links de los epw

#city = 'Madrid'
#country = 'Spain'
#continent = "Europe"

#continentLink = continentLink(continent)
#scrapeOB(city,country,continentLink)
