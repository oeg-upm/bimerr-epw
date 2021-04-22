import glob
import os
import time



def sendEPWVirtuoso(name):
    start_time = time.time()
    print("START")

    # lista = glob.glob('converter/Results/x*')

    # for elem in lista:
    #elem = elem.replace('converter/Results','')
    command = 'cd converter/Virtuoso \n java -jar api_zar_update.jar -p "../Results/'+ name + '.ttl" -g "https://bimerr.iot.linkeddata.es/def/weather/" -url "jdbc:virtuoso://localhost:1111" -user "dba" -pass "dba" -f "TTL"'
    os.system(command)
    # command2 = 'rm -f "converter/Results/'+ name + '.ttl"'
    # os.system(command2)

    print("END --- %s seconds ---" % ((time.time() - start_time)/60))


def sendJSONVirtuoso(name):
    start_time = time.time()
    print("START")


    command = 'cd converter/Virtuoso \n java -jar api_zar_update.jar -p "../Results/'+  name + '.ttl" -g "https://bimerr.iot.linkeddata.es/def/weather/" -url "jdbc:virtuoso://localhost:1111" -user "dba" -pass "dba" -f "TTL"'


    os.system(command)

    print("END --- %s seconds ---" % ((time.time() - start_time)/60))
