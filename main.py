from dotenv import load_dotenv
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

def getData(week):
    URL = f"https://sheets.googleapis.com/v4/spreadsheets/{sheetId}/values/Weekly%20Comp%20{week}!A1:Z?alt=json&key={key}"
    response = requests.get(URL)
    print(response.status_code)
    responseData = dict(response.json())
    return responseData['values']

def sortData(dataDict):
    def listData(data):
        list = []
        for i in data:
            list.append(i)
        return list
    dataList = listData(dataDict)
    print(dataList, "\n", dataList[0])
    events = []
    for i in dataList[0]:
        print(i)
        if i != "Tijdstempel" and i != "Discord username" and i != "Have you filmed your solves and do you want to show off? Drop the YouTube link here!":
            # if not in list, 
            events.append(i.split(" ")[0])
    print(events)


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
    sortData(data)
    succes = True
print("Succesfully executed program!")