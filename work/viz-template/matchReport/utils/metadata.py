import matplotlib.pyplot as plt

# Colors
pitch_background_color = 'w'
text_color = '#000000'
pitch_line_color = '#000000'

# home_color = '#1565c0'
# away_color = '#c62828'
home_color = '#B94B5F'
away_color = '#4A5EB8'

bar_stats = ['PPDA', 'Passes', 'Shots On Target', 'Shots', 'Expected Goals', 'Goals']
bar_CLstats = ['PPDA', 'Passes', 'Shots On Target', 'Shots', 'Goals']


def add_ax_title(ax, title):
    # Add title
    ax_title = ax.set_title(
                title,
                color=text_color,
                alpha=0.8,
                weight=650,
                fontsize=12,
                pad=8,
                zorder=-2,
                bbox=dict(
                    facecolor=pitch_background_color,
                    edgecolor=pitch_line_color,
                    linewidth=1.5,
                    alpha=1,
                    boxstyle='Sawtooth, pad=0.45',
                    zorder=1
                ))
    return ax_title

def add_arrow(ax, team):
    if team == 'home':
        ax_arrow = ax.arrow(x=25, y=50, dx=50, dy=0, length_includes_head=True,
                            width=5, head_length=8.5,
                            facecolor=(1, 1, 1, 0.1), edgecolor=(0,0,0,1), zorder=2)
    if team == 'away':
        ax_arrow = ax.arrow(x=25, y=50, dx=50, dy=0, length_includes_head=True,
                            width=5, head_length=8.5,
                            facecolor=(1, 1, 1, 0.1), edgecolor=(0,0,0,1), zorder=2)
        
    return ax_arrow