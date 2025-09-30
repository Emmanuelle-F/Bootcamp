import numpy as np

# Movie ratings matrix (5 viewers, 3 movies)
movie_ratings = np.array([
    [5, 1, 4],
    [4, 4, 2],
    [4, 3, 5],
    [1, 1, 5],
    [3, 2, 1]
])

# Tasks: Calculate average ratings for each movie and analyze viewer preferences

average_ratings = np.mean(movie_ratings, axis = 0)  # axis 0 => columns
print("Average Ratings:", average_ratings)

viewer_preference = np.argmax(movie_ratings, axis = 1) + 1  # axis 1 => rows
print("Viewer Preferances:", viewer_preference)