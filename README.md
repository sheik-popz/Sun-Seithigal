# Trend-Scope – Auto-Updating News Website

A mobile-friendly news website that brings the day's headlines from **Tamil Nadu, India and the world** in one place, along with cricket, football, Formula 1 and MotoGP. The news refreshes by itself on a schedule, so nobody has to update it by hand.

**Live site:** https://sheik-popz.github.io/TrendScope/

## About the project

TrendScope gives readers a simple, fast and clean front page for local, national and world news without ads or sign-ups. There is no server and no database. A scheduled GitHub job collects headlines from public news feeds, saves them to a data file, and the website reads that file in the browser.

## Features

- Front page with a lead story, top stories and a "Latest" column
- Sections for Tamil Nadu, India, World, Technology, Cricket, Football, Formula 1 and MotoGP
- Search across all headlines
- News updates automatically on a schedule, even when no computer is switched on
- Optional one-line story summaries written by Claude (Anthropic API)
- Every story links to the original publisher
- Tamil font support
- Dark mode that follows the device setting
- Works on phones, tablets and desktops

## Tech stack

- HTML, CSS and vanilla JavaScript in a single file (`index.html`)
- Python script (`fetch_news.py`) with the `feedparser` library to collect RSS news
- GitHub Actions for the automatic schedule
- GitHub Pages for hosting
- Anthropic Claude API for optional summaries
- Google Fonts (Source Serif 4, Inter, Noto Sans Tamil, Noto Serif Tamil)

## Project structure

```
.
├── index.html                          # the whole website
├── fetch_news.py                       # collects news and writes news.json
├── news.json                           # latest news, updated automatically
├── .github/
│   └── workflows/
│       └── update-news.yml             # the automatic update schedule
└── README.md                           # this file
```

## How the automatic update works

1. GitHub Actions runs `fetch_news.py` on a schedule.
2. The script reads the news feeds and, if an API key is set, asks Claude for a short summary of each story.
3. The result is saved to `news.json` in the repository.
4. The website loads `news.json` and shows the latest stories.

## Run locally

1. Download or clone this repository.
2. Install the requirements and fetch the news once:
   ```
   pip install feedparser anthropic
   python fetch_news.py
   ```
3. Start a small local server and open http://localhost:8000:
   ```
   python -m http.server
   ```

The site needs a local server because browsers block reading `news.json` when `index.html` is opened by double-clicking it.

## Customize

- **Sections and sources:** edit the `FEEDS` list at the top of `fetch_news.py`.
- **Update timing:** edit the `cron` line in `.github/workflows/update-news.yml`.
- **AI summaries (optional):** add a repository secret named `ANTHROPIC_API_KEY` under Settings > Secrets and variables > Actions.
- **Colours and fonts:** edit the CSS at the top of `index.html`.

## Note

TrendScope shows headlines, short summaries and links only. Full articles belong to their publishers. AI summaries use only the feed text and can be imperfect, so check the original article for details.
