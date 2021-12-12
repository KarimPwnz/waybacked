import time
from random import randint
import requests
import argparse
from functools import wraps
import json


def except_retry(retries, exceptions=(Exception,)):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(retries+1):
                try:
                    return func(*args, **kwargs)
                except exceptions:
                    time.sleep(randint(5, 10))

        return wrapper

    return decorator


class WaybackAPI:
    @staticmethod
    def get_pages_count(search):
        return int(requests.get(
            f"http://web.archive.org/cdx/search/cdx?url={search}&showNumPages=true"
        ).text)

    @staticmethod
    @except_retry(10, (requests.RequestException, json.decoder.JSONDecodeError))
    def get_page_json(search, page):
        return requests.get(
            f"http://web.archive.org/cdx/search/cdx?url={search}&output=json&fl=original&collapse=urlkey&page={page}"
        ).json()[1:]


class WaybackSearch:
    def __init__(self, search):
        self.search = search
        self.api = WaybackAPI()

    def run(self):
        try:
            pages_count = self.api.get_pages_count(self.search)
        except:
            return Exception("Couldn't get number of archive pages")
        for page in range(pages_count):
            yield self.page_json_to_urls(self.api.get_page_json(self.search, page))

    @staticmethod
    def page_json_to_urls(page_json):
        for row in page_json:
            yield row[0]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("search", metavar="search",
                        nargs=None, help="Search query")
    args = parser.parse_args()
    search = WaybackSearch(args.search)
    try:
        for page in search.run():
            for url in page:
                print(url)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
