from flask import Flask, render_template, jsonify
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import matplotlib

# Use non-GUI backend for Matplotlib (headless)
matplotlib.use('Agg')

app = Flask(__name__)

# Ensure static directory exists
STATIC_DIR = os.path.abspath("static")  # Use absolute path for static directory
print(f"static dirctory path: {STATIC_DIR}")  # Debug print

if not os.path.exists(STATIC_DIR):
    os.makedirs(STATIC_DIR)
    print(f"created staic directry at: {STATIC_DIR}")
else:
    print(f"static directory already exists at: {STATIC_DIR}")

# Check current working directry
print(f"Current working directory: {os.getcwd()}")

# Load dataset (ensure the correct path to the CSV file)
data = pd.read_csv('cleaned_taylor_swift_spotify.csv')

#  here this code is then converting the  duration colume  from milliseconds to minutes
data['duration_minutes'] = data['duration_ms'] / 60000

# Generate and save visualizations
def generate_visuals():
    try:
        print("Generting visual...") 
        # Pie Chart: Distribuion of tracks across albums
        album_counts = data['album'].value_counts()
        print(f"Album counts: {album_counts}")  # Debug print
        plt.figure(figsize=(8, 8))
        plt.pie(album_counts, labels=album_counts.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette('pastel'))
        pie_chart_path = os.path.join(STATIC_DIR, 'album_distribution.png')
        print(f"Saving pie chart to: {pie_chart_path}")  
        plt.savefig(pie_chart_path)
        print(f"Saved: {pie_chart_path}")
        plt.close()

        # Bar Chart: Popularity of tracks
        plt.figure(figsize=(10, 6))
        sns.barplot(x='popularity', y='name', data=data.sort_values('popularity', ascending=False).head(10), palette='viridis')
        plt.title('Top 10 Tracks by Popularity')
        plt.xlabel('Popularity')
        plt.ylabel('Track Name')
        bar_chart_path = os.path.join(STATIC_DIR, 'top_tracks.png')
        print(f"Saving bar chart to: {bar_chart_path}")  
        plt.savefig(bar_chart_path)
        print(f"Saved: {bar_chart_path}")
        plt.close()

        # Histogram: Track durations
        plt.figure(figsize=(10, 6))
        sns.histplot(data['duration_minutes'].dropna(), bins=20, kde=True, color='teal')
        plt.title('Distribution of Track Durations (in minutes)')
        plt.xlabel('Duration (minutes)')
        plt.ylabel('Count')
        hist_chart_path = os.path.join(STATIC_DIR, 'track_durations.png')
        print(f"saving histogram to: {hist_chart_path}")  # Debug print
        plt.savefig(hist_chart_path)
        print(f"Saved: {hist_chart_path}")
        plt.close()

        # Scatter Plot: Loudness vs. Popularity
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x='loudness', y='popularity', data=data.dropna(subset=['loudness', 'popularity']), hue='album', palette='tab10', alpha=0.7)
        plt.title('Loudness vs. Popularity')
        plt.xlabel('Loudness (dB)')
        plt.ylabel('Popularity')
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        scatter_chart_path = os.path.join(STATIC_DIR, 'loudness_vs_popularity.png')
        print(f"Saving scatter plot to: {scatter_chart_path}") 
        plt.savefig(scatter_chart_path)
        print(f"Saved: {scatter_chart_path}")
        plt.close()

    except Exception as e:
        print(f"Error generating visuals: {e}")

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
    
    generate_visuals()  
    app.run(debug=True)
