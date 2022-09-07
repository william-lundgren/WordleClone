import requests
from bs4 import BeautifulSoup as bs
import urllib.request


def get_words(url):
    response = requests.get(url)
    html = response.content
    soup = bs(html, "lxml")

    filters = "-.,'¨+!\"[]/{}&%€¤$#£@+\\*"
    words = []

    word_list = soup.select("li.list-group-item")

    for item in word_list:
        word = item.find("a").text
        if not any(symbol in word for symbol in filters):
            words.append(word)

    return words


def main():
    words = []

    url = "https://doon.se/ordl%C3%A4ngd/5?page="
    for i in range(1, 73):
        temp = get_words(url + str(i))
        words += temp

    with open("words.txt", "w") as file:
        for word in words:
            file.write(word + "\n")


if __name__ == "__main__":
    main()
