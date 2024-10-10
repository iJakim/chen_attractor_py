import numpy as np
from mpl_toolkits.mplot3d.art3d import Line3D, Line3DCollection
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm  # For color maps

# Disable the toolbar using rcParams
plt.rcParams['toolbar'] = 'None'

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
fig = plt.figure(figsize=(12, 12), dpi=200)  # Increase DPI for higher resolution
ax: Axes3D = fig.add_subplot(111, projection='3d')

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

# Shift the plot to the left (by adjusting subplot's position)
# The values are in the format (left, bottom, width, height), between 0 and 1.
# Here we shift it 0.2 to the left, meaning 20% of the figure width.
ax.set_position([-0.1, 0.1, 1, 1])  # Shifting the plot to the left and using more space

# Make the plot fullscreen
manager = plt.get_current_fig_manager()
manager.full_screen_toggle()

# Event handler to close the program on pressing Escape
def on_key_press(event):
    if event.key == 'escape':
        plt.close(fig)

# Bind the key press event
fig.canvas.mpl_connect('key_press_event', on_key_press)

# Initialization function for the animation
def init():
    return []

idx = 0
coll = Line3DCollection([],linewidths=1)
ax.add_collection(coll)
segments = []
colors = []
rot = 0
# Update function for the animation with rotation and color change
def update(frame):
    global idx, rot
    # Number of points to add in each frame
    step_size = 5

    # Get the segment of the attractor to plot
    i_start = max(0, frame * step_size - 1)
    i_end = (frame + 1) * step_size
    if i_end > len(x):
        i_end = len(x)

    #if len(lines) >= 10:
    #    lines.pop(0)

    # Skip if we've already plotted all points
    if i_start >= len(x):
        return [ax]

    # Change the line color gradually through the HSV spectrum
    hue = (frame // 3) % 360 / 360  # One full cycle every 1080 frames (360*3)
    color = cm.hsv(hue)  # Get the color from the HSV colormap

    # Plot the segment with the new color
    #if len(lines) >= 200:
    #    lines[idx].set_data_3d(x[i_start:i_end], y[i_start:i_end], z[i_start:i_end])
    #    lines[idx].set(color=color, lw=1)
    #    idx += 1
    #    if idx >= len(lines):
    #        idx = 0
    #else:
    #for i in range(i_start, i_end):
    #    segments.append((x[i], y[i], z[i]))
    #    colors.append(color)
    # build line
    sges = list(zip(x[i_start:i_end], y[i_start:i_end], z[i_start:i_end]))
    if len(sges) != 0:
        if len(segments) >= 500:
            segments[idx] = sges
            colors[idx] = color
            idx += 1
            if idx >= len(segments):
                idx = 0
        else:
            segments.append(sges)
            colors.append(color)
        coll.set(segments=segments, colors=colors)
    #line, = ax.plot(x[i_start:i_end], y[i_start:i_end], z[i_start:i_end], color=color, lw=1)
    #lines.append(line)  # Store the new segment

    # Rotate the view around the z-axis
    rot = (rot + 1) % 360
    ax.view_init(elev=30, azim=rot)
    return [ax]
# Create the animation (with blitting)
ani = FuncAnimation(fig, update, frames=len(t_eval)//10, init_func=init, interval=30, blit=True)

# Show the plot
plt.show()