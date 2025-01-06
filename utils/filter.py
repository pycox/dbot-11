import json
from openpyxl import load_workbook, Workbook
import os
from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb://localhost:27017/")
db = client["dbot"]
collection = db["leads"]

histDir = r"history.json"

ctrXlDir = r"clients.xlsx"

dbXlDir = r"data.xlsx"

cashData = {}

rowData = []


def ensure_history_file_exists():
    if not os.path.exists(histDir):
        with open(histDir, "w") as file:
            json.dump({}, file)


def getBotSpeed():
    try:
        wb = load_workbook(ctrXlDir)
        ws = wb.active
        speed = ws["F2"].value

        if isinstance(speed, (int, float)):
            return int(speed)
        else:
            return 4
    except FileNotFoundError:
        return 4
    except ValueError:
        return 4


def getLocations(location=None):
    location_data = {
        "UK": (
            "UK",
            "UNITED KINGDOM",
            "ENG",
            "GB",
            "United Kingdom",
            "London",
            "LONDON",
            "Bristol",
            "BRISTOL",
            "Tamworth",
            "TAMWORTH",
            "Brighton",
            "BRIGHTON",
            "England",
            "ENGLAND",
            "Birmingham",
            "BIRMINGHAM",
            "Cambridge",
            "CAMBRIDGE",
            "Manchester",
            "MANCHESTER",
            "Scotland",
            "SCOTLAND",
            "Leeds",
            "LEEDS",
            "Belfast",
            "Liverpool",
            "Newcastle",
            "Warrington",
            "Mayfair",
            "Cambridge",
            "Reading",
            "Salford",
            "Twickenham",
            "Wembley",
            "Southampton",
            "Borough",
            "BOROUGH",
        ),
        "US": (
            "US",
            "U.S.",
            "USA",
            "UNITED STATES",
            "United States",
            "New York",
            "NEW YORK",
            "Boston",
            "BOSTON",
            "San Francisco",
            "SAN FRANCISCO",
            "Washington",
            "WASHINGTON",
            "Philadelphia",
            "PHILADELPHIA",
            "Stamford",
            "STAMFORD",
            "Houston",
            "HOUSTON",
            "Los Angeles",
            "LOS ANGELES",
            "Chicago",
            "CHICAGO",
            "San Diego",
            "SAN DIEGO",
            "Denver",
            "DENVER",
            "Salt Lake City",
            "SALT LAKE CITY",
            "Miami",
            "MIAMI",
            "Tampa",
            "TAMPA",
            "Orlando",
            "ORLANDO",
            "California",
            "Radnor",
            "Dallas",
            "DALLAS",
            "Denver",
            "DENVER",
            "Kansas City",
            "KANSAS CITY",
            "Norman",
            "NORMAN",
            "Portland",
            "PORTLAND",
        ),
    }

    if location:
        location = location.strip()
    return location_data.get(location, location_data["UK"] + location_data["US"])


def filterUrls():
    wb = load_workbook(ctrXlDir)

    ws = wb.active

    urls = []

    if ws["D1"].value != "yes":
        return urls

    for row in ws.iter_rows(min_row=2, max_row=601):
        # for row in ws.iter_rows(min_row=1):

        if row[0].value == "ID" or row[0].value is None:
            continue

        if row[3].value == "yes":
            urls.append((row[0].value, row[1].value, row[2].value))

    return urls


def readUrl(key):
    wb = load_workbook(ctrXlDir)

    ws = wb.active

    if isinstance(key, int) and ws[f"A{key + 1}"].value == key:
        return [ws[f"B{key + 1}"].value, ws[f"C{key + 1}"].value]

    for row in ws.iter_rows(min_row=1):
        if str(row[0].value) == str(key):
            return [row[1].value, row[2].value]


def fetchJobs():
    wb = load_workbook(ctrXlDir)

    ws = wb.active

    return [cell.value.lower() for cell in ws["E"] if cell.value is not None]


def readHistory(key=None):
    ensure_history_file_exists()

    with open(histDir, "r") as file:
        try:
            data = json.load(file)

            if key is not None:
                return data.get(f"{key}", [])

            return data
        except:
            return []


def updateDB(key, arr):
    print(
        "########",
        f".{key}.",
        f"[{len(arr)}]",
        arr,
        "########",
        f".{key}.",
        f"[{len(arr)}]",
    )

    global rowData
    global cashData

    for item in arr:
        title, company, location, link = item

        result = collection.update_one(
            {"url": link},
            {
                "$set": {
                    "num": key,
                    "url": link,
                    "company": company,
                    "jobTitle": title,
                    "location": location,
                    "createdAt": datetime.now(),
                }
            },
            upsert=True,
        )


def eventHander(key, tp):
    print("@@@@@@@@", key, tp)


# client.close()
