import matplotlib.pyplot as plt
import numpy as np

# Points and their corresponding colors
points = [(-1, -1), (-1, 1), (1, 1), (1, -1)]
colors = ['blue', 'red', 'blue', 'red']

# Plot the points with filled circles and corresponding colors using plt.plot
for (x, y), color in zip(points, colors):
    plt.plot(x, y, marker='o', color=color, markersize=10, linestyle='')  # using colored filled circles with plt.plot

# Create x values for plotting the line y = x + 1
x_values = np.linspace(-2, 2, 400)
y_values = x_values + 1

# Plot the line y = x + 1
# plt.plot(x_values, y_values, label='y = x + 1', color='green')
plt.plot(x_values, y_values, linestyle='--')

# Make units on x and y axis equal
plt.axis('equal')

# Add x and y axes that intersect at (0, 0)
# plt.axhline(0, color='black', lw=0.5)
# plt.axvline(0, color='black', lw=0.5)

# Set the aspect ratio to 1
plt.gca().set_aspect('equal', adjustable='box')

# Set the x and y axis limits
plt.xlim(-2, 2)
plt.ylim(-2, 2)

# Show the plot
# plt.legend() # No faint rectangle in the upper right hand corner
plt.show()
