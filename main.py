from dotenv import load_dotenv
import os
import requests
from colorama import Fore, Style

cacheFolder = "/Cache"
dataFolder = "/Data"

load_dotenv()

key = os.getenv("API_KEY")
mail = os.getenv("SERVICE_EMAIL")
sheetId= os.getenv("SHEET_ID")

#How to print in color: 
#print(f"{Fore.RED}{2}{Style.RESET_ALL}")

succes = False
week = 0
events = []
defaultLength = 0
shortEvents = []

# future attempt to process data
class Person:
    def __init__(self, name, eventslist):
        self.name = name
        self.events = eventslist

def getData(week):
    URL = f"https://sheets.googleapis.com/v4/spreadsheets/{sheetId}/values/Weekly%20Comp%20{week}!A1:Z?alt=json&key={key}"
    response = requests.get(URL)
    print(f"{Fore.GREEN if response.status_code == 200 else Fore.RED}Response code:, {response.status_code}{Style.RESET_ALL}")
    responseData = dict(response.json())
    return responseData['values']

def checkEvents(dataDict):
    def listData(data):
        list = []
        for i in data:
            list.append(i)
        return list
    dataList = listData(dataDict)

    events, shortEvents = [], []
    for i in dataList[0]:
        if i != "Tijdstempel" and i != "Discord username" and i != "Have you filmed your solves and do you want to show off? Drop the YouTube link here!":
            events.append(i.split(" ")[0].lower())
            if i not in shortEvents:
                shortEvents.append(i.split(" ")[0].lower())
            
    print(f"{Fore.BLUE}Events: {shortEvents}{Style.RESET_ALL}")
    return dataList, len(events)

# def processData(events, data):
#     def assignPersonalSolves(listitem, events):
#         for i in range(len(listitem)):
#             if i <= 1:
#                 continue
#             elif i >= defaultLength:
#                 break
#                 #fmc vanishes
#             print(3, peopleDict.get(listitem[1]))
#             if peopleDict.get(listitem[1]) != None:
#                 if peopleDict[str(listitem[1])].get(events[i-2]) == None:
#                     peopleDict[str(listitem[1])][events[i-2]] = []
#                 peopleDict[str(listitem[1])][events[i-2]].append(listitem[i])
#             else:
#                 peopleDict[str(listitem[1])][events[i-2]] = [listitem[i]]
    
#     def calculateAverages(person, events):
#         def convertToFloat(timelist):
#             print(timelist)
        
#         eventsHad = []
#         print(person)
#         for event in events:
#             if event in eventsHad:
#                 continue
#             eventsHad.append(event)
#             convertToFloat(peopleDict[str(person)].get(str(event)))
    
#     for i in data:
#         if i == data[0]:
#             continue
#         assignPersonalSolves(i, events)
#         print(i)
#     for person in peopleDict:
#         print(3, peopleDict.get(person))
#         calculateAverages(person, events)
        
while succes == False: 
    while True:
        tempweek = input("What is the new weekly number? #")
        try: 
            week = int(tempweek)
        except:
            print("Not a valid week number! Try again")
            continue
        break
    data = getData(week)
    # print(1, data)
    datalist, defaultLength = checkEvents(data)
    # print(2, data, defaultLength)
    # processData(events, datalist)
    succes = True

print(f"{Fore.GREEN}Succesfully executed program!{Style.RESET_ALL}")