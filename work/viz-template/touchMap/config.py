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
lineColor = '#ededed' #black

homeColor = '#B94B5F'
awayColor = '#4A5EB8'

arrow_shift = 1.5 ##Units by which the arrow moves from its original position
shrink_val = 1 ##Units by which the arrow is shortened from the end_points
MAXLINEWIDTH = 10
MAXMARKERSIZE = 1000
COLORCODE = '#87CEEB'
MINTRANSPARENCY = 0.3


x = 'x_median'
end_x = 'x_median_end'
y = 'y_median'
end_y = 'y_median_end'

#Loading Some Fonts
smooch = "https://github.com/googlefonts/smooch/blob/master/fonts/ttf/Smooch-Regular.ttf?raw=true"
spaceMono_italy = 'https://github.com/googlefonts/spacemono/blob/main/fonts/SpaceMono-Italic.ttf?raw=true'
spaceMono_bold = 'https://github.com/googlefonts/spacemono/blob/main/fonts/SpaceMono-BoldItalic.ttf?raw=true'
spaceMono_dance = "https://github.com/googlefonts/moondance/tree/master/fonts/ttf?raw=true"
abel_regular = 'https://github.com/google/fonts/blob/main/ofl/abel/Abel-Regular.ttf?raw=true'

from matplotlib.colors import LinearSegmentedColormap
from mplsoccer import FontManager

# smoochFont = FontManager(smooch)
monoIFont = FontManager(spaceMono_italy)
monoBFont = FontManager(spaceMono_bold)
monoDFont = FontManager(spaceMono_dance)
# abel_regular = FontManager(abel_regular)

homeColor = "#FDC526"
awayColor = "#c77dff"

cmapA = LinearSegmentedColormap.from_list("my_cmap", ["#f8f8f8", homeColor], N=100)
cmapB = LinearSegmentedColormap.from_list("my_cmap", ["#131313", homeColor], N=100)
myFont = monoIFont
