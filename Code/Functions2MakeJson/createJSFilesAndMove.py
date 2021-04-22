import json
import os
import shutil

def removeFileJSEnergyPlus():
    if os.path.exists("Data/EnergyPlusMapData.js"):
        os.remove("Data/EnergyPlusMapData.js")
        return
    else:
        return


def removeFileJSOneBuilding():
    if os.path.exists("Data/OneBuildingMapData.js"):
        os.remove("Data/OneBuildingMapData.js")
        return
    else:
        return


def createJSFileEnergyPlus():

    removeFileJSEnergyPlus()

    with open('Data/EnergyPlusMapData.json') as json_file:
        data = json.load(json_file)

    document_js=open("Data/EnergyPlusMapData.js", "a+")

    document_js.write("""var geoLocations1 = """)

    json.dump(data, document_js, ensure_ascii=False, indent=4)

    document_js.close()
    json_file.close()


def createJSFileOneBuilding():

    removeFileJSOneBuilding()

    with open('Data/OneBuildingMapData.json') as json_file:
        data = json.load(json_file)

    document_js=open("Data/OneBuildingMapData.js", "a+")

    document_js.write("""var geoLocations = """)

    json.dump(data, document_js, ensure_ascii=False, indent=4)

    document_js.close()
    json_file.close()


def removeDataFromStatic():

    files = ['../TDATA2RDFANDV/converter/static/converter/taxonomyCitiesEnergyPlus.json', '../TDATA2RDFANDV/converter/static/converter/taxonomyCitiesOneBuilding.json', '../TDATA2RDFANDV/converter/static/converter/EnergyPlusMapData.js', '../TDATA2RDFANDV/converter/static/converter/OneBuildingMapData.js']

    for file in files:
        if os.path.exists(file):
            os.remove(file)



def moveFilesToStatic():
    files = ['Data/EnergyPlusMapData.js', 'Data/OneBuildingMapData.js', 'Data/taxonomyCitiesEnergyPlus.json', 'Data/taxonomyCitiesOneBuilding.json']
    for file in files:
        shutil.copy(file, '../TDATA2RDFANDV/converter/static/converter/')




createJSFileEnergyPlus()
createJSFileOneBuilding()

removeDataFromStatic()
moveFilesToStatic()