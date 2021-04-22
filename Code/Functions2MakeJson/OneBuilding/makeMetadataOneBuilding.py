
import os
import json




def removeFileJSON():
    if os.path.exists("Data/taxonomyCitiesOneBuilding.json"):
        os.remove("Data/taxonomyCitiesOneBuilding.json")
        return
    else:
        return


def createFileJSON(link,countryCode):

    a_dict = {
    "link": link,
    "adm0_a3": countryCode
    }

    with open("Data/taxonomyCitiesOneBuilding.json") as f:
        data = json.load(f)

    data['cities'].append(a_dict)

    with open("Data/taxonomyCitiesOneBuilding.json", 'w') as f:
        json.dump(data, f, indent=4)
