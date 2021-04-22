import urllib
from urllib.request import Request,urlopen, urlretrieve
from io import BytesIO
import re

urls = ['https://energyplus.net/weather-download/europe_wmo_region_6/ESP//ESP_Madrid.082210_IWEC/ESP_Madrid.082210_IWEC.epw', 'https://energyplus.net/weather-download/europe_wmo_region_6/ESP//ESP_Madrid.082210_SWEC/ESP_Madrid.082210_SWEC.epw']

def splitUrlName(url):
    name = url.split('/')
    name = name[-1]
    return name


def createEPWFile(urls):
    for url in urls:
        req = Request(url, headers = {"User-Agent": "Mozilla/5.0"})
        resp = urlopen(req).read()
        data = resp.decode("utf-8", 'ignore')
        name = splitUrlName(url)
        f = open('converter/DownloadEPWRS/tmpFiles/'+name,"a+")
        f.write("\n".join(data.splitlines()))
        f.close()

def createEPWZip(data,name):
    f=open("converter/DownloadEPWRS/tmpFiles/" + name + ".epw", "a+")
    f.write(re.sub('\r?\n','\n',"".join(data)))
    f.close()




# MAIN
#createEPWFile(urls)