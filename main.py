from fetchers import newsapi
from fetchers import gnews

# data = newsapi.fetch(query="technology")
data = gnews.fetch(query="technology")
print(data)