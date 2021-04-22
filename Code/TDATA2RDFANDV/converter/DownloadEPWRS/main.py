from converter.DownloadEPWRS.createEPWFile import createEPWFile, createEPWZip
from converter.DownloadEPWRS.EnergyPlusScraper import continentGetLink, scrapeEP
from converter.DownloadEPWRS.getDate import getDate
from converter.DownloadEPWRS.jsonReader import jsonReader
from converter.DownloadEPWRS.OneBuildingScraper import continentLinker, scrapeOB
from converter.DownloadEPWRS.extractFile import extractEPWFile
import os
import shutil



data = {
        "city" : "Madrid",
        "country" : "Spain",
        "continent" : "Europe",
        "year" : 1984,
        "source" : "EnergyPlus"
        }

def main(data):

    linkList = []

    if not os.path.exists('converter/DownloadEPWRS/tmpFiles'):
        os.mkdir('converter/DownloadEPWRS/tmpFiles')
    else:    
        shutil.rmtree('converter/DownloadEPWRS/tmpFiles')
        os.mkdir('converter/DownloadEPWRS/tmpFiles')

    city, country, continent, year, source, out = jsonReader(data)


    if source == "EnergyPlus":
        continentLink = continentGetLink(continent)

        epwLinkList = scrapeEP(city,country,continentLink)

        createEPWFile(epwLinkList)

        finalDateList, returnEPWListFiles = getDate(year)

        if returnEPWListFiles != []:
            if out == "file":
                return returnEPWListFiles
            elif out == "link":
                for link in epwLinkList:
                    link2 = link.split("/")
                    link2 = link2[-1]
                    if link2 in returnEPWListFiles:
                        linkList.append(link)
                return linkList
        else:
            return finalDateList


    elif source == "OneBuilding":
        continentLink = continentLinker(continent)
        epwLinkList = scrapeOB(city,country,continentLink)

        for url in epwLinkList:
            data,name = extractEPWFile(url)
            createEPWZip(data,name)
        
        finalDateList, returnEPWListFiles = getDate(year)

        if returnEPWListFiles != []:
            if out == "file":
                return returnEPWListFiles
            elif out == "link":
                for link in epwLinkList:
                    link2 = link.split("/")
                    link2 = link2[-1].replace(".zip",".epw")
                    if link2 in returnEPWListFiles:
                        linkList.append(link)
                return linkList
        else:
            return finalDateList

#main(data)