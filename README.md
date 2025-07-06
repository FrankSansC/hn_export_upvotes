# hn_export_upvotes.py

The purpose of this script is to export **your** upvoted posts list from [Hacker News](https://news.ycombinator.com/) into a JSON file.

But why you may ask ? First and foremost because I haven't found any working tool that were able to do this. And second because I consider this to be **my** data, and I want to be able to backup it.

## AI usage

Please note that most of this script has been written using [OpenAI](https://openai.com/) [ChatGPT](https://chatgpt.com/) (GPT-4o) as a teammate.

This project is an excuse to see how good AI is at helping to write small tools (I always have lots of ideas but don't have time to implement them).

# Dependencies

`hn_export_upvotes` relies on two dependencies :
- [`requests`](https://requests.readthedocs.io/en/latest/)
- [`beautifulsoup`](https://www.crummy.com/software/BeautifulSoup/)

You can either install them with your favorite package manager or install [`uv`](https://docs.astral.sh/uv/) and launch `hn_export_upvotes.py` right away.

It makes use of [PEP-723](https://peps.python.org/pep-0723/) that allows to add metadata :

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "requests",
#     "beautifulsoup4"
# ]
# ///
```

When launched the first time you'll see `uv` downloading and installing the dependencies :

```
Resolved 8 packages in 651ms
[...]
Prepared 8 packages in 583ms
Installed 8 packages in 17ms
 + beautifulsoup4==4.13.4
 + certifi==2025.6.15
 + charset-normalizer==3.4.2
 + idna==3.10
 + requests==2.32.4
 + soupsieve==2.7
 + typing-extensions==4.14.1
 + urllib3==2.5.0
```

I got the inspiration to use `uv` thanks to this blog post : [Fun with uv and PEP 723](https://www.cottongeeks.com/articles/2025-06-24-fun-with-uv-and-pep-723) (related [hn post](https://news.ycombinator.com/item?id=44369388)).

# Usage

```shell
usage: hn_export_upvotes.py [-h] [-u USERNAME] [-p PASSWORD] [-o OUTPUT] [--overwrite] [--debug]

Export your Hacker News (https://news.ycombinator.com/) upvoted posts to JSON.

options:
  -h, --help            show this help message and exit
  -u, --username USERNAME
                        Hacker News username
  -p, --password PASSWORD
                        Hacker News password
  -o, --output OUTPUT   output filename (default: upvoted_posts.json)
  --overwrite           overwrite output file if it already exists
  --debug               enable debug logging

You can also set HN_USERNAME and HN_PASSWORD environment variables to avoid using --username / --password.
```

# TODO

- [ ] Alternative export format : RSS feed (XML file) (see issue #1)
- [ ] Procedure to use a [systemd timer](https://www.freedesktop.org/software/systemd/man/latest/systemd.timer.html) (and not `cron`) to call it periodically
- [ ] Script to version the output JSON file into a git repository
- [ ] Use [`ntfy`](https://github.com/binwiederhier/ntfy) to have notifications when we grab new entries

# Similar projects

Here's a non-exhaustive list, in non-specific order, of similar projects to `hn_export_upvotes` :

- [Show HN: Export HN Favorites to a CSV File](https://news.ycombinator.com/item?id=22788236)
  - [getHNFavorites.js](https://gabrielsroka.github.io/getHNFavorites.js)
- [hacker-new-favorites-api](https://github.com/reactual/hacker-news-favorites-api)
- [hn-utils](https://github.com/jaytaylor/hn-utils)
- [Show HN: Export HN saved links (upvotes) as JSON or CSV](https://news.ycombinator.com/item?id=11754099)
  - [HN-Saved-Links-Export](https://github.com/amjd/HN-Saved-Links-Export)
- [hn-saved-export](https://github.com/thomaskcr/hn-saved-export)
- [hackernews-to-raindrop](https://github.com/davenicoll/hackernews-to-raindrop)
- [archivy-hn](https://github.com/archivy/archivy-hn)
- [hackernewsGetUserUpvotesDevConsole.js](https://gist.github.com/VehpuS/d70dc3669d96da953c7a4f9f6665e83d)

# License

[MIT License](./LICENSE)
