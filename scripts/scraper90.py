import requests
from bs4 import BeautifulSoup
from utils import updateDB


def main(key, com, url):
    response = requests.get(url)
    html_content = response.text

    soup = BeautifulSoup(html_content, "html.parser")

    data = []

    items = soup.select("li.job-result-item")

    for item in items:
        link = item.select_one("a")["href"].strip()
        location = item.select_one("li.results-job-location").text.strip()

        data.append(
            [
                item.select_one("div.job-title").text.strip(),
                com,
                location,
                link,
            ]
        )

    updateDB(key, data)


if __name__ == "__main__":
    main()
