from mplsoccer import FontManager
from matplotlib.colors import LinearSegmentedColormap

whiteTheme = {
    "figBackColor":"#F8F8FF",
    "axBackColor":"#F8F8FF",
    "textColor": "#131313",
    "lineColor" : "#495E62",
    "homeColor":'#B94B5F',
    "awayColor":'#13A5D6',
}

blackTheme = {
    "figBackColor":"#131313",
    "axBackColor":"#131313",
    "textColor": "#f8f8f8",
    "homeColor":'#B94B5F',
    "awayColor":'#13A5D6'
}

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

#Loading Some Fonts
smooch = "https://github.com/googlefonts/smooch/blob/master/fonts/ttf/Smooch-Regular.ttf?raw=true"
spaceMono_italy = 'https://github.com/googlefonts/spacemono/blob/main/fonts/SpaceMono-Italic.ttf?raw=true'
spaceMono_bold = 'https://github.com/googlefonts/spacemono/blob/main/fonts/SpaceMono-BoldItalic.ttf?raw=true'
spaceMono_dance = "https://github.com/googlefonts/moondance/tree/master/fonts/ttf?raw=true"
# smoochFont = FontManager(smooch)
monoIFont = FontManager(spaceMono_italy)
monoBFont = FontManager(spaceMono_bold)
# monoDFont = FontManager(spaceMono_dance)

pitch_color = '#131313'
text_color = '#ffffff'
oneColor = '#B94B5F'
theOtherColor = '#4A5EB8'

cmapA = LinearSegmentedColormap.from_list("my_cmap", [pitch_color, oneColor], N=100)
cmapB = LinearSegmentedColormap.from_list("my_cmap", [pitch_color, theOtherColor], N=100)
myFont = monoIFont
