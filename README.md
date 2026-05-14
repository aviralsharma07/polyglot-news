# Polyglot News

A Python CLI tool that pulls news from multiple free APIs, normalizes the data into a unified structure, and outputs a ranked digest to the terminal and a CSV file.

I built this project to learn AI and Python by building stuff. The ranking pipeline is intentionally simple today, with clear hooks for future AI-based scoring.

## Features

- Multi-source news fetching (NewsAPI, GNews, Currents API)
- Unified article schema across providers
- Ranking by recency and source diversity, with a clickbait penalty
- Clean terminal digest output
- CSV export for later analysis

## How it works

```
fetchers/    -> pull raw API JSON
pipeline/    -> normalize + score
output/      -> terminal digest + CSV
```

Data flow:

```
API calls -> normalize -> score -> display + csv
```

## Requirements

- Python 3.13+
- API keys for the supported providers

## Setup

1. Create and activate a virtual environment

```
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies

```
pip install -e .
```

3. Add API keys (create a .env file in the repo root)

```
NEWSAPI_KEY=your_newsapi_key
GNEWSAPI_KEY=your_gnews_key
CURRENTAPI_KEY=your_currents_key
```

## Usage

Basic run:

```
python main.py
```

Search a topic and control the output size:

```
python main.py --query "ai" --top 20
```

Select sources:

```
python main.py --sources newsapi gnews
```

Skip CSV export:

```
python main.py --no-csv
```

CLI options:

- `--query`, `-q`: search topic (default: "technology")
- `--top`, `-n`: number of articles to fetch and display (default: 15)
- `--no-csv`: disable CSV export
- `--sources`, `-s`: choose sources (`newsapi`, `gnews`, `currentapi`)

## Output

- Terminal digest with ranking, source, age, and score
- CSV saved to the `digests/` folder with a timestamped filename

Example digest snippet:

```
[01] Example headline here
		 Example Source  ·  1.2h ago  ·  score: 0.842
		 https://example.com/article
```

## Normalized schema

Each article is normalized into a shared shape:

```
{
	"title": "...",
	"url": "...",
	"source": "...",
	"published_at": datetime,
	"description": "...",
	"query": "...",
	"fetched_from": "NewsAPI | GNews | CurrentNews"
}
```

## Ranking logic (current)

- Recency: newer articles score higher
- Diversity: sources seen less get a small bonus
- Clickbait penalty for known patterns

This is intentionally simple to keep it readable and hackable.

## Project structure

```
.
├── main.py
├── fetchers/
│   ├── newsapi.py
│   ├── gnews.py
│   └── currentapi.py
├── pipeline/
│   ├── normalize.py
│   └── rank.py
├── output/
│   ├── display.py
│   └── csv_writer.py
├── data_examples/
└── digests/            # created at runtime
```

## Adding a new source

1. Create a new fetcher in `fetchers/`
2. Add a normalizer in `pipeline/normalize.py`
3. Wire it into `main.py` and CLI choices

## Troubleshooting

- Missing or invalid API keys will raise HTTP errors from the provider.
- Some free plans have delayed or limited results.
- If CSV is not created, ensure `digests/` is writable.
