import os
from datetime import datetime

def write(df, query):
    os.makedirs("digests", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"digests/{query.replace(' ', '_')}_{timestamp}.csv"
    
    cols = ["rank_position", "title", "source", "published_at", 
            "score", "url", "description", "query"]
    df.index.name = "rank_position"
    df.reset_index()[cols].to_csv(filename, index=False)
    print(f"\n[✓] Saved to {filename}")
    return filename