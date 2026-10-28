"""Fetch news from RSS feeds, optionally summarize with Claude, write news.json.
Run hourly by GitHub Actions (see .github/workflows/update-news.yml)."""
import json, os, re, html, calendar
from datetime import datetime, timezone
from urllib.parse import quote
import feedparser

def gnews(q):  # Google News RSS search, India edition
    return f"https://news.google.com/rss/search?q={quote(q)}%20when:1d&hl=en-IN&gl=IN&ceid=IN:en"

# Edit this list to add or change sections and sources.
FEEDS = {
    "Tamil Nadu": [
        "https://www.thehindu.com/news/national/tamil-nadu/feeder/default.rss",
        gnews("Tamil Nadu politics"), gnews("Villupuram OR Gingee OR Senji"),
    ],
    "India": [
        "https://www.thehindu.com/news/national/feeder/default.rss",
        gnews("India state news"),
    ],
    "World": [
        "https://feeds.bbci.co.uk/news/world/rss.xml",
        gnews("Israel Iran"), gnews("Trump Iran decision"),
    ],
    "Technology": [gnews("Elon Musk flying car"), "https://feeds.bbci.co.uk/news/technology/rss.xml"],
    "Cricket": ["https://www.espncricinfo.com/rss/content/story/feeds/0.xml", gnews("cricket India")],
    "Football": ["https://feeds.bbci.co.uk/sport/football/rss.xml"],
    "Formula 1": ["https://feeds.bbci.co.uk/sport/formula1/rss.xml"],
    "MotoGP": [gnews("MotoGP")],
}
PER_SECTION = 15

def clean(t):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", t or ""))).strip()

def fetch_section(urls):
    seen, items = set(), []
    for url in urls:
        try:
            feed = feedparser.parse(url)
        except Exception as e:
            print("feed failed", url, e); continue
        for e in feed.entries[:20]:
            title = clean(e.get("title"))
            if not title or title.lower() in seen: continue
            seen.add(title.lower())
            ts = e.get("published_parsed") or e.get("updated_parsed")
            items.append({
                "title": title,
                "link": e.get("link"),
                "source": clean(e.get("source", {}).get("title") if e.get("source") else feed.feed.get("title", "")),
                "summary": clean(e.get("summary"))[:240],
                "time": datetime.fromtimestamp(calendar.timegm(ts), timezone.utc).isoformat() if ts else None,
            })
    items.sort(key=lambda x: x["time"] or "", reverse=True)
    return items[:PER_SECTION]

def ai_summarize(section, items):
    """One-sentence neutral summaries via Claude. Skipped if no API key."""
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key or not items: return
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=key)
        lines = "\n".join(f"{i}. {it['title']} - {it['summary']}" for i, it in enumerate(items))
        msg = client.messages.create(
            model=os.environ.get("CLAUDE_MODEL", "claude-haiku-5-5"), max_tokens=2000,
            messages=[{"role": "user", "content":
                f"Section: {section}. For each numbered headline, write one plain, neutral sentence "
                "(max 25 words) based only on the given text. Do not invent facts. "
                'Reply ONLY with JSON: {"0": "...", "1": "..."}\n\n' + lines}])
        out = json.loads(re.search(r"\{.*\}", msg.content[0].text, re.S).group(0))
        for i, it in enumerate(items):
            if str(i) in out: it["summary"] = out[str(i)]
    except Exception as e:
        print("AI summary skipped for", section, e)

def main():
    data = {"updated": datetime.now(timezone.utc).isoformat(), "sections": {}}
    for name, urls in FEEDS.items():
        items = fetch_section(urls)
        ai_summarize(name, items)
        data["sections"][name] = items
        print(name, len(items))
    with open("news.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)

if __name__ == "__main__":
    main()
