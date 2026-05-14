def render(df, top_n=15):
    print("\n" + "="*60)
    print(f"  POLYGLOT NEWS DIGEST — Top {top_n} Articles")
    print("="*60 + "\n")
    
    for i, row in df.head(top_n).iterrows():
        rank = i + 1
        age_h = round(row["hours_ago"], 1)
        print(f"[{rank:02d}] {row['title']}")
        print(f"     {row['source']}  ·  {age_h}h ago  ·  score: {row['score']:.3f}")
        print(f"     {row['url']}")
        if row["description"]:
            print(f"     {row['description'][:100]}...")
        print()