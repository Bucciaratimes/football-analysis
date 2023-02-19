from mplsoccer import FontManager
from matplotlib.colors import LinearSegmentedColormap

pitchColor="#ededed"
pitchColor="#131313" #black
pitchLineColor = '#495E62'
pitchLineColor = '#ededed' #black
textColor = "#efefef"
# discribeColor = "#6D6065"
discribeColor = "#ededed" #black
# playerNameColor = "#1A1F21"
playerNameColor = "#efefef" #_black
# lineColor = '#3D3337'

# homeColor = '#B94B5F'
# awayColor = "#0077FF" #'#4A5EB8'


x = 'x_median'
end_x = 'x_median_end'
y = 'y_median'
end_y = 'y_median_end'

arrow_shift = 1.5 ##Units by which the arrow moves from its original position
shrink_val = 1 ##Units by which the arrow is shortened from the end_points
MAXLINEWIDTH = 10
MAXMARKERSIZE = 1000
COLORCODE = '#87CEEB'
MINTRANSPARENCY = 0.3

#Loading Some Fonts
spaceMono_bold = 'https://github.com/googlefonts/spacemono/blob/main/fonts/SpaceMono-BoldItalic.ttf?raw=true'
monoBFont = FontManager(spaceMono_bold)

homeColor = "#ee9b00"
awayColor = "#c77dff"

homeColor = "#fb8ee0"
awayColor = "#b4e1ff"

cmapA = LinearSegmentedColormap.from_list("my_cmap", ["#f8f8f8", homeColor], N=100)
cmapB = LinearSegmentedColormap.from_list("my_cmap", ["#f8f8f8", awayColor], N=100)
