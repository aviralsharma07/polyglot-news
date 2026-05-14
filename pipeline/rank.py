from datetime import datetime, timezone

def score(df):
    now = datetime.now(timezone.utc)
    
    # Recency score: articles published in last 2 hours get 1.0, 
    # older articles decay toward 0
    df["hours_ago"] = (now - df["published_at"]).dt.total_seconds() / 3600
    df["recency_score"] = 1 / (1 + df["hours_ago"])   # decay function
    
    # Source diversity bonus: reward sources you've seen less
    source_counts = df["source"].value_counts()
    df["source_freq"] = df["source"].map(source_counts)
    df["diversity_score"] = 1 / df["source_freq"]
    
    # Title quality: penalize clickbait patterns
    clickbait_words = ["shocking", "you won't believe", "viral", "exposed"]
    df["clickbait_penalty"] = df["title"].str.lower().apply(
        lambda t: 0.5 if any(w in t for w in clickbait_words) else 1.0
    )
    
    # Final score
    df["score"] = (
        df["recency_score"] * 0.6 +
        df["diversity_score"] * 0.3
    ) * df["clickbait_penalty"]
    
    return df.sort_values("score", ascending=False).reset_index(drop=True)