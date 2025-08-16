from dotenv import load_dotenv
import os

cacheFolder = "/Cache"
dataFolder = "/Data"

load_dotenv()

key = os.getenv("API_KEY")
mail = os.getenv("SERVICE_EMAIL")

print(key)
print(mail)
print(float(10.2))