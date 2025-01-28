import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
data = pd.read_csv('cleaned_taylor_swift_spotify.csv')

# Pie Chart: Distribution of tracks across albums
album_counts = data['album'].value_counts()
plt.figure(figsize=(8, 8))
plt.pie(album_counts, labels=album_counts.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette('pastel'))
plt.title('tracks per album')
plt.show()

# Bar Chart: Popularity of tracks
plt.figure(figsize=(10, 6))
sns.barplot(x='popularity', y='name', data=data.sort_values('popularity', ascending=False).head(10), palette='viridis')
plt.title('Top 10 Tracks by Popularity')
plt.xlabel('Popularity')
plt.ylabel('Track Name')
plt.show()



# Scatter Plot: Loudness vs. Popularity
plt.figure(figsize=(10, 6))
sns.scatterplot(x='loudness', y='popularity', data=data, hue='album', palette='tab10', alpha=0.7)
plt.title('Loudness vs. Popularity')
plt.xlabel('Loudness (dB)')
plt.ylabel('Popularity')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()

# Line Plot: Average acousticness per album
average_acousticness = data.groupby('album')['acousticness'].mean().sort_values()
plt.figure(figsize=(12, 6))
average_acousticness.plot(kind='line', marker='o', color='purple')
plt.title('Average Acousticness per Album')
plt.xlabel('Album')
plt.ylabel('Average Acousticness')
plt.xticks(rotation=90)
plt.grid(True)
plt.show()
