import colorsys

N=13
HSV_tuples = [(x*1.0/N, 1.0, 1.0) for x in range(N)]
RGB_tuples = ['#%02x%02x%02x' % (int(x[0]*255), int(x[1]*255), int(x[2]*255)) for x in list(map(lambda x: colorsys.hsv_to_rgb(*x), HSV_tuples))]
RGB_tuples


def hue_range(n):
    return (i / n for i in range(n))

def hsv(hue=1.0, saturation=1.0, value=1.0):
    return hue, saturation, value

def hsv2rgb(hsv):
    r, g, b = colorsys.hsv_to_rgb(*hsv)
    return int(r * 255), int(g * 255), int(b * 255)

def rgb_codes(n):
    return ("#%02x%02x%02x" % hsv2rgb(hsv) for hsv in map(hsv, hue_range(n)))

def main():
    N = 24
    print(*rgb_codes(N))

if __name__ == '__main__':
    main()
