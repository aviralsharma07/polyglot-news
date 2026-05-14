from fetchers import newsapi , gnews, currentapi
from pipeline import normalize , rank
from output import display, csv_writer
import pandas as pd
import argparse

def main():
    parser = argparse.ArgumentParser(description="Polyglot News Aggregator")
    parser.add_argument("--query", "-q", default="technology", help="Search topic")
    parser.add_argument("--top", "-n", type=int, default=15, help="Number of articles")
    parser.add_argument("--no-csv", action="store_true", help="Skip CSV export")
    parser.add_argument("--sources", "-s", nargs="+", choices=["newsapi", "gnews", "currentapi"], default=["newsapi", "gnews", "currentapi"], help="Data sources to fetch from")
    args = parser.parse_args()

    # FETCH
    all_articles = []
    if "newsapi" in args.sources:
        newsapi_data = newsapi.fetch(query=args.query, page_size=args.top)
        all_articles += normalize.from_newsapi(newsapi_data, args.query)
    if "gnews" in args.sources:
        gnews_data = gnews.fetch(query=args.query, max_results=args.top)
        all_articles += normalize.from_gnews(gnews_data, args.query)
    if "currentapi" in args.sources:
        current_news_data = currentapi.fetch(query=args.query, page_size=args.top)
        all_articles += normalize.from_currentapi(current_news_data, args.query)

    # PIPELINE
    df = pd.DataFrame(all_articles).drop_duplicates(subset=["url"])
    df = rank.score(df)

    # OUTPUT
    display.render(df, top_n=args.top)
    if not args.no_csv:
        csv_writer.write(df, args.query)


if __name__ == "__main__":
    main()