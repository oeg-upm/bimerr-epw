import json


def getJsonData(epwName):

    epwName += ".csv"

    with open('converter/DataStorage/metadata.json') as f:
        data = json.load(f)

    numberRowstoSkip = data['skipRows']
    f.close()

    for url in data['tables']:
        if url['url'] == epwName:
            headers = [str(header['name']).strip(' ').replace("'","") for header in url['tableSchema']['columns']]
            return headers, numberRowstoSkip