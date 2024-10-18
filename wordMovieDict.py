from transformers import DistilBertTokenizer, DistilBertModel
import torch
from movies import movies  # Assuming the movie dictionary is already imported

# Load DistilBERT tokenizer and model
tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
model = DistilBertModel.from_pretrained('distilbert-base-uncased')


def get_distilbert_token_embeddings(text):
    """Get DistilBERT token embeddings for the input text."""
    inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)

    # Get the token embeddings (hidden states from the last layer)
    token_embeddings = outputs.last_hidden_state.squeeze(0)  # Shape: (sequence_length, hidden_size)
    return token_embeddings, inputs['input_ids'][0]  # Return both embeddings and token IDs


def max_pooling(token_embeddings):
    """Perform max pooling over token embeddings (over the sequence dimension)."""
    # Max pooling over the sequence length dimension (dim=0)
    max_pooled_embedding, _ = torch.max(token_embeddings, dim=0)
    return max_pooled_embedding


def build_word_movie_dict(movies):
    """Build a dictionary where the keys are words selected by max pooling, and values are lists of movies."""
    word_movie_dict = {}

    for movie, details in movies.items():
        movie_text = f"{details[0]} {details[1]}"  # Combine title and synopsis
        token_embeddings, input_ids = get_distilbert_token_embeddings(movie_text)

        # Perform max pooling over the token embeddings
        max_pooled_embedding = max_pooling(token_embeddings)

        # Find the token indices corresponding to the max-pooled embedding
        max_token_ids = (token_embeddings == max_pooled_embedding.unsqueeze(0)).nonzero(as_tuple=False)[:, 0]

        # Get the words corresponding to the max token IDs
        max_tokens = tokenizer.convert_ids_to_tokens(input_ids[max_token_ids])

        # Add the movie to the dictionary for each word in max_tokens
        for token in max_tokens:
            if token not in word_movie_dict:
                word_movie_dict[token] = []
            word_movie_dict[token].append(movie)

    return word_movie_dict


# Build the word-movie dictionary
word_movie_dict = build_word_movie_dict(movies)

# Print the resulting dictionary
for word, movie_list in word_movie_dict.items():
    print(f"{word}: {movie_list}")
