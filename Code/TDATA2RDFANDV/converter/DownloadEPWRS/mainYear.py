from converter.DownloadEPWRS.createEPWFile import createEPWFile, createEPWZip
from converter.DownloadEPWRS.EnergyPlusScraper import continentGetLink, scrapeEP
from converter.DownloadEPWRS.getDate import getDateNoYear
from converter.DownloadEPWRS.jsonReader import jsonReaderYears
from converter.DownloadEPWRS.OneBuildingScraper import continentLinker, scrapeOB
from converter.DownloadEPWRS.extractFile import extractEPWFile
import os
import shutil



data = {
        "city" : "Madrid",
        "country" : "Spain",
        "continent" : "Europe",
        "source" : "EnergyPlus"
        }

def mainYear(data):

    if not os.path.exists('converter/DownloadEPWRS/tmpFiles'):
        os.mkdir('converter/DownloadEPWRS/tmpFiles')
    else:    
        shutil.rmtree('converter/DownloadEPWRS/tmpFiles')
        os.mkdir('converter/DownloadEPWRS/tmpFiles')

    city, country, continent, source = jsonReaderYears(data)

    if source == "EnergyPlus":
        continentLink = continentGetLink(continent)
        epwLinkList = scrapeEP(city,country,continentLink)

        createEPWFile(epwLinkList)

        finalDateList = getDateNoYear()

        return finalDateList

    elif source == "OneBuilding":
        continentLink = continentLinker(continent)
        epwLinkList = scrapeOB(city,country,continentLink)
        for url in epwLinkList:
            data,name = extractEPWFile(url)
            createEPWZip(data,name)
        
        finalDateList = getDateNoYear()

        return finalDateList

#main(data)