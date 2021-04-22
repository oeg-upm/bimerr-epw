
import os
import json




def removeFileJSON():
    if os.path.exists("Data/taxonomyCitiesEnergyPlus.json"):
        os.remove("Data/taxonomyCitiesEnergyPlus.json")
        return
    else:
        return


def createFileJSON(link,countryCode):

    a_dict = {
    "link": link,
    "adm0_a3": countryCode
    }

    with open("Data/taxonomyCitiesEnergyPlus.json") as f:
        data = json.load(f)

    data['cities'].append(a_dict)

    with open("Data/taxonomyCitiesEnergyPlus.json", 'w') as f:
        json.dump(data, f, indent=4)

    f.close()