import tkinter as tk
from tkinter import Label, Canvas, Frame, Scrollbar
from PIL import Image, ImageTk
import requests
from io import BytesIO
from transformers import DistilBertTokenizer, DistilBertModel
import torch
from sklearn.metrics.pairwise import cosine_similarity
from movies import movies


# Load DistilBERT tokenizer and model
tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
model = DistilBertModel.from_pretrained('distilbert-base-uncased')

# OMDb API key
OMDB_API_KEY = 'ab4301c4'

# Initialize global variables
selected_genres = []
recommended_movies = []
ranked_movies = []


def toggle_genre(genre, button):
    """Toggle the genre button on and off, updating the selected_genres list."""
    if genre in selected_genres:
        selected_genres.remove(genre)
        button.config(bg="SystemButtonFace")  # Reset to default color
    else:
        selected_genres.append(genre)
        button.config(bg="gray")  # Darken when selected


def filter_movies_by_genre(selected_genres):
    """Filter and return movies that match the selected genres."""
    matching_movies = {}
    if selected_genres:
        for movie, details in movies.items():
            movie_genres = details[2]  # The third element in the list is the genres list
            if any(genre in movie_genres for genre in selected_genres):  # If there's a genre match
                matching_movies[movie] = details
    else:
        matching_movies = movies  # If no genre is selected, return all movies
    return matching_movies


def get_distilbert_embedding(text):
    """Get DistilBERT embedding for the input text."""
    inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=512)
    with torch.no_grad():  # Disable gradient calculations to save memory
        outputs = model(**inputs)
    # Use the first token ([CLS]) for sentence-level embedding
    cls_embedding = outputs.last_hidden_state[:, 0, :].numpy()
    return cls_embedding


def rank_movies_by_similarity(user_input, recommended_movies):
    """Rank the recommended movies based on similarity to user input using DistilBERT embeddings."""
    user_embedding = get_distilbert_embedding(user_input)
    ranked_movies = []

    for movie, details in recommended_movies.items():
        movie_text = f"{details[0]} {details[1]}"  # Combine recommendation and synopsis
        movie_embedding = get_distilbert_embedding(movie_text)

        # Compute cosine similarity between user input and movie description
        similarity_score = cosine_similarity(user_embedding, movie_embedding)[0][0]
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
    global answer, genre, recommended_movies, ranked_movies
    answer = entry.get()  # Get the text from the entry bar
    genre = selected_genres.copy()  # Get the selected genres

    # Filter movies based on selected genres
    recommended_movies = filter_movies_by_genre(genre)

    if recommended_movies:
        # Rank the recommended movies based on user input similarity
        ranked_movies = rank_movies_by_similarity(answer, recommended_movies)

        # Update the window to show top 10 recommendations
        display_recommendations()
    else:
        print("No movies found for the selected genres.")


# Create the main window
window = tk.Tk()
window.title("Mood Question")

# Create a scrollable canvas
canvas = Canvas(window)
scrollbar = Scrollbar(window, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)

# Create a frame inside the canvas to hold the genre buttons and text bar
scrollable_frame = Frame(canvas)
scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

# Pack the canvas and scrollbar
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

# Add a label at the top
label = tk.Label(scrollable_frame, text="What are you in the mood for?", font=("Arial", 14))
label.pack(pady=10)

# Create buttons for genres
genres = [
    "Action", "Adult", "Adventure", "Animation", "Biography", "Comedy", "Crime",
    "Documentary", "Drama", "Family", "Fantasy", "Film Noir", "Game Show",
    "History", "Horror", "Musical", "Music", "Mystery", "News", "Reality-TV",
    "Romance", "Sci-Fi", "Short", "Sport", "Talk-Show", "Thriller", "War", "Western"
]

# Add genre buttons to the scrollable frame with proper command
for genre in genres:
    button = tk.Button(scrollable_frame, text=genre, width=10)
    button.config(command=lambda g=genre, b=button: toggle_genre(g, b))
    button.pack(pady=5)

# Create a text entry bar
entry = tk.Entry(scrollable_frame, width=50)
entry.pack(pady=10)

# Bind the Enter key to the on_enter function
entry.bind("<Return>", on_enter)

# Run the window
window.mainloop()
