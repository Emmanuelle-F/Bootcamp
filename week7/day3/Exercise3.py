import numpy as np

# Temperature data matrix (4 cities, 7 days)
temperature_data = np.array([
    [27, 20, 15, 18, 26, 18, 22],
    [24, 18, 20, 17, 19, 22, 21],
    [23, 23, 27, 25, 16, 21, 22],
    [22, 29, 23, 16, 20, 24, 28]
])

# Tasks: Calculate average, max, min temperatures and make day comparisons

average_temp = np.mean(temperature_data, axis = 1)
print("Average Temperature:", average_temp)

min_temp = np.min(temperature_data, axis=1)
print("Min Temperature:", min_temp)

max_temp = np.max(temperature_data, axis=1)
print("Max Temperature:", max_temp)

average_per_day = np.mean(temperature_data, axis=0)
print("Average Temperature per day:", average_per_day)

max_per_day = np.max(temperature_data, axis=0)
print("Max Temperature per day:", max_per_day)

min_per_day = np.min(temperature_data, axis=0)
print("Min Temperature per day:", min_per_day)

