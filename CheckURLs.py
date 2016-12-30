import urllib.request
import ssl
import pprint
from random import randint
from random import uniform
from time import strftime
import os
import datetime

outputBase = input("Where do you want the log file to go?")

if outputBase == "":
    outputBase = r"C:/Temp/"
if not os.path.exists(outputBase):
    print("Invalid directory")
logfile = open(outputBase + "logfile.txt", "a+")

pp = pprint.PrettyPrinter(indent=4)
bad_urls = list()

#default locations
lat=47.66
lon=-122.3

level=14
row=1315
col=2874

#Setting up url components
protocol_s = "https://"
protocol = "http://"

#Apache
loadbalancer = "123.12.1234.3"
ips = ("12.345.6.78", "23.456.78.9")
services = ("myFirstService, mySecondService")
tiles = ("myFirstTile, mySecondTile")

#Find out what the user needs
request = input("What type of request are you troubleshooting (s for service, t for tile, or b for both)?")
request = request.lower()

#Setup parameter to bypass certficate
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

#Functions
def logMessage():
    '''Prints a message to the console and logs in a file.'''
    print(strftime("%Y-%m-%d %H:%M:%S") + " " + str(message))
    logfile.write(strftime("%Y-%m-%d %H:%M:%S") + " " + str(message) + "\n")

def check_url():
    try:
        urllib.request.urlopen(curl, context=ctx)
        print("Succeeded")
        print("")
    except:
        print("Failed")
        print("")
        bad_urls.append(curl)

def randomize_tile(val=0):
    '''returns a (level, row, column) based on the val'''
    val = int(val)
    if val < 0:
        val *= -1
    myrand = randint(-val, val)
    return (level, row + myrand, col + myrand)

def randomize_location(val=0):
    '''returns a randomized (lat, long) based on the val'''
    val = float(val)
    if val < 0:
        val *= -1
    myrand = uniform(-val, val)
    return (lat + myrand, lon + myrand)


#Start troubleshooting
try:
    if request in ("t", "tile", "b", "both"):
        val = input("By how many tiles would you like to randomize in any direction?")

        #Check tiles
        for tile in tiles:
            #Check the load balancer
            level, row, col = randomize_tile(val)
            message = "Checking: " + tile
            print(message)
            logMessage()
            curl = protocol_s + loadbalancer  + "/" + tile + "/" + str(level) + "/" + str(row) + ":" + str(col) + "/tile.png"
            message = "Checking: " + curl
            print(message)
            logMessage()
            check_url()

            #Check the tiles at each ip address
            for ip in ips:
                level, row, col = randomize_tile(val)
                message = "Checking: " + tile + ": " + ip
                print(message)
                logMessage()
                curl = protocol + ip + "/" + tile + "/" + str(level) + "/" + str(row) + ":" + str(col) + "/tile.png"
                message = "Checking: " + curl
                print(message)
                logMessage()
                check_url()

    if request in ("s", "service", "b", "both"):
        val = input("By how many degrees would you like to randomize the location in any direction?")

        #Check the services
        for service in services:

            #Check the load balancer
            lat, lon = randomize_location(val)
            message = "Checking: " + service
            print(message)
            logMessage()
            curl = protocol + loadbalancer + ":8080/rest/" + service + "/results.xml?Data.Lat=" + str(lat) + "&Data.Long=" + str(lon)
            message = "Checking: " + curl
            print(message)
            logMessage()
            check_url()

            #Check the services at each ip address
            for ip in ips:
                lat, lon = randomize_location(val)
                message = "Checking: " + service + ": " + ip
                print(message)
                logMessage()
                curl = protocol + ip + ":8080/rest/" + service + "/results.xml?Data.Lat=" + str(lat) + "&Data.Long=" + str(lon)
                message = "Checking: " + curl
                print(message)
                logMessage()
                check_url()

finally:
    message = "-------"
    print(message)
    logMessage()
    message = "SUMMARY"
    print(message)
    logMessage()
    message = "-------"
    print(message)
    logMessage()
    if bad_urls:
        message = "Bad:"
        print(message)
        logMessage()
        pp.pprint(bad_urls)
        message = bad_urls
        logMessage()

    else:
        message = "All URLs succeeded."
        print(message)
        logMessage()

    logfile.close()
