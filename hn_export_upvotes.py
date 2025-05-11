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
            resp = self.session.get(next_link)
            soup = BeautifulSoup(resp.text, "html.parser")
            rows = soup.select("tr.athing")

            for row in rows:
                title_elem = row.select_one("a.storylink")
                if not title_elem:
                    continue
                title = title_elem.text
                link = title_elem['href']
                item_id = row['id']
                upvotes.append({
                    "id": item_id,
                    "title": title,
                    "url": link
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
