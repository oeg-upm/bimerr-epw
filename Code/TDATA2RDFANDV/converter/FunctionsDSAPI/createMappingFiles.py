import json
import os



def createDSAPIMappings(json_name,json_path): # PASAR COMO PARÁMETRO JSON_NAME PARA PODER HACER LO DE LOS DIRECTORIOS
    removeLocationSource()
    removeCurrentlySource()
    removeDailySource()
    removeHourlySource()
    removeMinutelySource()
    createLocationSource(json_name)
    createCurrentlySource(json_name)
    createMinutelySource(json_name)
    createHourlySource(json_name)
    createDailySource(json_name)


def removeCurrentlySource():# MappingsDSAPIStorage tendrá que ser el nombre del directorio asignado a la persona --> borrarlo al cabo de una hora
    if os.path.exists("converter/MappingsDSAPIStorage/currently_data_source.json"):
        os.remove("converter/MappingsDSAPIStorage/currently_data_source.json")
        return
    else:
        return

def removeLocationSource():# MappingsDSAPIStorage tendrá que ser el nombre del directorio asignado a la persona --> borrarlo al cabo de una hora
    if os.path.exists("converter/MappingsDSAPIStorage/location_data_source.json"):
        os.remove("converter/MappingsDSAPIStorage/location_data_source.json")
        return
    else:
        return


def removeDailySource():# MappingsDSAPIStorage tendrá que ser el nombre del directorio asignado a la persona --> borrarlo al cabo de una hora
    if os.path.exists("converter/MappingsDSAPIStorage/daily_data_source.json"):
        os.remove("converter/MappingsDSAPIStorage/daily_data_source.json")
        return
    else:
        return


def removeHourlySource():# MappingsDSAPIStorage tendrá que ser el nombre del directorio asignado a la persona --> borrarlo al cabo de una hora
    if os.path.exists("converter/MappingsDSAPIStorage/hourly_data_source.json"):
        os.remove("converter/MappingsDSAPIStorage/hourly_data_source.json")
        return
    else:
        return


def removeMinutelySource():# MappingsDSAPIStorage tendrá que ser el nombre del directorio asignado a la persona --> borrarlo al cabo de una hora
    if os.path.exists("converter/MappingsDSAPIStorage/minutely_data_source.json"):
        os.remove("converter/MappingsDSAPIStorage/minutely_data_source.json")
        return
    else:
        return


def createCurrentlySource(json_name): # DSAPIDataStorage tendrá que ser una carpeta dentro de un directorio con el nombre del fichero asignado a la persona --> borrarlo al cabo de una hora
    json_file = {}
    json_file['datasources'] = []
    json_file['datasources'].append({
          "id" : "Json Values current",
          "type" : "JsonDatasource",
          "arguments" : ["$.current[*]"],
          "connector"  : {
           "arguments" : ["../DSAPIDataStorage/" + json_name + ".json"],
           "type" : "LocalFileConnector"
          }
        })
    document = open("converter/MappingsDSAPIStorage/currently_data_source.json", "w")
    json.dump(json_file, document, indent=4)

def createLocationSource(json_name): # DSAPIDataStorage tendrá que ser una carpeta dentro de un directorio con el nombre del fichero asignado a la persona --> borrarlo al cabo de una hora
    json_file = {}
    json_file['datasources'] = []
    json_file['datasources'].append({
          "id" : "Json Values Location",
          "type" : "JsonDatasource",
          "arguments" : ["$.location[*]"],
          "connector"  : {
           "arguments" : ["../DSAPIDataStorage/" + json_name + ".json"],
           "type" : "LocalFileConnector"
          }
        })
    document = open("converter/MappingsDSAPIStorage/location_data_source.json", "w")
    json.dump(json_file, document, indent=4)

def createMinutelySource(json_name): # DSAPIDataStorage tendrá que ser una carpeta dentro de un directorio con el nombre del fichero asignado a la persona --> borrarlo al cabo de una hora
    json_file = {}
    json_file['datasources'] = []
    json_file['datasources'].append({
          "id" : "Json Values minutely",
          "type" : "JsonDatasource",
          "arguments" : ["$.minutely[*]"],
          "connector"  : {
           "arguments" : ["../DSAPIDataStorage/" + json_name + ".json"],
           "type" : "LocalFileConnector"
          }
        })
    document = open("converter/MappingsDSAPIStorage/minutely_data_source.json", "w")
    json.dump(json_file, document, indent=4)

def createHourlySource(json_name): # DSAPIDataStorage tendrá que ser una carpeta dentro de un directorio con el nombre del fichero asignado a la persona --> borrarlo al cabo de una hora
    json_file = {}
    json_file['datasources'] = []
    json_file['datasources'].append({
          "id" : "Json Values hourly",
          "type" : "JsonDatasource",
          "arguments" : ["$.hourly[*]"],
          "connector"  : {
           "arguments" : ["../DSAPIDataStorage/" + json_name + ".json"],
           "type" : "LocalFileConnector"
          }
        })
    document = open("converter/MappingsDSAPIStorage/hourly_data_source.json", "w")
    json.dump(json_file, document, indent=4)

def createDailySource(json_name): # DSAPIDataStorage tendrá que ser una carpeta dentro de un directorio con el nombre del fichero asignado a la persona --> borrarlo al cabo de una hora
    json_file = {}
    json_file['datasources'] = []
    json_file['datasources'].append({
          "id" : "Json Values daily",
          "type" : "JsonDatasource",
          "arguments" : ["$.daily[*]"],
          "connector"  : {
           "arguments" : ["../DSAPIDataStorage/" + json_name + ".json"],
           "type" : "LocalFileConnector"
          }
        })
    document = open("converter/MappingsDSAPIStorage/daily_data_source.json", "w")
    json.dump(json_file, document, indent=4)


