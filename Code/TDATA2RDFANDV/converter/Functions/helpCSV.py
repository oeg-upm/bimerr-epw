import os

def removeFile(document):
    if os.path.exists("converter/DataStorage/" + document):
        os.remove("converter/DataStorage/" + document)
        return
    else:
        return


def createFile(document):
    documentCTD=open("converter/DataStorage/" + document, "a+")
    return documentCTD # Document Created


def openFile(document):
    documentOPD=open("converter/DataStorage/" + document,'r')
    return documentOPD # Document Opened