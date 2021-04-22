import zipfile, urllib, os
from urllib.request import Request,urlopen, urlretrieve
from io import BytesIO


def extractEPWFile(url):

    resp = urlopen(url)
    zipfiles = zipfile.ZipFile(BytesIO(resp.read()))
    file = zipfiles.namelist()[2]

    epwFile = [file for file in zipfiles.namelist() if file.endswith('.epw')]

    file = epwFile[0]

    data = zipfiles.open(file).readlines() # Información perteneciente al archivo EPW
    data = [d.decode("utf-8") for d in data]

    name = url.split('/')[-1].replace('.zip','')

    zipfiles.close()

    return data, name

url = 'http://climate.onebuilding.org/WMO_Region_6_Europe/ESP_Spain/MD_Madrid/ESP_MD_Madrid-Cuatro.Vientos.AP.082230_TMYx.2004-2018.zip'

#extractEPWFile(url)