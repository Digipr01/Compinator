from dotenv import load_dotenv
from collections import defaultdict
import os
import requests
from colorama import Fore, Style

cacheFolder = "/Cache"
dataFolder = "/Data"

load_dotenv()

key = os.getenv("API_KEY")
mail = os.getenv("SERVICE_EMAIL")
sheetId= os.getenv("SHEET_ID")

# don't forget to update USB .env file when adding more variables

succes = False
week = 0
events = []
peopleDict = defaultdict(dict)
defaultLength = 0

#How to print in color: 
#print(f"{Fore.RED}{2}{Style.RESET_ALL}")

def getData(week):
    URL = f"https://sheets.googleapis.com/v4/spreadsheets/{sheetId}/values/Weekly%20Comp%20{week}!A1:Z?alt=json&key={key}"
    response = requests.get(URL)
    print(f"{Fore.GREEN if int(response.status_code) == 200 else Fore.RED}Response code: {response.status_code}{Style.RESET_ALL}")
    responseData = dict(response.json())
    return responseData['values']

def checkEvents(dataDict):
    def listData(data):
        list = []
        for i in data:
            list.append(i)
        return list
    dataList = listData(dataDict)

    events = []
    for i in dataList[0]:
        if i != "Tijdstempel" and i != "Discord username" and i != "Have you filmed your solves and do you want to show off? Drop the YouTube link here!":
            events.append(i.split(" ")[0])
            
    print(f"{Fore.BLUE}Events: {events}{Style.RESET_ALL}")
    return events, dataList, len(events)

def processData(events, data):
    def assignPersonalSolves(listitem, events):
        print(f"{Fore.RED}Length: {len(listitem)} list: {listitem}{Style.RESET_ALL}")
        for i in range(len(listitem)):
            if i <= 1:
                continue
            elif i >= defaultLength:
                break
                #fmc vanishes
            print(f"{Fore.YELLOW}{i}{Style.RESET_ALL}")
            if peopleDict.get(listitem[1]) != None:
                if peopleDict[str(listitem[1])].get(events[i-2]) == None:
                    peopleDict[str(listitem[1])][events[i-2]] = []
                peopleDict[str(listitem[1])][events[i-2]].append(listitem[i])
            else:
                peopleDict[str(listitem[1])][events[i-2]] = [listitem[i]]
    
    def calculateAverages(person, events):
        def convertToFloat(timelist):
            print(f"{Fore.MAGENTA}{timelist}{Style.RESET_ALL}")
        
        eventsHad = []
        print(f"{Fore.BLUE}{person}{Style.RESET_ALL}")
        for event in events:
            if event in eventsHad:
                continue
            eventsHad.append(event)
            convertToFloat(peopleDict[str(person)].get(str(event)))
    
    for i in data:
        if i == data[0]:
            continue
        assignPersonalSolves(i, events)
    for person in peopleDict:
        calculateAverages(person, events)
        
while succes == False:
    prevWeek = week 
    while week == prevWeek:
        tempweek = input("What is the new weekly number? #")
        try: 
            week = int(tempweek)
        except:
            print("Not a valid week number! Try again")
            continue
    data = getData(week)
    events, datalist, defaultLength = checkEvents(data)
    processData(events, datalist)
    
    succes = True

print(f"{Fore.GREEN}Succesfully executed program!{Style.RESET_ALL}")