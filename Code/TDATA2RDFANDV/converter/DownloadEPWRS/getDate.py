import csv
from os import listdir
from os.path import isfile, join


def getDate(year):
    year = str(year)
    finalDateList = []
    returnEPWListFiles = []

    onlyfiles = [f for f in listdir('converter/DownloadEPWRS/tmpFiles/') if isfile(join('converter/DownloadEPWRS/tmpFiles/', f))]

    for file in onlyfiles:
        with open('converter/DownloadEPWRS/tmpFiles/' + file, 'r') as f:
            data = f.read().splitlines(True)
            csvData = data[8:]
            csvData = ''.join(csvData)
            csvReader = csv.reader(csvData.splitlines(), delimiter=',')
            dateList = [row[0] for row in csvReader]
            dateList = list(dict.fromkeys(dateList))
            #dateList.insert(0,file)
            if year in dateList:
                returnEPWListFiles.append(file)
            finalDateList.append(dateList)
    finalDateList = [date for d in finalDateList for date in d]
    finalDateList = list(dict.fromkeys(finalDateList))
    finalDateList.sort()
    return finalDateList, returnEPWListFiles


def getDateNoYear():
    finalDateList = []

    onlyfiles = [f for f in listdir('converter/DownloadEPWRS/tmpFiles/') if isfile(join('converter/DownloadEPWRS/tmpFiles/', f))]

    for file in onlyfiles:
        with open('converter/DownloadEPWRS/tmpFiles/' + file, 'r') as f:
            data = f.read().splitlines(True)
            csvData = data[8:]
            csvData = ''.join(csvData)
            csvReader = csv.reader(csvData.splitlines(), delimiter=',')
            dateList = [row[0] for row in csvReader]
            dateList = list(dict.fromkeys(dateList))
            finalDateList.append(dateList)
    finalDateList = [date for d in finalDateList for date in d]
    finalDateList = list(dict.fromkeys(finalDateList))
    finalDateList.sort()
    return finalDateList