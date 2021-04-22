
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

    zipfiles.close()

    return data

def extractEPWData(url):
    headers = {'User-Agent': 'Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
    reg_url = url
    req = Request(url=reg_url, headers=headers) 
    data = urlopen(req)
    lines = data.readlines()
    data = [d.decode("latin-1") for d in lines]
    return data