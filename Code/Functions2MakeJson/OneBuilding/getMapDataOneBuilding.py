import json
import os



def removeFileJSON():
    if os.path.exists("Data/OneBuildingMapData.json"):
        os.remove("Data/OneBuildingMapData.json")
        return
    else:
        return

def getMapDataOneBuilding():

    with open("Data/taxonomyCitiesOneBuilding.json") as f:
        data = json.load(f)
        codes = [city['adm0_a3'] for city in data['cities']]
        codesNoDuplicates = list(dict.fromkeys(codes))

    f.close()

    removeFileJSON()

    trueData=open("Data/OneBuildingMapData.json", "a+")

    trueData.write("""{
        "type": "FeatureCollection",
        "features": []
        }
    """)
    trueData.close()


    with open('Data/FullMapData.json') as f:
            data = json.load(f)


    with open('Data/OneBuildingMapData.json') as g:
        dataset = json.load(g)


    [dataset['features'].append(feature) for feature in data['features'] if feature['properties']['adm0_a3'] in codesNoDuplicates]

    f.close()

    with open('Data/OneBuildingMapData.json', 'w') as g:
        json.dump(dataset, g, indent=4)


    g.close()