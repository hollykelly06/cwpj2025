from flask import Flask, jsonify, request, render_template
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

# Global dataframe to hold uploaded data
df = pd.DataFrame()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_data():
    global df
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No file provided"}), 400

    try:
        # Read the CSV and clean data
        df = pd.read_csv(file)
        df = df.dropna()  # Drop rows with missing values
        if "album" not in df.columns or "popularity" not in df.columns:
            return jsonify({"error": "File must contain 'album' and 'popularity' columns"}), 400

        return jsonify({"message": "Dataset uploaded and processed successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/analytics")
def analytics():
    if df.empty:
        return jsonify({"error": "No data available. Upload a dataset first."}), 400

    # Compute album counts
    album_counts = df["album"].value_counts().to_dict()

    # Compute average popularity by album
    popularity = df.groupby("album")["popularity"].mean().sort_values(ascending=False).to_dict()

    return jsonify({
        "album_counts": album_counts,
        "popularity": popularity
    })

@app.route("/chart")
def chart():
    if df.empty:
        return jsonify({"error": "No data available. Upload a dataset first."}), 400

    try:
        # Create a chart for top 5 albums by song count
        top_albums = df["album"].value_counts().head(5)
        plt.figure(figsize=(8, 6))
        plt.bar(top_albums.index, top_albums.values, color="skyblue")
        plt.title("Top 5 Albums by Number of Songs")
        plt.xlabel("Albums")
        plt.ylabel("Number of Songs")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()

        # Save the chart as a base64 image
        buffer = io.BytesIO()
        plt.savefig(buffer, format="png")
        buffer.seek(0)
        img = base64.b64encode(buffer.read()).decode("utf-8")
        buffer.close()
        plt.close()

        return jsonify({"chart": f"data:image/png;base64,{img}"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
