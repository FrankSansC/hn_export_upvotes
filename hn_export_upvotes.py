import os
import argparse
import requests
from bs4 import BeautifulSoup
import json
import time
import getpass

class HackerNewsScraper:
    def __init__(self, username, password):
        self.session = requests.Session()
        self.username = username
        self.password = password
        self.base_url = "https://news.ycombinator.com"

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
            print(f"Scraping page {next_link}")
            resp = self.session.get(next_link)
            soup = BeautifulSoup(resp.text, "html.parser")
            rows = soup.select("tr.athing.submission")

            for row in rows:
                item_id = row.get("id")
                print(f"item_id = {item_id}", end=" ")
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
                print(f"title = {title}", end = " ")

                # May be missing (flagged/dead)
                url = link_tag.get("href", "").strip()
                print(f"url = {url}", end = " ")

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
                print(f"timestamp = {timestamp}")

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
    parser = argparse.ArgumentParser(description="Export Hacker News upvoted posts to JSON.")
    parser.add_argument("--username", help="Hacker News username")
    parser.add_argument("--password", help="Hacker News password")
    parser.add_argument("--output", default="upvoted_posts.json", help="Output filename (default: upvoted_posts.json)")
    args = parser.parse_args()

    username, password = get_credentials(args)

    scraper = HackerNewsScraper(username, password)
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
