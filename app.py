import streamlit as st
import pandas as pd
from textblob import TextBlob
import matplotlib.pyplot as plt
from googleapiclient.discovery import build

# YouTube API credentials
api_key = "AIzaSyCHHl6hVsWq2FdgyLPYlMHbpzU9TX2HyNs"

# Sentiment Analysis function
def get_sentiment(text):
    analysis = TextBlob(text)
    if analysis.sentiment.polarity > 0:
        return 'Positive'
    elif analysis.sentiment.polarity < 0:
        return 'Negative'
    else:
        return 'Neutral'

# Function to fetch comments
def get_comments_and_title(video_id):
    youtube = build('youtube', 'v3', developerKey=api_key)

    # Get video title
    video_request = youtube.videos().list(
        part="snippet",
        id=video_id
    )
    video_response = video_request.execute()
    video_title = video_response["items"][0]["snippet"]["title"]

    # Fetch comments
    comments = []
    nextPageToken = None
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

    return comments, video_title


# Streamlit UI

st.title("YouTube Sentiment Analyzer 🎯")

video_url = st.text_input("Enter YouTube Video URL")

if video_url:
    try:
        # Extract video ID automatically
        if "v=" in video_url:
            video_id = video_url.split("v=")[1].split("&")[0]
        elif "youtu.be/" in video_url:
            video_id = video_url.split("youtu.be/")[1].split("?")[0]
        elif "live/" in video_url:
            video_id = video_url.split("live/")[1].split("?")[0]
        else:
            st.error("Invalid URL format!")
            st.stop()

        st.write("Fetching comments...")
        comments, video_title = get_comments_and_title(video_id)
        st.subheader(f"🎥 Video Title: {video_title}")

        st.write(f"Total comments fetched: {len(comments)}")

        sentiments = [get_sentiment(comment) for comment in comments]
        sentiment_counts = pd.Series(sentiments).value_counts()

        # Pie chart
        plt.figure(figsize=(5, 5))
        sentiment_counts.plot(kind='pie', autopct='%1.1f%%')
        plt.title("Sentiment Analysis of YouTube Comments")
        st.pyplot(plt)

    except Exception as e:
        st.error(f"Error: {e}")

