# Seithi – auto-updating news site

How it works:
1. `fetch_news.py` reads RSS feeds (The Hindu, BBC, ESPNcricinfo, Google News searches) and, if you give it a Claude API key, writes a one-line summary for each story.
2. It saves everything to `news.json`.
3. `.github/workflows/update-news.yml` runs that script **every hour** on GitHub for free and commits the new `news.json`.
4. `index.html` reads `news.json` and shows it (re-checks every 10 minutes).

## Go live (free, about 10 minutes)
1. Create a GitHub account and a new **public** repository, e.g. `seithi`.
2. Upload all files here, including the `.github` folder.
3. Repo **Settings → Pages**: Source = "Deploy from a branch", Branch = `main`, folder `/ (root)`.
4. Repo **Settings → Secrets and variables → Actions → New repository secret**: name `ANTHROPIC_API_KEY`, value = your key from console.anthropic.com. (Optional. Without it the site shows the feed's own snippets.)
5. Open the **Actions** tab → "Update news hourly" → **Run workflow** once to create the first `news.json`.
6. Your site is at `https://<your-username>.github.io/seithi/`.

## Test on your computer
```
pip install feedparser anthropic
python fetch_news.py
python -m http.server
```
Open http://localhost:8000

## Customize
Edit the `FEEDS` list at the top of `fetch_news.py` to add sections (for example, "Villupuram district") or change search terms. Each Google News entry is just a search query.

## Notes
- GitHub's hourly schedule can run a few minutes late. That is normal.
- The site shows headlines, short summaries and links back to the publisher. Do not copy full articles, since publishers own them.
- AI summaries use only the feed text and can be imperfect, which is why each card links to the original source.
