# Author : Animesh Das , Sujay Narumanchi , Shruti Rijhwani , Viraj Prabhu
# Information Retrieval Project - Group 6
# Libraries Used : 
#               python sklearn
#               python scrapy 
#               python selenium

import os

archiveSites = []
archiveSitesFile = 'archiveSites.txt'

readingSites = open(archiveSitesFile)

for line in readingSites :
     archiveSites.append(line)

os.system('start cmd /c java -jar selenium-server-standalone-2.44.0.jar')

for archiveSite in archiveSites :
     commandToBePassed = "scrapy crawl TheHindu -a archiveSiteToCrawl=" + archiveSite + " -o DataCrawled/" + archiveSite[archiveSite.find('web/')+4 : len(archiveSite)].replace('/','') + ".json"
     print "Sending command " + commandToBePassed
     os.system("start /wait cmd /c " + commandToBePassed)
