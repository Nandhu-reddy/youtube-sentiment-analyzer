import pandas as pd
from textblob import TextBlob
import matplotlib.pyplot as plt
from googleapiclient.discovery import build

# Replace with your API key and video ID
api_key = "AIzaSyCHHl6hVsWq2FdgyLPYlMHbpzU9TX2HyNs"
video_id = "6IeVKpXu7cE"

# Build YouTube API client
youtube = build('youtube', 'v3', developerKey=api_key)

comments = []
nextPageToken = None

# Fetch multiple pages of comments
while True:
    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=100,
        pageToken=nextPageToken
    )
    response = request.execute()

    for item in response['items']:
        comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
        comments.append(comment)

    nextPageToken = response.get('nextPageToken')
    if not nextPageToken:
        break
print(f"Total Comments Fetched: {len(comments)}")

# Sentiment Analysis Function
def get_sentiment(text):
    analysis = TextBlob(text)
    if analysis.sentiment.polarity > 0:
        return 'Positive'
    elif analysis.sentiment.polarity == 0:
        return 'Neutral'
    else:
        return 'Negative'

results = [get_sentiment(c) for c in comments]

# Create DataFrame
df = pd.DataFrame({'Comment': comments, 'Sentiment': results})
print(df.head())

# Visualization
counts = df['Sentiment'].value_counts()
counts.plot(kind='pie', autopct='%1.1f%%')
plt.title("Sentiment Analysis of YouTube Comments")
plt.show()
