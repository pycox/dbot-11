import json
from openpyxl import load_workbook, Workbook
import os

histDir = r"history.json"

ctrXlDir = r"clients.xlsx"

dbXlDir = r"data.xlsx"

cashData = {}

data = []


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


def getLocations(location):
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
            locations = getLocations(ws["G2"].value)
            urls.append((row[0].value, row[1].value, row[2].value, locations))

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
    global data
    global cashData

    hist = readHistory(key)
    newHist = []

    for item in arr:
        title, _, _, link = item

        newHist.append(link)

        if not link in hist:

            for job in fetchJobs():
                if job in title.lower():
                    data.append(item)
                    break

    cashData[f"{key}"] = newHist


def saveData():
    global data
    global cashData

    if os.path.exists(dbXlDir):
        wb = load_workbook(dbXlDir)
    else:
        wb = Workbook()

    if wb.active:
        ws = wb.active
    else:
        ws = wb.create_sheet()

    if ws["A1"] != "Job Title":
        ws.append(["Job Title", "Company", "Location", "Url"])

    for item in data:
        ws.append(item)

    wb.save(dbXlDir)

    ensure_history_file_exists()

    if not isinstance(cashData, dict):
        return

    with open(histDir, "w") as file:
        try:
            json.dump(cashData, file, indent=4)
        except Exception as e:
            print(e)