import numpy as np
import pandas as pd
from matplotlib import colormaps
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.colors import ListedColormap

from mplsoccer import (VerticalPitch, Pitch, create_transparent_cmap,
                       FontManager, arrowhead_marker, Sbopen)

df_shots = pd.read_csv('wsl1.csv')

df_goals = df_shots[df_shots.isGoal == True].copy()
df_non_goal_shots = df_shots[df_shots.isGoal != True].copy()

pitch = VerticalPitch(pad_bottom=0.5,  # pitch extends slightly below halfway line
                      half=True,  # half of a pitch
                      pitch_type='opta',
                      goal_type='box',
                      goal_alpha=0.8)  # control the goal transparency
fig, ax = pitch.draw(figsize=(12, 10))

# plot non-goal shots with hatch
sc1 = pitch.scatter(df_non_goal_shots.x, df_non_goal_shots.y,
                    s=(df_non_goal_shots.xG * 1000) + 100,
                    edgecolors='#606060',  # give the markers a charcoal border
                    c='#FF0000',  # no facecolor for the markers
                    #hatch='///',  # the all important hatch (triple diagonal lines)
                    # for other markers types see: https://matplotlib.org/api/markers_api.html
                    marker='o',
                    ax=ax)

# plot goal shots with a color
sc2 = pitch.scatter(df_goals.x, df_goals.y,
                    s=(df_goals.xG * 1000) + 100,
                    edgecolors='#606060',  # give the markers a charcoal border
                    c='#00FF00',  # color for scatter in hex format
                    # for other markers types see: https://matplotlib.org/api/markers_api.html
                    marker='o',
                    ax=ax)

txt = ax.text(x=40, y=80, s='Predicted xG Shots - WSL',
              size=30,
              color=pitch.line_color,
              va='center', ha='center')

# Add title
fig.suptitle('WSL Shots 2023-24', fontsize=20, fontweight='bold')

# Add custom legend
legend_elements = [
    Line2D([0], [0], marker='o', color='w', label='Goals', markerfacecolor='#00FF00', markersize=10),
    Line2D([0], [0], marker='o', color='w', label='Not Goals', markerfacecolor='#FF0000', markersize=10),
    Line2D([0], [0], marker='o', color='w', label='Size ~ xG', markerfacecolor='#808080', markersize=15)
]
ax.legend(handles=legend_elements, loc='lower right', title='Legend')

plt.show()

