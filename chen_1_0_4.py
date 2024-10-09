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

# Initialize the line object for animation
line, = ax.plot([], [], [], lw=1)

# Initialization function for the animation
def init():
    line.set_data([], [])
    line.set_3d_properties([])
    return line,

# Update function for the animation with rotation and color change
def update(frame):
    # Update the data for the attractor
    line.set_data(x[:frame], y[:frame])
    line.set_3d_properties(z[:frame])
    
    # Rotate the view around the z-axis
    ax.view_init(elev=30, azim=frame)

    # Change the line color gradually through the HSV spectrum
    hue = (frame // 20) % 360 / 360  # One full cycle every 7200 frames (360*20)
    color = cm.hsv(hue)  # Get the color from the HSV colormap
    line.set_color(color)
    
    return line,

# Create the animation (without blitting for smoother rotation)
ani = FuncAnimation(fig, update, frames=len(t_eval), init_func=init, interval=30)

# Show the plot
plt.show()