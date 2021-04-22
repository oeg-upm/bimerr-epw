import os


def createEPW(data,epwName):
    documentCTD=open("converter/DataStorage/" + epwName + ".epw", "a+")
    duplicated=open("converter/DataStorage/epw.epw", "a+")
    for d in data:
        documentCTD.write(d)
        duplicated.write(d)
    documentCTD.close()
    duplicated.close()
    