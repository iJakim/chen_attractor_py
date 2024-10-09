import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

# derivative calculation
def deriv(t, st):
    x, y, z = st
    dxdt = 400 * (y - x)
    dydt = -120 * x - 10 * x * z + 280 * y
    dzdt = 10 * x * y - 30 * z
    return [dxdt, dydt, dzdt]

# initial conditions
init = [-5, -10, 20] # init coordinates
t_span = (0, 10)  # integration time span
t_eval = np.linspace(t_span[0], t_span[1], 10000)  # time eval

# solve
sol = solve_ivp(deriv, t_span, init, t_eval=t_eval)
x = sol.y[0]
y = sol.y[1]
z = sol.y[2]

# 3d plot init
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# plot limit
ax.set_xlim(np.min(x), np.max(x))
ax.set_ylim(np.min(y), np.max(y))
ax.set_zlim(np.min(z), np.max(z))

# line init
line, = ax.plot([], [], [], lw=1)

# animation function init
def init():
    line.set_data([], [])
    line.set_3d_properties([])
    return line,

# animation function update
def update(frame):
    line.set_data(x[:frame], y[:frame])
    line.set_3d_properties(z[:frame])
    return line,

# run animation
ani = FuncAnimation(fig, update, frames=len(t_eval), init_func=init, blit=True, interval=1)
plt.show()