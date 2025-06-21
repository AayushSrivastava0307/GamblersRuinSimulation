import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import tkinter as tk
from tkinter import messagebox

def theoretical_bankruptcy_probability(i, c, p):
    """
    Computes the theoretical probability of the gambler going bankrupt.
    """
    q = 1 - p
    if p == 0.5:
        return c / (i + c)
    return (1-(1 - (q/ p) ** i) / (1 - (q / p) ** (i + c)))

def simulate_gamblers_ruin(i, c, p, max_steps=1000):
    """
    Simulates the gambler's ruin problem and returns the trajectory and outcome.
    """
    stake = i
    trajectory = [stake]

    for _ in range(max_steps):
        if stake == 0 or stake == i + c:
            break  # Stop if the gambler is ruined or succeeds
        if np.random.rand() < p:
            stake += 1  # Gambler wins
        else:
            stake -= 1  # Gambler loses
        trajectory.append(stake)

    return trajectory, "Ruin" if stake == 0 else "Success"

def update(frame, trajectories, lines, ax):
    """
    Update function for the animation. Updates the plot for each frame.
    """
    all_finished = True
    for line, trajectory in zip(lines, trajectories):
        if frame < len(trajectory):
            line.set_data(range(frame + 1), trajectory[:frame + 1])
            if trajectory[frame] != 0 and trajectory[frame] != i + c:
                all_finished = False
    
    if all_finished:
        ax.text(0.5, 0.85, "Simulation Complete", 
                horizontalalignment='center', verticalalignment='center', 
                transform=ax.transAxes, fontsize=14, bbox=dict(facecolor='white', alpha=0.8))
        root = tk.Tk()
        root.withdraw()
        if messagebox.showinfo("Simulation Complete", "All simulations have finished. Click Close to exit."):
            plt.close()
    return lines

def animate_gamblers_ruin(i, c, p, num_simulations=5, max_steps=1000):
    """
    Animates multiple simulations of the gambler's ruin problem and computes the probability of bankruptcy.
    """
    trajectories, outcomes = zip(*[simulate_gamblers_ruin(i, c, p, max_steps) for _ in range(num_simulations)])
    ruin_count = outcomes.count("Ruin")
    bankruptcy_probability = ruin_count / num_simulations
    theoretical_probability = theoretical_bankruptcy_probability(i, c, p)

    # Set up the plot
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.canvas.manager.set_window_title("Gambler's Ruin Simulation")
    ax.set_xlim(0, max_steps)
    ax.set_ylim(0, i + c + 10)
    ax.set_xlabel('Number of Plays')
    ax.set_ylabel('Gambler\'s Stake')
    ax.set_title(f'Gambler\'s Ruin Problem (p={p}, i={i}, c={c})')
    ax.axhline(y=i + c, color='green', linestyle='--', label='Success Threshold (i + c)')
    ax.axhline(y=0, color='red', linestyle='--', label='Ruin Threshold (0)')
    ax.legend()
    ax.grid(True)

    ax.text(0.5, 0.95, f'Empirical Probability of Bankruptcy: {bankruptcy_probability:.2f}\nTheoretical Probability: {theoretical_probability:.2f}',
            horizontalalignment='center', verticalalignment='center',
            transform=ax.transAxes, fontsize=12, bbox=dict(facecolor='white', alpha=0.8))

    lines = [ax.plot([], [], label=f'Simulation {j + 1}')[0] for j in range(num_simulations)]

    ani = FuncAnimation(
        fig, update, frames=max_steps,
        fargs=(trajectories, lines, ax),
        interval=50, blit=True
    )

    plt.show()

def get_user_input():
    """
    Prompts the user for input parameters.
    """
    i = int(input("Enter the gambler's initial stake (i): "))
    c = int(input("Enter the casino's initial stake (c): "))
    p = float(input("Enter the probability of the gambler winning a single game (p): "))
    num_simulations = int(input("Enter the number of simulations: "))
    max_steps = int(input("Enter the maximum number of steps: "))
    return i, c, p, num_simulations, max_steps

if __name__ == "__main__":
    print("Gambler's Ruin Problem Simulation")
    i, c, p, num_simulations, max_steps = get_user_input()
    animate_gamblers_ruin(i, c, p, num_simulations, max_steps)
