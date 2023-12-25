from typing import Set, Tuple

import requests
from bs4 import BeautifulSoup
from urllib.parse import ParseResult, urlparse, urljoin

urls = set()


def scrape_links(website):
    webpage = requests.get(website)
    html_content = webpage.content
    soup = BeautifulSoup(html_content, "lxml")

    for tag in soup.find_all("a", href=True):
        href = tag.get("href")

        if href.startswith("/"):
            href = urljoin("https://stnd.projectrazer.org", href)

        url = urlparse(href)

        if href.startswith("#") or not url.netloc.startswith("stnd"):
            continue

        if href not in urls:
            urls.add(href)

            with open("urls.txt", "r") as file:
                text = file.readlines()
                for idx, line in enumerate(text):
                    text[idx] = line.strip("\n")

            with open("urls.txt", "a") as file:
                if href not in text:
                    file.writelines(href + "\n")
                else:
                    continue

            scrape_links(href)


class Crawler():
    def __init__(self, base_url: str, output_file: str, external_links: bool = False):
        if base_url.endswith("/"):
            base_url = base_url[:-1]

        self.base_url: str = base_url
        self.external_links: bool = external_links
        self.webpage: requests.Response = requests.get(self.base_url)
        self.html_content: bytes = self.webpage.content
        self.soup: BeautifulSoup = BeautifulSoup(self.html_content, "lxml")
        self.exclude: Set = set()
        self.output_file = output_file
   
    def crawl(self):
        for tag in self.soup.find_all("a", href=True):
            href: str = tag.get("href")

            if href.startswith("/"):
                href: str = urljoin(self.base_url, href)

            url: ParseResult = urlparse(href)

            if (
                href.startswith("#")
                or href in self.exclude
                or url.path in self.exclude
            ):
                continue
    
    def filter(self, path: bool = False, subdomain: bool = False, *args: Tuple[str]):
        for arg in args:
            self.exclude.add(arg)



scrape_links("https://stnd.projectrazer.org/")
