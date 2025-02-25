from flask import Flask,render_template, jsonify
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

app = Flask(__name__)

# Ensure static directory exists
if not os.path.exists("static"):
    os.makedirs("static")

# Load dataset
data = pd.read_csv('cleaned_taylor_swift_spotify.csv')

# Convert duration from milliseconds to minutes for easier visualization
data['duration_minutes'] = data['duration_ms'] / 60000

# Generate and save visualizations
def generate_visuals():
    # Pie Chart: Distribution of tracks across albums
    album_counts = data['album'].value_counts()
    plt.figure(figsize=(8, 8))
    plt.pie(album_counts, labels=album_counts.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette('pastel'))
    plt.title('Distribution of Tracks Across Albums')
    plt.savefig('static/album_distribution.png')
    plt.close()

    # Bar Chart: Popularity of tracks
    plt.figure(figsize=(10, 6))
    sns.barplot(x='popularity', y='name', data=data.sort_values('popularity', ascending=False).head(10), palette='viridis')
    plt.title('Top 10 Tracks by Popularity')
    plt.xlabel('Popularity')
    plt.ylabel('Track Name')
    plt.savefig('static/top_tracks.png')
    plt.close()

    # Histogram: Track durations
    plt.figure(figsize=(10, 6))
    sns.histplot(data['duration_minutes'], bins=20, kde=True, color='teal')
    plt.title('Distribution of Track Durations (in minutes)')
    plt.xlabel('Duration (minutes)')
    plt.ylabel('Count')
    plt.savefig('static/track_durations.png')
    plt.close()

    # Scatter Plot: Loudness vs. Popularity
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='loudness', y='popularity', data=data, hue='album', palette='tab10', alpha=0.7)
    plt.title('Loudness vs. Popularity')
    plt.xlabel('Loudness (dB)')
    plt.ylabel('Popularity')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.savefig('static/loudness_vs_popularity.png')
    plt.close()

@app.route('/')
def index():
    generate_visuals()
    return render_template('index.html')

@app.route('/api/albums')
def get_albums():
    """Returns a list of all albums and their songs"""
    albums = data.groupby("album")["name"].apply(list).to_dict()
    return jsonify(albums)

@app.route('/api/songs')
def get_songs():
    """Returns a list of all songs with details"""
    songs = data.to_dict(orient="records")
    return jsonify(songs)

if __name__ == '__main__':
    app.run(debug=True)