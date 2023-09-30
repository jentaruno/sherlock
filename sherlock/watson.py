import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0",
}


def make_soup(url):
    try:
        page = requests.get(url, headers=headers, timeout=5).content
    except requests.exceptions.Timeout:
        print("Request timeout")
    return BeautifulSoup(page, "html.parser")


def check_instagram(username):
    url = "https://www.instagram.com/" + username
    soup = make_soup(url)
    tag = soup.find(string="Sorry, this page isn't available.")
    # print(soup)
    # print(tag)
    if tag is None:
        print("found")
        return {
            "site": "Instagram",
            "urlMain": "https://www.instagram.com/",
            "urlUser": url,
            "status": "Claimed",
            "httpStatus": 200,
            "responseTime": 0.8199266480005463
        },
    else:
        print("unavailable")
        return
