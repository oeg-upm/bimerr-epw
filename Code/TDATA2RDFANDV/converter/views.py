from rest_framework.schemas import AutoSchema
import coreapi
from .models import downlEPW
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
import json
import shutil
import pathlib
import glob
import os
from os import listdir
from os.path import isfile, join

from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from rest_framework import status

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Create your views here.


# TAKE DATA FUNCTIONS

# take data from json['code']
from converter.Functions.takeDataJson import takeData
# extract the epw file from url zip
from converter.Functions.extractFile import extractEPWFile, extractEPWData
from converter.Functions.makeCSVW import removeFileJSON, createFileJson  # make metadata
# get json from created csvw
from converter.Functions.getDataFromJson import getJsonData
from converter.Functions.parse2CSV import parseToCSV  # parse epw file to csv
from converter.Functions.makeSH import makeSHEPW, makeSHJSON
from converter.Functions.createEPWFile import createEPW
from converter.Functions.createJSONFile import create8LinesJson
#from converter.Functions.sendVirtuoso import sendEPWVirtuoso, sendJSONVirtuoso
from converter.Functions.createMappingFiles import createMappings
from converter.FunctionsDSAPI.request import makeRequest
from converter.FunctionsDSAPI.createMappingFiles import createDSAPIMappings
from converter.DownloadEPWRS.main import main
from converter.DownloadEPWRS.zipdir import zipdir
from converter.DownloadEPWRS.mainYear import mainYear
# directory to storage data == DataStorage


def index(request):
    return render(request, 'converter/page.html')



@csrf_exempt  # ONEBUILDIND.ORG WEATHER MAP
def mapData(request):
    if request.method == "POST":
        response = json.loads(request.body)
        data = takeData(response)
        flag = False

        while flag == False:
            if not os.getcwd().endswith("TDATA2RDFANDV"):
                os.chdir("..")
            else:
                flag = True

        jsonFile = open(
            'converter/static/converter/taxonomyCitiesOneBuilding.json')
        jsonData = json.load(jsonFile)

        jsonDictionary = {'cities': []}

        [jsonDictionary['cities'].append({'adm0_a3': city['adm0_a3'], 'link':city['link']})
         for city in jsonData['cities'] if city['adm0_a3'] == data]

        jsonFile.close()

        # print(jsonDictionary)

        return JsonResponse(jsonDictionary, safe=False)


@csrf_exempt  # ENERGY PLUS WEATHER MAP
def mapDataEnergyPlus(request):
    if request.method == "POST":
        response = json.loads(request.body)
        data = takeData(response)

        flag = False

        while flag == False:
            if not os.getcwd().endswith("TDATA2RDFANDV"):
                os.chdir("..")
            else:
                flag = True


        jsonFile = open(
            'converter/static/converter/taxonomyCitiesEnergyPlus.json')
        jsonData = json.load(jsonFile)
        # print(jsonData)

        jsonDictionary = {'cities': []}

        [jsonDictionary['cities'].append({'adm0_a3': city['adm0_a3'], 'link':city['link']})
         for city in jsonData['cities'] if city['adm0_a3'] == data]

        jsonFile.close()
        # print(jsonDictionary)

        return JsonResponse(jsonDictionary, safe=False)


@csrf_exempt  # EXTRACT DATA FROM LINK FROM ONEBUILDING.ORG WEATHER
def extract_Convert(request):
    if request.method == "POST":

        flag = False

        while flag == False:
            if not os.getcwd().endswith("TDATA2RDFANDV"):
                os.chdir("..")
            else:
                flag = True

        #Clean Storage

        shutil.rmtree('converter/Results/', ignore_errors=True)
        pathlib.Path(
            "converter/Results/").mkdir(parents=True, exist_ok=True)

        shutil.rmtree('converter/DataStorage/', ignore_errors=True)
        pathlib.Path(
            "converter/DataStorage").mkdir(parents=True, exist_ok=True)
        
        shutil.rmtree('converter/static/converter/Downloads/', ignore_errors=True)
        pathlib.Path(
            "converter/static/converter/Downloads/").mkdir(parents=True, exist_ok=True)

        

        response = json.loads(request.body)
        link = takeData(response)
        # get data from EPW file that is inside Zip File
        data = extractEPWFile(link)
        removeFileJSON()  # Remove csvw.json
        # last replace is for a problem with Helio
        epwName = link.split('/')[-1].replace('.zip', '').replace(".", "-").replace("%20","_")
        createFileJson(data, epwName)  # Create csvw.json

        headers, numberRowstoSkip = getJsonData(epwName)

        # Get the headers properly

        headers = str(str(headers).strip('[]').replace(
            "'", "").split(', ')).strip('[]').replace(", ", ",")

        headers = str(headers).strip('[]').replace("'", "").replace(", ", ",")

        # Parse all data to CSV

        parseToCSV(data, numberRowstoSkip, headers,
                   epwName)  # parse data to csv

        # Get the epw file as a file
        createEPW(data, epwName)

        # Create json with data

        create8LinesJson(data, numberRowstoSkip, epwName)

        createMappings(epwName)

        # Create mapping files with epwName

        print('Starting Transformation')

        makeSHEPW(epwName)  # IMPORTANTE DESCOMENTAR PARA ENSEÑAR HELIO

        #print('Sending to Virtuoso')

        #sendEPWVirtuoso(epwName)

        if not os.getcwd().endswith("DataStorage"):
            os.chdir("converter/DataStorage")

        dictionary = {}

        shutil.move("../Results/rdf.ttl", '../../converter/static/converter/Downloads/')
        shutil.move("epw.epw", '../../converter/static/converter/Downloads/')

        for file in glob.glob("../Results/*.ttl"):
            for epw in glob.glob("*.epw"):
                dictionary = {
                    'METADATA': "static/converter/metadata.json",
                    'CSV': "static/converter/" + epwName + ".csv",
                    'EPW': "static/converter/" + epw,
                    'RDF': "static/converter/" + file
                }
        
        return JsonResponse(dictionary, safe=False)


@csrf_exempt
def extract_ConvertEnergyPlus(request):
    if request.method == "POST":

        flag = False

        while flag == False:
            if not os.getcwd().endswith("TDATA2RDFANDV"):
                os.chdir("..")
            else:
                flag = True

        # Clean Storage

        shutil.rmtree('converter/Results/', ignore_errors=True)
        pathlib.Path(
            "converter/Results/").mkdir(parents=True, exist_ok=True)


        shutil.rmtree('converter/DataStorage/', ignore_errors=True)
        pathlib.Path(
            "converter/DataStorage").mkdir(parents=True, exist_ok=True)

        shutil.rmtree('converter/static/converter/Downloads/', ignore_errors=True)
        pathlib.Path(
            "converter/static/converter/Downloads/").mkdir(parents=True, exist_ok=True)

        response = json.loads(request.body)
        link = takeData(response)
        data = extractEPWData(link)
        removeFileJSON()  # Remove csvw.json
        # last replace is for a problem with Helio
        epwName = link.split('/')[-1].replace('.epw', '').replace(".", "-").replace("%20","_").replace("%20","_")
        createFileJson(data, epwName)  # Create csvw.json

        headers, numberRowstoSkip = getJsonData(epwName)

        # Get the headers properly

        headers = str(str(headers).strip('[]').replace(
            "'", "").split(', ')).strip('[]').replace(", ", ",")

        headers = str(headers).strip('[]').replace("'", "").replace(", ", ",")

        # Parse all data to CSV

        parseToCSV(data, numberRowstoSkip, headers,
                   epwName)  # parse data to csv

        # Get the epw file as a file
        createEPW(data, epwName)

        # Create json with data

        create8LinesJson(data, numberRowstoSkip, epwName)

        # Create mapping files with epwName


        print(os.getcwd())

        createMappings(epwName)

        print('Starting Transformation')

        makeSHEPW(epwName)  # IMPORTANTE DESCOMENTAR PARA ENSEÑAR HELIO

        # print('Sending to Virtuoso')

        # sendEPWVirtuoso(epwName)

        if not os.getcwd().endswith("DataStorage"):
            os.chdir("converter/DataStorage")

        dictionary = {}


        shutil.move("../Results/rdf.ttl", '../../converter/static/converter/Downloads/')
        shutil.move("epw.epw", '../../converter/static/converter/Downloads/')

        for file in glob.glob("../Results/*.ttl"):
            for epw in glob.glob("*.epw"):
                dictionary = {
                    'METADATA': "static/converter/metadata.json",
                    'CSV': "static/converter/" + epwName + ".csv",
                    'EPW': "static/converter/" + epw,
                    'RDF': "static/converter/" + file
                }

        return JsonResponse(dictionary, safe=False)


@csrf_exempt
def extract_ConvertDarkSkyAPI(request):
    if request.method == "POST":
        
        shutil.rmtree('converter/Results/', ignore_errors=True)
        pathlib.Path(
            "converter/Results/").mkdir(parents=True, exist_ok=True)

        shutil.rmtree('converter/static/converter/Downloads/', ignore_errors=True)
        pathlib.Path(
            "converter/static/converter/Downloads/").mkdir(parents=True, exist_ok=True)

        shutil.rmtree('converter/DSAPIDataStorage/', ignore_errors=True)
        pathlib.Path(
            "converter/DSAPIDataStorage").mkdir(parents=True, exist_ok=True)


        response = json.loads(request.body)

        flag = False

        while flag == False:
            if not os.getcwd().endswith("TDATA2RDFANDV"):
                os.chdir("..")
            else:
                flag = True

        json_data, json_name, json_path = makeRequest(
            response['latitude'], response['longitude'])
        createDSAPIMappings(json_name, json_path)
        makeSHJSON(json_name)

        #sendJSONVirtuoso(json_name)

        shutil.move("converter/Results/rdf.ttl", 'converter/static/converter/Downloads/')

        return JsonResponse(json_data, safe=False)


@swagger_auto_schema(
    method='POST',
    operation_description="Obtain EPW files from one specific year.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'city': openapi.Schema(type=openapi.TYPE_STRING, example="Madrid"),
            'country': openapi.Schema(type=openapi.TYPE_STRING, example="Spain"),
            'continent': openapi.Schema(type=openapi.TYPE_STRING, example="Europe"),
            'year': openapi.Schema(type=openapi.TYPE_INTEGER, example="1989"),
            'source': openapi.Schema(type=openapi.TYPE_STRING, example="EnergyPlus or OneBuilding"),
            'output': openapi.Schema(type=openapi.TYPE_STRING, example="file or link"),
        }
    ),
    responses={
        200: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            description="If the year is in the EPW files, the response will be a zip file (if you want to download this file you have to do the curl call with an external terminal writing at the end --output 'EPW.zip'). If the year is not in the EPW files, the response will be a json with the years that these files contain, as below you can see:",
            properties={
                'info': openapi.Schema(type=openapi.TYPE_STRING, example="Your year does not coincide with any of the years established within the epw files, please select one of the following"),
                'years': openapi.Schema(type=openapi.TYPE_STRING, example="1985,1986,1987,1989,1990,1991,1993,1994,1999"),
            },
        ),
    }
)
@api_view(['POST'])
@csrf_exempt
def downloadEPW(request):
    if request.method == "POST":

        flag = False

        while flag == False:
            if not os.getcwd().endswith("TDATA2RDFANDV"):
                os.chdir("..")
            else:
                flag = True

        response = request.data
        resultList = main(response)
        if resultList[0].endswith('.epw') and not resultList[0].startswith("http"):
            onlyfiles = [f for f in listdir(
                'converter/DownloadEPWRS/tmpFiles') if isfile(join('converter/DownloadEPWRS/tmpFiles/', f))]
            os.mkdir('converter/DownloadEPWRS/tmpFiles/EPW')
            for result in resultList:
                shutil.move("converter/DownloadEPWRS/tmpFiles/"+result,
                            "converter/DownloadEPWRS/tmpFiles/EPW/"+result)
            zipdir("converter/DownloadEPWRS/tmpFiles/EPW/",
                   "converter/DownloadEPWRS/tmpFiles/EPW.zip", True)
            zip_file = open("converter/DownloadEPWRS/tmpFiles/EPW.zip", 'rb')
            return FileResponse(zip_file)

        elif resultList[0].startswith("http"):
            resultList = ','.join(resultList)
            dictionary = {
                'info': 'The links of the epw files that you have requested are as follows:',
                'links': resultList
            }
            return JsonResponse(dictionary, safe=False)

        else:
            resultList = ','.join(resultList)
            dictionary = {
                'info': 'Your year does not coincide with any of the years established within the epw files, please select one of the following',
                'years': resultList
            }

            return JsonResponse(dictionary, safe=False)


@swagger_auto_schema(
    method='POST',
    operation_description=" Obtain the years contained in the EPW documents belonging to the city indicated.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'city': openapi.Schema(type=openapi.TYPE_STRING, example="Madrid"),
            'country': openapi.Schema(type=openapi.TYPE_STRING, example="Spain"),
            'continent': openapi.Schema(type=openapi.TYPE_STRING, example="Europe"),
            'source': openapi.Schema(type=openapi.TYPE_STRING, example="EnergyPlus or OneBuilding"),
        }
    ),
    responses={
        200: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'years': openapi.Schema(type=openapi.TYPE_STRING, example="1985,1986,1987,1989,1990,1991,1993,1994,1999"),
            },
        ),
    }
)
@api_view(['POST'])
@csrf_exempt
def getEPWYears(request):
    if request.method == "POST":

        flag = False

        while flag == False:
            if not os.getcwd().endswith("TDATA2RDFANDV"):
                os.chdir("..")
            else:
                flag = True

        response = request.data
        resultList = mainYear(response)
        resultList = ','.join(resultList)
        dictionary = {
            'years': resultList
        }
        return JsonResponse(dictionary, safe=False)
