import zipfile, urllib, os
from urllib.request import Request,urlopen, urlretrieve
from io import BytesIO

from bs4 import BeautifulSoup
import requests
import urllib.request
import time

from OneBuilding.climateContinents import getContinentsURL
from OneBuilding.zipScraperFunctions import scraperZip, getCountryCode

from OneBuilding.makeMetadataOneBuilding import removeFileJSON, createFileJSON


def createTaxonomyCitiesOneBuilding():

    removeFileJSON()

    documentJSON=open("Data/taxonomyCitiesOneBuilding.json", "a+")

    documentJSON.write("""{
    "cities":[]
    }
    """)

    documentJSON.close()


    # COGEMOS LAS URLs DE LOS CONTINENTES

    africaURL, asiaURL, south_AmericaURL, north_central_AmericaURL, southWest_PacificURL, europeURL, antarticaURL = getContinentsURL()

    # AKGNDSG

    urls = [africaURL, asiaURL, south_AmericaURL, north_central_AmericaURL, southWest_PacificURL, europeURL, antarticaURL]

    # urls = [0=Africa,1=Asia,2=Sudamérica,3=Norte-Centroamérica,4=Sudoeste del Pacífico,5=Europa,6=Antartica]


    allCountries = [scraperZip(url,'/index.html') for url in urls] # Lista con todos los Países del Mundo


    allCountryCodes = [getCountryCode(country) for countries in allCountries for country in countries] # Lista con todos los Códigos de los países del mundo HABRÁ QUE QUITARLA PORQUE SE COGERAN DE LAS CIUDADESS

    allCountries = [country for countries in allCountries for country in countries]

    # [print(country) for country in allCountries]

    # AQUÍ YA TENEMOS UNA LISTA CON LOS PAISES Y OTRA LISTA CON LOS CÓDIGOS DE CADA PAÍS, TIENEN LAS MISMAS POSICIONES ENTRE ELLOS
    allCities = []


    [allCities.append(scraperZip(str(country),'.zip')) for country in allCountries]



    allCities = [city for cities in allCities for city in cities]

    # print(allCities)

    allCitiesCCodes = [getCountryCode(city) for city in allCities]


    # print(allCitiesCCodes)

    
    tamaño = int(len(allCities)/2)

    allCities1 = allCities[:tamaño]
    allCities2 = allCities[tamaño:]


    allCitiesCCodes1 = allCitiesCCodes[:tamaño]
    allCitiesCCodes2 = allCitiesCCodes[tamaño:]

    # tamaño = int(len(allCities)/4)

    # allCities1 = allCities[:tamaño]
    # allCities2 = allCities[tamaño:tamaño*2]
    # allCities3 = allCities[tamaño*2:tamaño*3]
    # allCities4 = allCities[tamaño*3:]



    # allCitiesCCodes1 = allCitiesCCodes[:tamaño]
    # allCitiesCCodes2 = allCitiesCCodes[tamaño:tamaño*2]
    # allCitiesCCodes3 = allCitiesCCodes[tamaño*2:tamaño*3]
    # allCitiesCCodes4 = allCitiesCCodes[tamaño*3:]




    print('Se empieza a generar la taxonomía de OneBuilding')
    [createFileJSON(allCities1[pos],allCitiesCCodes1[pos]) for pos in range(len(allCities1))]
    print('Primera parte completada de la taxonomía de OneBuilding')
    [createFileJSON(allCities2[pos],allCitiesCCodes2[pos]) for pos in range(len(allCities2))]
    print('Segunda parte completada de la taxonomía de OneBuilding')
    # [createFileJSON(allCities3[pos],allCitiesCCodes3[pos]) for pos in range(len(allCities3))]
    # print('Tercera parte completada de la taxonomía de OneBuilding')
    # [createFileJSON(allCities4[pos],allCitiesCCodes4[pos]) for pos in range(len(allCities4))]
    # print('Cuarta parte completada y fin de la ejecución')



