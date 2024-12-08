import requests
from bs4 import BeautifulSoup
from utils import updateDB


def main(key, com, url):

    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")

    items = soup.select("a.Card__StyledCard-sc-y213rf-1")

    data = []

    for item in items:
        link = item.get("href").strip()
        title = item.select_one("h3").text.strip() if item.select_one("h3") else ""
        location = "London"

        data.append([title, com, location, f"https://www.kfh.co.uk{link}"])

    updateDB(key, data)


if __name__ == "__main__":
    main()
