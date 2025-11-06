from dotenv import load_dotenv
import os
import requests
from colorama import Fore, Style

load_dotenv()

key = os.getenv("API_KEY")
sheetId = os.getenv("SHEET_ID")

#How to print in color: 
#print(f"{Fore.RED}{2}{Style.RESET_ALL}")

succes = False
week = 0
events = []
shortEvents = []
defaultLength = 0
peopleDict = {}

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
    
    def checkShortEvents(target):
        for i in shortEvents:
            if i == target:
                return True
        return False
    dataList = listData(dataDict)
    

    for i in dataList[0]:
        if i != "Tijdstempel" and i != "Discord username" and i != "Have you filmed your solves and do you want to show off? Drop the YouTube link here!":
            events.append(i.split(" ")[0].lower())
            if not checkShortEvents(i.split(" ")[0].lower()):
                shortEvents.append(i.split(" ")[0].lower())
    print(f"{Fore.BLUE}Events: {shortEvents}{Style.RESET_ALL}")
    return dataList, len(events)

def processData(events, data):
    def assignPersonalSolves(listitem, events):
        for i in range(len(listitem)):
            if i <= 1:
                continue
            elif i >= defaultLength + 2:
                break
            if peopleDict.get(listitem[1]) != None:
                if peopleDict[str(listitem[1])].get(events[i-2]) == None:
                    peopleDict[str(listitem[1])][events[i-2]] = []
                peopleDict[str(listitem[1])][events[i-2]].append(listitem[i])
            else:
                peopleDict[str(listitem[1])] = {str(events[i-2]): [listitem[i]],}

    for i in data:
        if i == data[0]:
            continue
        assignPersonalSolves(i, events)

        
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
    datalist, defaultLength = checkEvents(data)
    processData(events, datalist)
    print(peopleDict)
    succes = True

print(f"{Fore.GREEN}Succesfully executed program!{Style.RESET_ALL}")