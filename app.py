from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load dataset
movies = pd.read_csv('movie.csv')

# Show first rows
print(movies.head())

# Check columns
print(movies.columns)

# Get unique genres
all_genres = set()

for genre_list in movies['genres']:
    genres = str(genre_list).split('|')

    for genre in genres:
        all_genres.add(genre)

all_genres = sorted(list(all_genres))


@app.route('/', methods=['GET', 'POST'])
def home():

    recommendations = []

    if request.method == 'POST':

        selected_genre = request.form['genre']

        filtered_movies = movies[
            movies['genres'].str.contains(
                selected_genre,
                case=False,
                na=False
            )
        ]

        if len(filtered_movies) > 0:
            recommendations = filtered_movies['title'].sample(
                min(10, len(filtered_movies))
            ).tolist()

    return render_template(
        'index.html',
        genres=all_genres,
        recommendations=recommendations
    )


if __name__ == '__main__':
    app.run(debug=True)