import argparse
import os
import sys
import time
from dataclasses import dataclass
from typing import Dict, ClassVar

from notion_client import Client
from notion_client.helpers import iterate_paginated_api


@dataclass
class NotionPage:
    page_id: str
    last_edited_time: str
    url: str
    title: str

    pages_by_key: ClassVar[Dict[str, 'NotionPage']] = {}

    def __str__(self):
        return f"title:{self.title} | last_edited:{self.last_edited_time} | url:{self.url}"

    def record_page_by_key(self) -> bool:
        page_key = self.title + ' ' + self.last_edited_time
        if page_key in NotionPage.pages_by_key:
            return False
        else:
            NotionPage.pages_by_key[page_key] = self

        return True

    @staticmethod
    def instantiate_page_from_page_info(page_info):
        page_id = page_info['id']
        last_edited_time = page_info['last_edited_time']
        url = page_info['url']
        titles = page_info['properties']['Name']['title']
        if len(titles) > 1:
            print(f'ERROR: {url} has more than one title')
        title = page_info['properties']['Name']['title'][0]['plain_text']

        return NotionPage(page_id, last_edited_time, url, title)


def get_notion_token_from_env_var():
    NOTION_TOKEN_ENV_VAR = 'NOTION_TOKEN'
    if NOTION_TOKEN_ENV_VAR in os.environ:
        return os.environ[NOTION_TOKEN_ENV_VAR]
    else:
        print(f"""You must specify your Notion token using the environment variable {NOTION_TOKEN_ENV_VAR}
Example: export {NOTION_TOKEN_ENV_VAR}=secret_abc1234""", file=sys.stderr)
        sys.exit(1)


def parse_args():
    ap = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                 description="Detect duplicated pages in a Notion database and optionally delete them")
    ap.add_argument('-m', '--max_page_count', type=int, nargs='?',
                    help="Maximum number of pages to scan for duplicated pages")
    ap.add_argument('-D', '--delete', action='store_true', help="Do the actual deletion (set in_trash=True)")
    ap.add_argument('-M', '--max_delete_page_count', type=int, nargs='?',
                    help="Maximum number of pages to delete")

    ap.add_argument('database_id',
                    help="Notion database on which to conduct the duplicate search. See README.md for more details")

    return ap.parse_args()


def main():
    notion = Client(auth=get_notion_token_from_env_var())

    cli_args = parse_args()
    database_id = cli_args.database_id

    delete_page_count = dupe_count = page_count = 0
    max_page_count = cli_args.max_page_count if cli_args.max_page_count else sys.maxsize
    max_delete_page_count = cli_args.max_delete_page_count if cli_args.max_delete_page_count else sys.maxsize
    start = time.time()
    for page_info in iterate_paginated_api(notion.databases.query, database_id=database_id):
        page = NotionPage.instantiate_page_from_page_info(page_info)
        recorded = page.record_page_by_key()
        if not recorded:
            dupe_count += 1
            if cli_args.delete:
                print(f"DELETING dupe page -> {page}")
                notion.pages.update(page_id=page.page_id, in_trash=True)
                delete_page_count += 1
                if delete_page_count >= max_delete_page_count:
                    print("Reached max delete page count")
                    break
            else:
                print(f"This page is a dupe -> {page}")

        page_count += 1
        if page_count >= max_page_count:
            print("Reached max page count")
            break
        elif page_count % 100 == 0:
            seconds_from_start = time.time() - start
            print(
                f"Scanned {page_count:5d} in {seconds_from_start:5.2f} secs or {page_count / seconds_from_start:3.0f} pages/sec")

    print(
        f"Iterated over {page_count} pages in the database:{database_id}. Found {dupe_count} duplicated page(s) and deleted {delete_page_count} page(s)")
    print(f"Elapased time:{time.time() - start:.2f} seconds")


if __name__ == "__main__":
    main()
