import time
from random import randint
import requests
import argparse
from functools import wraps


def except_retry(retries):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(retries+1):
                try:
                    return func(*args, **kwargs)
                except:
                    time.sleep(randint(5, 10))

        return wrapper

    return decorator


class ArchiveSearcher:
    def __init__(self, search):
        self.search = search

    def run_search(self):
        num_pages = self.get_num_pages()
        for page in range(num_pages):
            self.print_page(page)

    @except_retry(10)
    def print_page(self, page):
        response_json = requests.get(
            f"http://web.archive.org/cdx/search/cdx?url={self.search}&output=json&fl=original&collapse=urlkey&page={page}"
        ).json()[1:]
        for row in response_json:
            print(row[0])

    def get_num_pages(self):
        response = requests.get(
            f"http://web.archive.org/cdx/search/cdx?url={self.search}&showNumPages=true"
        ).text
        if not response:
            return None
        return int(response)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("search", metavar="search",
                        nargs=None, help="Search query")
    args = parser.parse_args()
    searcher = ArchiveSearcher(args.search)
    searcher.run_search()


if __name__ == "__main__":
    main()
