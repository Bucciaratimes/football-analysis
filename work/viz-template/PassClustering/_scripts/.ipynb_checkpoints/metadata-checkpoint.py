# columns required for the input df
start_x_key = 'x'
start_y_key = 'y'
end_x_key = 'endX'
end_y_key = 'endY'
team_key = 'teamName'
opp_key = 'opponent'


# additional columns added in processing
start_goal_dist_key = 'start_distance_to_goal'
end_goal_dist_key = 'end_distance_to_goal'
length_key = 'length'
advanced_percent_key = 'advanced_%'
angle_key = 'angle'
cluster_key = 'cluster'


# clustering will be run based on these features
clustering_features = [
    start_x_key,
    start_y_key,
    end_x_key,
    end_y_key,
    angle_key
]


# clustering parameters
c_metric = 'euclidean'
c_min_samples = 5
c_xi = 0.1


# other stuff
field_length = 120
field_width = 80
progressive_min_dist_percent = 0.25
n_top_clusters_to_plot = 10


#plotting
cluster_colors = ['orange', 'dodgerblue', 'lightpink', 'goldenrod', 'magenta', 'white', 'aqua', 'lime', 'tomato', 'yellow', 'tan', 'mediumspringgreen', 'hotpink']
font_color = '#cdcdcd'

class PassArrow():
    opacity = 0.05
    width = 0.25
    zorder = 10

class AvgArrow():
    opacity = 0.4
    width = 0.25
    zorder = 11

ax_title_txts = {
    team_key: '',
    opp_key: ' - Allowed'
}

pitchColor="#ededed"
pitchColor="#131313" #black
pitchLineColor = '#495E62'
pitchLineColor = '#ededed' #black
textColor = "#efefef"
