from movies import movies
unique_genres = set()

# Loop through the movies dictionary
for movie, details in movies.items():
    genres = details[2]  # The third entry in the list is the genres list
    unique_genres.update(genres)  # Add genres to the set (set automatically handles duplicates)

# Print the set of unique genres
print(unique_genres)