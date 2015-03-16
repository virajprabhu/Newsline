import easygui as eg
from datetime import datetime, date, timedelta as td
import sys
import logging
from optparse import OptionParser
from time import time
import os
from queryMatcher import queryMatcher

def call_file(commandToBePassed) :
        print "start cmd /c python " + commandToBePassed
        os.system("start cmd /c python " + commandToBePassed)

def call_file_wait(commandToBePassed) :
        print "start /wait cmd /c python " + commandToBePassed
        os.system("start /wait cmd /c python " + commandToBePassed)

def crawl():
        msg = "Crawling from The Hindu newspaper. \n\n Enter start and end dates of articles to crawl\nOR use the default values. Year = 2014."
        title = "The Crawler"
        names = ["Start Date (dd/mm)", "End Date (dd/mm)"]
        values = ["01/10", "10/10"]
        values = eg.multenterbox(msg, title, names, values)

        if values == None:
                main()

        else:
                for value in values:
                        try:
                                value = value+"/2014"
                                datetime.strptime(value, "%d/%m/%Y")
                        except ValueError:
                                if eg.ccbox("Invalid date! Try again?", "Invalid Input"):
                                        crawl()
                                else:
                                        main()

                                return None


                d1 = date(2014, int(values[0][3:5]), int(values[0][0:2]))

                d2 = date(2014, int(values[1][3:5]), int(values[1][0:2]))

                delta = d2 - d1

                url = open("archiveSites.txt", 'w')

                for i in range(delta.days + 1):
                        newdate = d1 + td(days=i)

                        url.write("http://www.thehindu.com/archive/web/2014/"+str(newdate.month)+"/"+str(newdate.day)+"/\n")

                url.close()

                call_file("automateSpider.py")

                main()
                

def choosedir():

        value = eg.diropenbox("", "", "testData")

        if value == None:
                cluster()

        choice = eg.indexbox("Cluster at directory "+value, "Confirm Clustering", ("Continue", "Change Directory", "Return Home"))

        if choice == 0:
                call_file_wait("hac_cluster.py " + value)
                displaycluster()

        elif choice == 1:
                choosedir()

        elif choice == 2:
                main()

def displaycluster(path = "finalClusters.txt"):
        f = open(path, 'r')
        text = f.read()

        eg.textbox("Clustering Output", "hello", text, 0)

        main()



def cluster():
        msg = "Choose directory to cluster or use the default!"
        title = "The Cluster"

        choice = eg.ccbox(msg, title, ("Choose Directory", "Return Home"))
        
        if choice == 1:
                choosedir()
        else:
                main()  

def query():
        msg = "Enter your query"
        title = "Search"
        
        query = eg.enterbox(msg, title, '', True)
        if query:
                #call querying code
                (doc, returned_cluster) = queryMatcher(query, str(os.getcwd())+"\\testData")
                if(doc == None):
                        text = "No results found\n"
                else:
                        text = "Best match:\n\n" + doc + "\n\nRelated articles:\n\n" 
                        for cluster_element in returned_cluster:
                                if(doc != cluster_element):
                                        text += str(cluster_element) + "\n"
                eg.textbox("Retrieved documents", "Results", text, 0)
                main()
        else:
                main()
                
def about():
        b = eg.textbox('About the Project', 'About the Project', 'Hello. We are group 6', 0)
        main()

def main():
        a = eg.indexbox('  Information Retrieval Assignment\n\n\tCS F***\n\nNews Article Crawl and Cluster Tool\n\n  Choose an option Below\n\n', 'News Article Tool', ('Crawl', 'Cluster', 'Search', 'About', 'Exit'))
        
        if a == 0:
                crawl()
        elif a == 1:
                cluster()
        elif a == 2:
                query()
        elif a == 3:
                about()
        elif a == 4:
                sys.exit(0)

                
main()
