import tkinter as tk
from tkinter import Label, Canvas, Frame, Scrollbar
from PIL import Image, ImageTk
import requests
from io import BytesIO
from transformers import DistilBertTokenizer, DistilBertModel
from sentence_transformers import SentenceTransformer
import numpy as np
import random
from movies import movies

# Load DistilBERT tokenizer and model
tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# OMDb API key
OMDB_API_KEY = 'ab4301c4'

# Initialize global variables
selected_phrases = []
recommended_movies = []
ranked_movies = []

# List of 20 movie descriptions
movie_phrases = [
    "Heartwarming family adventure", "Dark psychological thriller", "Romantic comedy drama",
    "Intense crime mystery", "Epic fantasy saga", "Action-packed superhero film", "Mind-bending sci-fi",
    "Gripping political drama", "Inspiring true story", "Uplifting feel-good comedy", "Emotional coming-of-age",
    "Suspenseful detective story", "Visually stunning animation", "Dark supernatural horror",
    "Light-hearted romantic comedy", "Gritty crime drama", "High-stakes courtroom drama",
    "Fast-paced action thriller", "Historical war epic", "Witty satirical comedy"
]

# Set of genres
genres = {'Action', 'Western', 'Political Drama', 'Family', 'Music', 'Political Thriller', 'Romance',
          'Teen Drama', 'Medical Drama', 'Sci-Fi', 'Political', 'Horror', 'Sports', 'Fantasy',
          'Biography', 'Anime', 'Dystopian', 'Historical Drama', 'Musical', 'Animation', 'Drama',
          'Superhero', 'Comedy', 'Mystery', 'Legal Drama', 'Anthology', 'War', 'Spy', 'Historical',
          'Thriller', 'Adventure', 'Crime'}


def filter_movies_by_genre(selected_phrases, user_input):
    """Filter and return movies that match the selected genres, and apply special handling for anime/animation."""
    filtered_movies = {}

    # If 'anime' or 'animation' is in the user input, only show those genres
    if 'anime' in user_input.lower() or 'animation' in user_input.lower():
        for movie, details in movies.items():
            if 'Anime' in details[2] or 'Animation' in details[2]:
                filtered_movies[movie] = details
    else:
        filtered_movies = movies  # If no specific filter, return all movies

    return filtered_movies


def get_distilbert_embedding(text):
    """Get DistilBERT embedding for the input text."""
    return model.encode(text)


def rank_movies_by_similarity(user_input, recommended_movies):
    """Rank the recommended movies based on similarity to user input using DistilBERT embeddings."""
    user_embedding = get_distilbert_embedding(user_input)
    ranked_movies = []

    for movie, details in recommended_movies.items():
        movie_text = f"{details[0]} {details[1]}"  # Combine title and synopsis
        movie_embedding = get_distilbert_embedding(movie_text)

        # Compute cosine similarity between user input and movie description
        similarity_score = np.dot(user_embedding, movie_embedding) / (
                np.linalg.norm(user_embedding) * np.linalg.norm(movie_embedding))

        # Check for genre matches and apply the 30% boost for each match
        movie_genres = details[2]
        for genre in genres:
            if genre.lower() in user_input.lower() and genre in movie_genres:
                similarity_score *= 1.3  # Apply the 30% boost for each matching genre

        ranked_movies.append((movie, similarity_score))

    # Sort movies by similarity in descending order
    ranked_movies.sort(key=lambda x: x[1], reverse=True)

    return ranked_movies[:10]  # Return the top 10 most similar movies


def fetch_poster_image(movie_title):
    """Fetch the movie poster URL from OMDb API and return the image."""
    url = f"http://www.omdbapi.com/?t={movie_title}&apikey={OMDB_API_KEY}"
    response = requests.get(url)
    data = response.json()

    if 'Poster' in data and data['Poster'] != 'N/A':
        poster_url = data['Poster']
        response = requests.get(poster_url)
        img_data = response.content
        img = Image.open(BytesIO(img_data))
        return img
    else:
        return None


def display_recommendations():
    """Display the top 10 recommendations and their posters on the window in a scrollable frame."""
    # Clear the window
    for widget in window.winfo_children():
        widget.destroy()

    # Create a scrollable canvas
    canvas = Canvas(window)
    scroll_y = Scrollbar(window, orient="vertical", command=canvas.yview)

    scrollable_frame = Frame(canvas)

    # Update the scroll region after adding widgets
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scroll_y.set)

    # Add a new label for "Top Recommendations"
    label = tk.Label(scrollable_frame, text="Top Results from Friends' Recommendations", font=("Arial", 14))
    label.pack(pady=10)

    # Display the top 10 ranked movies and their posters
    for idx, (movie, score) in enumerate(ranked_movies):
        # Display movie title
        title_label = tk.Label(scrollable_frame, text=f"{idx + 1}. {movie} - Similarity: {score:.2f}")
        title_label.pack(pady=2)

        # Fetch and display the poster
        poster_img = fetch_poster_image(movie)
        if poster_img:
            poster_img = poster_img.resize((150, 220))  # Resize image to fit
            poster_tk = ImageTk.PhotoImage(poster_img)
            poster_label = Label(scrollable_frame, image=poster_tk)
            poster_label.image = poster_tk  # Keep reference to avoid garbage collection
            poster_label.pack(pady=5)

    # Pack and configure scrollable canvas and scrollbar
    canvas.pack(side="left", fill="both", expand=True)
    scroll_y.pack(side="right", fill="y")

    # Update the window to listen for "Enter" key to close
    window.bind("<Return>", close_window)


def close_window(event=None):
    """Close the window after showing recommendations."""
    window.quit()


def on_enter(event=None):
    """Handle the first Enter press to get recommendations and update the window."""
    global answer, recommended_movies, ranked_movies
    answer = entry.get()  # Get the text from the entry bar

    if not answer and selected_phrases:
        answer = " ".join(selected_phrases)  # Concatenate the selected phrases

        # If there's still no input (i.e., user didn't click any button or type anything)
    if not answer:
        print("No input or selections made.")
        return  # Exit if nothing is provided to avoid processing

    # Filter movies based on selected phrases and handle anime/animation filter
    recommended_movies = filter_movies_by_genre(selected_phrases, answer)

    if recommended_movies:
        # Rank the recommended movies based on user input similarity
        ranked_movies = rank_movies_by_similarity(answer, recommended_movies)

        # Update the window to show top 10 recommendations
        display_recommendations()
    else:
        print("No movies found for the selected input.")


def append_phrase(phrase):
    """Append the selected phrase to the user's input in the entry field."""
    current_text = entry.get()
    updated_text = current_text + " " + phrase
    entry.delete(0, tk.END)
    entry.insert(0, updated_text)


# Create the main window
window = tk.Tk()
window.title("Mood Question")

# Create a scrollable canvas
canvas = Canvas(window)
scrollbar = Scrollbar(window, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)

# Create a frame inside the canvas to hold the buttons and text bar
scrollable_frame = Frame(canvas)
scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

# Pack the canvas and scrollbar
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

# Create the label and entry field
label = tk.Label(scrollable_frame, text="What are you in the mood for?", font=("Arial", 14))
label.grid(row=0, column=0, columnspan=10, pady=10)  # Span across 10 columns

entry = tk.Entry(scrollable_frame, width=50)
entry.grid(row=1, column=0, columnspan=10, pady=10)  # Span across 10 columns

# Randomly select 10 phrases from movie_phrases
random_phrases = random.sample(movie_phrases, 10)

# Create buttons for the random movie phrases
for index, phrase in enumerate(random_phrases):
    button = tk.Button(scrollable_frame, text=phrase, width=25, command=lambda p=phrase: append_phrase(p))
    row = (index // 2) + 2  # Place in rows starting from row 2
    col = index % 2  # Arrange in two columns
    button.grid(row=row, column=col, padx=5, pady=5)  # Add padding for spacing

# Bind the Enter key to the on_enter function
entry.bind("<Return>", on_enter)

# Run the window
window.mainloop()
