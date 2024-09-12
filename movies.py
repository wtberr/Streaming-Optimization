import requests
import random
from datasets import load_dataset

# Hugging Face API URL and Token
API_URL = "https://api-inference.huggingface.co/models/gpt2"
headers = {"Authorization": "Bearer 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"}


# Function to generate a recommendation for a given movie
def generate_recommendation(movie_title):
    prompt = f"Give me a short recommendation for the movie '{movie_title}' as if you're a friend recommending it."
    response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
    result = response.json()

    # Extract the text from the model response
    return result[0]['generated_text'].strip().lower()


# Create a dictionary with movie titles and corresponding recommendations
def create_movie_recommendation_dict(movie_titles):
    movie_dict = {}
    random_movies = random.sample(movie_titles, 100)  # Randomly pick 100 unique movie titles
    for movie in random_movies:
        recommendation = generate_recommendation(movie)
        movie_dict[movie] = recommendation
    return movie_dict


# OMDb API key
OMDB_API_KEY = 'ab4301c4'


# Function to fetch movie data and create the combined string without labels, punctuation, or capitalization
def get_movie_data(movie_title, movie_recommendations):
    """Fetch movie data and return a continuous string of plot, actors, director, writer, and production."""
    url = f"http://www.omdbapi.com/?t={movie_title}&apikey={OMDB_API_KEY}"
    response = requests.get(url)
    movie_data = response.json()

    if movie_data['Response'] == 'True':
        # Extract fields, remove punctuation, convert to lowercase
        plot = movie_data.get('Plot', '').lower()
        actors = movie_data.get('Actors', '').lower()
        director = movie_data.get('Director', '').lower()
        writer = movie_data.get('Writer', '').lower()
        production = movie_data.get('Production', '').lower()
        genre = movie_data.get('Genre', '').split(', ')

        # Combine all the elements into a string without labels or punctuation
        combined_info = f"{plot} {actors} {director} {writer} {production}".replace(',', '')
        return [movie_recommendations[movie_title], combined_info.strip(), genre]  # Remove any extra spaces
    else:
        return f"Error: {movie_data.get('Error', 'Unknown error occurred')}"


# Create a dictionary for the movies with recommendations, continuous string, and genres
def create_movies_dict():
    # Load the dataset
    ds = load_dataset("wykonos/movies", split='train[:500]')

    # Extract movie titles from the dataset
    movie_titles = [item['title'] for item in ds]  # Assuming 'title' is the field name for the movie title

    # Generate the dictionary of recommendations
    movie_recommendations = create_movie_recommendation_dict(movie_titles)

    movies_dict = {}

    # Loop through the movie recommendations and populate the dictionary
    for movie in movie_recommendations:
        movies_dict[movie] = get_movie_data(movie, movie_recommendations)

    return movies_dict


# Example movie dictionary with movie names, recommendations, overviews, and genres
movies = {
    "The Shawshank Redemption": [
        "A classic tale of hope and friendship",
        "Two imprisoned men bond over a number of years finding solace and eventual redemption through acts of common decency",
        ["Thriller"]
    ],
    "The Godfather": [
        "A must-watch for anyone who loves crime dramas",
        "The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son",
        ["Action", "Thriller"]
    ],
    "Inception": [
        "A mind-bending thriller that challenges your perception of reality",
        "A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a CEO",
        ["Thriller", "Action"]
    ],
    "The Dark Knight": [
        "An unforgettable superhero movie with a compelling villain",
        "When the menace known as the Joker emerges from his mysterious past he wreaks havoc and chaos on the people of Gotham",
        ["Action", "Thriller"]
    ],
    "Pulp Fiction": [
        "A wild ride of intertwining stories and dark humor",
        "The lives of two mob hitmen a boxer a gangster and his wife and a pair of diner bandits intertwine in four tales of violence and redemption",
        ["Thriller", "Comedy"]
    ],
    "Forrest Gump": [
        "A heartwarming story about an extraordinary man living through historic moments",
        "The presidencies of Kennedy and Johnson the events of Vietnam Watergate and other historical events unfold from the perspective of an Alabama man with an IQ of 75",
        ["Romance", "Comedy"]
    ],
    "Fight Club": [
        "A brutal commentary on consumerism and masculinity",
        "An insomniac office worker and a devil-may-care soap maker form an underground fight club that evolves into something much more",
        ["Thriller"]
    ],
    "The Matrix": [
        "A revolutionary sci-fi film that changed the genre",
        "A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers",
        ["Action", "Thriller"]
    ],
    "Interstellar": [
        "An epic space adventure that explores the limits of human survival",
        "A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival",
        ["Thriller", "Romance"]
    ],
    "Gladiator": [
        "A gripping historical drama filled with action and intrigue",
        "A former Roman General sets out to exact vengeance against the corrupt emperor who murdered his family and sent him into slavery",
        ["Action", "Thriller"]
    ],
    "Jurassic Park": [
        "An iconic film that brings dinosaurs back to life",
        "During a preview tour a theme park suffers a major power breakdown that allows its cloned dinosaur exhibits to run amok",
        ["Thriller", "Action"]
    ],
    "Braveheart": [
        "A stirring tale of rebellion and freedom",
        "Scottish warrior William Wallace leads his countrymen in a rebellion to free his homeland from the tyranny of King Edward I of England",
        ["Action", "Romance"]
    ],
    "The Silence of the Lambs": [
        "A psychological thriller with chilling performances",
        "A young FBI cadet must receive the help of an incarcerated and manipulative cannibal killer to help catch another serial killer",
        ["Thriller", "Horror"]
    ],
    "Schindler's List": [
        "A deeply moving historical drama",
        "In German-occupied Poland during World War II industrialist Oskar Schindler gradually becomes concerned for his Jewish workforce after witnessing their persecution by the Nazis",
        ["Romance", "Thriller"]
    ],
    "Saving Private Ryan": [
        "A powerful war film that honors those who served",
        "Following the Normandy Landings a group of US soldiers go behind enemy lines to retrieve a paratrooper whose brothers have been killed in action",
        ["Action", "Romance"]
    ],
    "The Departed": [
        "A gripping crime thriller about loyalty and betrayal",
        "An undercover cop and a mole in the police attempt to identify each other while infiltrating an Irish gang in South Boston",
        ["Thriller", "Action"]
    ],
    "Whiplash": [
        "An intense drama about the pursuit of perfection",
        "A promising young drummer enrolls at a cutthroat music conservatory where his dreams of greatness are mentored by an instructor who will stop at nothing to realize a student's potential",
        ["Thriller"]
    ],
    "The Prestige": [
        "A fascinating story about the rivalry between two magicians",
        "After a tragic accident two stage magicians engage in a battle to create the ultimate illusion while sacrificing everything they have to outwit each other",
        ["Thriller", "Action"]
    ],
    "The Wolf of Wall Street": [
        "A wild true story of excess and corruption in the financial world",
        "Based on the true story of Jordan Belfort from his rise to a wealthy stockbroker living the high life to his fall involving crime corruption and the federal government",
        ["Comedy", "Thriller"]
    ],
    "Django Unchained": [
        "A thrilling revenge tale set in the pre-Civil War South",
        "With the help of a German bounty hunter a freed slave sets out to rescue his wife from a brutal Mississippi plantation owner",
        ["Action", "Romance"]
    ],
    "The Social Network": [
        "A gripping account of the founding of Facebook",
        "Harvard student Mark Zuckerberg creates the social networking site that would become known as Facebook but is later sued by two brothers who claimed he stole their idea",
        ["Thriller"]
    ],
    "Good Will Hunting": [
        "An emotionally resonant drama about genius and self-discovery",
        "Will Hunting a janitor at MIT has a gift for mathematics but needs help from a psychologist to find direction in his life",
        ["Romance"]
    ],
    "The Grand Budapest Hotel": [
        "A quirky and visually stunning adventure",
        "A writer encounters the owner of an aging high-class hotel who tells him of his early years serving as a lobby boy in the hotel's glorious years under an exceptional concierge",
        ["Comedy", "Thriller"]
    ],
    "Her": [
        "A thought-provoking love story about technology and connection",
        "In a near future a lonely writer develops an unlikely relationship with an operating system designed to meet his every need",
        ["Romance"]
    ],
    "Mad Max Fury Road": [
        "A high-octane action-packed post-apocalyptic adventure",
        "In a post-apocalyptic wasteland a woman rebels against a tyrannical ruler in search for her homeland with the aid of a group of female prisoners a psychotic worshipper and a drifter named Max",
        ["Action", "Thriller"]
    ],
    "Shutter Island": [
        "A mind-bending psychological thriller",
        "In 1954 a US Marshal investigates the disappearance of a murderer who escaped from a hospital for the criminally insane",
        ["Thriller"]
    ],
    "Se7en": [
        "A gripping and dark crime thriller",
        "Two detectives a rookie and a veteran hunt a serial killer who uses the seven deadly sins as his motives",
        ["Thriller", "Horror"]
    ],
    "Blade Runner 2049": [
        "A visually stunning and deeply thoughtful sci-fi epic",
        "A young blade runner's discovery of a long-buried secret leads him to track down former blade runner Rick Deckard who's been missing for thirty years",
        ["Action", "Thriller"]
    ],
    "The Imitation Game": [
        "A compelling story of genius and tragedy",
        "During World War II the English mathematical genius Alan Turing tries to crack the German Enigma code with help from fellow mathematicians",
        ["Thriller", "Romance"]
    ],
    "La La Land": [
        "A delightful musical romance full of heart",
        "While navigating their careers in Los Angeles a pianist and an actress fall in love while attempting to reconcile their aspirations for the future",
        ["Romance", "Comedy"]
    ],
    "The Irishman": [
        "An epic tale of crime loyalty and regret",
        "A mob hitman recalls his possible involvement with the slaying of Jimmy Hoffa",
        ["Action", "Thriller"]
    ],
    "Joker": [
        "A haunting character study of a man pushed to his limits",
        "In Gotham City mentally troubled comedian Arthur Fleck is disregarded and mistreated by society turning to a life of crime and chaos",
        ["Thriller"]
    ],
    "Parasite": [
        "A darkly funny and shocking social thriller",
        "Greed and class discrimination threaten the newly formed symbiotic relationship between the wealthy Park family and the destitute Kim clan",
        ["Thriller", "Comedy"]
    ],
    "The Lion King": [
        "A beloved animated classic for all ages",
        "Lion prince Simba and his father are targeted by his bitter uncle who wants to ascend the throne himself",
        ["Action", "Romance"]
    ],
    "Spirited Away": [
        "A magical and heartwarming animated adventure",
        "During her family's move to the suburbs a sullen 10-year-old girl wanders into a world ruled by gods witches and spirits where humans are changed into beasts",
        ["Romance", "Comedy"]
    ],
    "Titanic": [
        "A sweeping romantic tragedy set against a historical event",
        "A seventeen-year-old aristocrat falls in love with a kind but poor artist aboard the luxurious ill-fated RMS Titanic",
        ["Romance"]
    ],
    "The Terminator": [
        "A thrilling sci-fi action classic",
        "A human soldier is sent from 2029 to 1984 to stop an almost indestructible cyborg killing machine sent from the same year which has been programmed to execute a young woman whose unborn son is the key to humanity's future salvation",
        ["Action", "Thriller"]
    ],
    "Alien": [
        "A tense and terrifying sci-fi horror",
        "After a space merchant vessel receives an unknown transmission as a distress call one of the crew is attacked by a mysterious life form and they soon realize that its life cycle has merely begun",
        ["Horror", "Thriller"]
    ]
}

