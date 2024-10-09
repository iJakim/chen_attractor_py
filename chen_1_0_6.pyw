import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
import random
from matplotlib import cm  # For color maps

# Chen attractor system of equations
def chen_attractor(t, state):
    x, y, z = state
    dxdt = 400 * (y - x)
    dydt = -120 * x - 10 * x * z + 280 * y
    dzdt = 10 * x * y - 30 * z
    return [dxdt, dydt, dzdt]

# Choose random initial conditions within some range
initial_state = [random.uniform(-10, 10) for _ in range(3)]
initial_state[2] += 25

# Time span and evaluation points
t_span = (0, 10)  # Time span for the integration
t_eval = np.linspace(t_span[0], t_span[1], 10000)  # Time points where solution is evaluated

# Solve the system of equations
sol = solve_ivp(chen_attractor, t_span, initial_state, t_eval=t_eval)

# Extract the solution (x, y, z coordinates over time)
x = sol.y[0]
y = sol.y[1]
z = sol.y[2]

# Create a 3D plot for animation
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Set background color to black
fig.patch.set_facecolor('black')  # Background color of the figure
ax.set_facecolor('black')         # Background color of the 3D plot

# Set up the plot limits
ax.set_xlim(np.min(x), np.max(x))
ax.set_ylim(np.min(y), np.max(y))
ax.set_zlim(np.min(z), np.max(z))

# Remove the axes and grid
ax.set_axis_off()  # Hide the axes
ax.grid(False)     # Turn off the grid

# List to store line segments
lines = []

# Initialization function for the animation
def init():
    return lines

# Update function for the animation with rotation and color change
def update(frame):
    # Number of points to add in each frame
    step_size = 3

    # Get the segment of the attractor to plot
    i_start = max(0, frame * step_size - 1)
    i_end = (frame + 1) * step_size
    if i_end > len(x):
        i_end = len(x)

    # Skip if we've already plotted all points
    if i_start >= len(x):
        return lines

    # Change the line color gradually through the HSV spectrum
    hue = (frame // 1) % 360 / 360  # One full cycle every 360 frames (360*1)
    color = cm.hsv(hue)  # Get the color from the HSV colormap

    # Plot the segment with the new color
    line, = ax.plot(x[i_start:i_end], y[i_start:i_end], z[i_start:i_end], color=color, lw=1)
    lines.append(line)  # Store the new segment

    # Rotate the view around the z-axis
    ax.view_init(elev=30, azim=frame)

    return lines

# Create the animation (without blitting for smoother rotation)
ani = FuncAnimation(fig, update, frames=len(t_eval)//10, init_func=init, interval=30, blit=False)

# Show the plot
plt.show()