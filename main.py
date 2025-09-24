from dotenv import load_dotenv
from collections import defaultdict
import os
import requests

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

def getData(week):
    URL = f"https://sheets.googleapis.com/v4/spreadsheets/{sheetId}/values/Weekly%20Comp%20{week}!A1:Z?alt=json&key={key}"
    response = requests.get(URL)
    print("Response code:", response.status_code)
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
            
    print("Events:", events)
    return events, dataList, len(events)

def processData(events, data):
    def assignPersonalSolves(listitem, events):
        for i in range(len(listitem)):
            if i <= 1:
                continue
            elif i >= defaultLength:
                break
            if peopleDict.get(listitem[1]) != None:
                if peopleDict[str(listitem[1])].get(events[i-2]) == None:
                    peopleDict[str(listitem[1])][events[i-2]] = []
                peopleDict[str(listitem[1])][events[i-2]].append(listitem[i])
            else:
                peopleDict[str(listitem[1])][events[i-2]] = [listitem[i]]
    for i in data:
        if i == data[0]:
            continue
        assignPersonalSolves(i, events)
        
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
    succes = True
    processData(events, datalist)
    print(peopleDict)

print("Succesfully executed program!")