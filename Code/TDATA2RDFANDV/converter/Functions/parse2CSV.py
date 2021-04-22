# Función para saltar filas y para añadir encabezados
from converter.Functions.skip_addRows import skipRows_addHeader


# Funciones para borrar y crear los documentos csv
from converter.Functions.helpCSV import createFile,openFile,removeFile

# Función para recoger todos los documentos pertenecientes a la extensión epw
# from glob import glob

# documents = glob("Documents/*.epw") # Cogemos todos los documentos pertenecientes a la extensión epw

def parseToCSV(dataset,numberRowstoSkip,headers,epwName):

    contents = skipRows_addHeader(numberRowstoSkip,dataset,headers)

    city = ''+ epwName +'.csv'
    
    removeFile(city)
    documentCTD = createFile(city)

    for line in contents:
        line = line.strip('\n').split(',')
        line = str(line).strip('[]').replace("'","").replace(", ",",")
        documentCTD.write(line + '\n') 

    documentCTD.close()