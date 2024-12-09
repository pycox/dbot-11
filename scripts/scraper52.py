import requests
from bs4 import BeautifulSoup
from utils import updateDB, eventHander


def main(key, com, url):

    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")

    items = soup.select("div.posting")

    data = []

    for item in items:
        location = item.find_all("span")[-1].text.strip()
        link = item.find("a").get("href").strip()
        title = item.find("h5").text.strip()

        data.append([title, com, location, link])

    updateDB(key, data)


if __name__ == "__main__":
    main()
