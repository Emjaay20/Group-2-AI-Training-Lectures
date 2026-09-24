# Lab: Data collection (Playwright)

Files: `1_dataCollection.py`, `dataCollectionSimplified.py`, `Day1/` copies, output `headlines.json` / `crime_headlines.json`.

## Purpose
Turn an open news listing into structured records the rest of the course can analyse.

## What the class did
- Launch Chromium with Playwright (async, usually headless).
- Open `https://www.vanguardngr.com/search/crime`.
- Wait for headline selectors (`h2 a`, `h3 a`).
- Save title + link.
- Fuller script also:
  - filters crime-ish keywords (kill, murder, kidnap, …),
  - guesses a Nigerian location if a state/city name appears,
  - pulls a date from visible text or the URL path (`/2026/09/...`),
  - writes JSON with source URL, category, UTC timestamp, count, and ranked items.

The simplified script is the teaching core: goto → wait → query links → dump JSON.

## Why Playwright, not just `requests`
News pages are often JS-rendered. A real browser sees the same DOM the user sees. Headless + blocked images/CSS keeps it lighter.

## Teaching points
- Unstructured web text is the raw material for later NLP.
- Always store source + time. Intelligence work is provenance, not just titles.
- Scraping public news for a classroom lab is not the same as accessing closed or illegal forums.

## Typical questions to expect
- How do I change the source site?
- Why did wait_for_selector fail?
- How does this JSON feed Lab 3 sentiment?
