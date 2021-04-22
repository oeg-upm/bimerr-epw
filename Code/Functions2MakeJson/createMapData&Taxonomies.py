
# Energy Plus Imports

from EnergyPlus.createTaxonomyCitiesEnergyPlus import createTaxonomyCitiesEnergyPlus
from EnergyPlus.getMapDataEnergyPlus import getMapDataEnergyPlus

# Climate One Building Imports

from OneBuilding.createTaxonomyCitiesOneBuilding import createTaxonomyCitiesOneBuilding
from OneBuilding.getMapDataOneBuilding import getMapDataOneBuilding

# Create JavaScript files  and move files Imports

from Functions2MakeJson.createJSFilesAndMove import createJSFileEnergyPlus, createJSFileOneBuilding, removeDataFromStatic, moveFilesToStatic


# Create Taxonomies
print("Energy Plus Taxonomy")
createTaxonomyCitiesEnergyPlus()
print("Climate One Building Taxonomy")
createTaxonomyCitiesOneBuilding()

# Create Map Data

print("Map Data Energy Plus")
getMapDataEnergyPlus()
print("Map Data Climate One Building")
getMapDataOneBuilding()

# Create JavaScript Files

createJSFileEnergyPlus()
print("Created Energy Plus Java Script File")
createJSFileOneBuilding()
print("Created Energy Plus Java Script File")
removeDataFromStatic()
print("Removed Duplicated Files from Static Directory")
moveFilesToStatic()
print("Moved Files to Static Directory")

# Move Files to static Directory
