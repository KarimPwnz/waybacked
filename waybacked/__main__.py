import argparse
import sys
import time
from functools import wraps
from random import randint

import requests


def except_retry(retries, exceptions=(Exception,)):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions:
                    time.sleep(randint(5, 10))

        return wrapper

    return decorator


class WaybackAPI:
    @staticmethod
    def get_pages_count(search):
        return int(
            requests.get(
                f"https://web.archive.org/cdx/search/cdx?url={search}&showNumPages=true"
            ).text
        )

    @staticmethod
    @except_retry(10, (requests.RequestException))
    def get_page_text(search, page):
        return requests.get(
            f"https://web.archive.org/cdx/search/cdx?url={search}&fl=original&collapse=urlkey&page={page}"
        ).text


class WaybackSearchError(Exception):
    pass


class WaybackSearch:
    def __init__(self, search):
        self.search = search
        self.api = WaybackAPI()

    def run(self):
        try:
            pages_count = self.api.get_pages_count(self.search)
        except:
            raise WaybackSearchError("Couldn't get number of archive pages")
        for page in range(pages_count):
            # Split lines and remove last empty line
            data = self.api.get_page_text(self.search, page).split("\n")[:-1]
            if data:
                yield data


def process_search(search):
    search = WaybackSearch(search)
    try:
        for page in search.run():
            for url in page:
                print(url, flush=True)
    except WaybackSearchError as e:
        print(e)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "search", metavar="search", nargs="?", help="Search query", default=None
    )
    args = parser.parse_args()
    search_strs = (args.search,) if args.search else (l.rstrip("\n") for l in sys.stdin)
    try:
        for search in search_strs:
            process_search(search)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
