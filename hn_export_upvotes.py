import os
import sys
import argparse
import requests
from bs4 import BeautifulSoup
import json
import time
import getpass

class HackerNewsScraper:
    def __init__(self, username, password, debug=False):
        self.session = requests.Session()
        self.username = username
        self.password = password
        self.base_url = "https://news.ycombinator.com"
        self.debug = debug

    def _debug_print(self, *args):
        if self.debug:
            print("[DEBUG] ", *args)

    def login(self):
        login_url = f"{self.base_url}/login"
        data = {
            "acct": self.username,
            "pw": self.password
        }

        login_resp = self.session.post(login_url, data=data)
        if "Bad login" in login_resp.text or "login" in login_resp.url:
            raise Exception("Login failed. Check your username and password.")
        return True

    def scrape_upvoted(self):
        upvotes = []
        next_link = f"{self.base_url}/upvoted?id={self.username}"
        while next_link:
            self._debug_print(f"Scraping page {next_link}")
            resp = self.session.get(next_link)
            soup = BeautifulSoup(resp.text, "html.parser")
            rows = soup.select("tr.athing.submission")

            for row in rows:
                item_id = row.get("id")
                self._debug_print(f" > item_id = {item_id}")
                titleline = row.select_one("span.titleline")
                if not titleline:
                    print(f"❌ Error: no span.titleline found for item_id {item_id}")
                    continue

                # Extract the first <a> inside titleline
                link_tag = titleline.find("a")
                if not link_tag:
                    print(f"❌ Error: no a found for item_id {item_id}")
                    continue

                title = link_tag.text.strip()
                self._debug_print(f"    - title = {title}")

                # May be missing (flagged/dead)
                url = link_tag.get("href", "").strip()
                self._debug_print(f"    - url = {url}")

                # Get the next <tr> sibling and look for timestamp
                timestamp = ""
                next_row = row.find_next_sibling("tr")
                if next_row:
                    age_span = next_row.select_one("span.age")
                    if age_span and age_span.has_attr("title"):
                        timestamp_parts = age_span["title"].split()
                        if len(timestamp_parts) > 1:
                            # The UNIX timestamp
                            timestamp = timestamp_parts[1]
                self._debug_print(f"    - timestamp = {timestamp}")

                upvotes.append({
                    "id": item_id,
                    "timestamp": timestamp,
                    "title": title,
                    "url": url
                })


            more_link = soup.find("a", string="More")
            if more_link:
                next_link = self.base_url + "/" + more_link["href"]
                time.sleep(1)
            else:
                next_link = None
        return upvotes

    def export_json(self, data, filename="upvoted_posts.json"):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

def get_credentials(args):
    username = args.username or os.getenv("HN_USERNAME")
    password = args.password or os.getenv("HN_PASSWORD")

    if not username:
        username = input("Enter your HN username: ")
    if not password:
        password = getpass.getpass("Enter your HN password: ")

    return username, password

def main():
    parser = argparse.ArgumentParser(
        description="Export your Hacker News (https://news.ycombinator.com/) upvoted posts to JSON.",
        epilog="You can also set HN_USERNAME and HN_PASSWORD environment variables to avoid using --username / --password.",
        allow_abbrev=False)
    parser.add_argument("-u", "--username", help="Hacker News username")
    parser.add_argument("-p", "--password", help="Hacker News password")
    parser.add_argument("-o", "--output", default="upvoted_posts.json", help="output filename (default: upvoted_posts.json)")
    parser.add_argument("--overwrite", action="store_true", help="overwrite output file if it already exists")
    parser.add_argument("--debug", action="store_true", help="enable debug logging")
    args = parser.parse_args()

    # Check if output file already exist and if we're ok to overwrite it
    if os.path.exists(args.output) and not args.overwrite:
        print(f"Error: File '{args.output}' already exists. Use --overwrite to replace it.")
        # EEXIST 17 File exists
        sys.exit(17)

    username, password = get_credentials(args)

    scraper = HackerNewsScraper(username, password, debug=args.debug)
    try:
        scraper.login()
        print(f"✅ Logged in as {username}. Scraping upvoted posts...")
        upvoted = scraper.scrape_upvoted()
        scraper.export_json(upvoted, filename=args.output)
        print(f"✅ Exported {len(upvoted)} upvoted posts to '{args.output}'")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
