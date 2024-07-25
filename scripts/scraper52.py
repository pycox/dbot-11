import requests
from bs4 import BeautifulSoup
from utils import readUrl, updateDB


def main(key, com, url, locations):

    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")

    items = soup.select("div.posting")

    data = []

    for item in items:
        location = item.find_all("span")[-1].text.strip()
        for str in locations:
            if str in location:
                link = item.find("a").get("href").strip()
                title = item.find("h5").text.strip()
                data.append([title, com, location, link])
                break

    updateDB(key, data)


if __name__ == "__main__":
    main()
