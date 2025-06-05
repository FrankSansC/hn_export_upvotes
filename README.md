# hn_export_upvotes.py

The purpose of this script is to export **your** upvoted posts list from [Hacker News](https://news.ycombinator.com/) into a JSON file.

But why you may ask ? First and foremost because I haven't found any working tool that were able to do this. And second because I consider this to be **my** data, and I want to be able to backup it.

## AI usage

Please note that most of this script has been written using [OpenAI](https://openai.com/) [ChatGPT](https://chatgpt.com/) (GPT-4o) as a teammate.

This project is an excuse to see how good AI is at helping to write small tools (I always have lots of ideas but don't have time to implement them).

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

- [ ] Use [`uv`](https://github.com/astral-sh/uv) to install dependencies ([`requests`](https://github.com/psf/requests) and [`beautifulsoup`](https://code.launchpad.net/beautifulsoup))
- [ ] Procedure to use a [systemd timer](https://www.freedesktop.org/software/systemd/man/latest/systemd.timer.html) (and not `cron`) to call it periodically
- [ ] Script to version the output JSON file into a git repository
- [ ] Use [`ntfy`](https://github.com/binwiederhier/ntfy) to have notifications when we grab new entries

# License

[MIT License](./LICENSE)
