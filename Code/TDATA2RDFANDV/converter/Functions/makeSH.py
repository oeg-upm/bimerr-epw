import os
import shutil

def makeSHEPW(name): # CHANGE
    command = "cd converter/RMLMapper \n java -jar rmlmapper-4.8.1.jar -m '../MappingsEPWStorage/mapping.rml' -o '../Results/" + name + ".ttl' -s 'turtle'"

    os.system(command)


    src_dir="converter/Results/" + name + ".ttl"
    dst_dir="converter/Results/rdf.ttl"
    shutil.copy(src_dir,dst_dir)
        






def makeSHJSON(name): # CHANGE

    command = "cd converter/Helio \n java -jar helio.jar -p '../MappingsDSAPIStorage' -o '../Results/" + name + ".ttl' -s 'turtle'"

    os.system(command)

    print(os.getcwd())
    src_dir="converter/Results/" + name + ".ttl"
    dst_dir="converter/Results/rdf.ttl"
    shutil.copy(src_dir,dst_dir)

    