from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

ollie_dictionary = {'thunderstorm': "It's stormin",
                    'drizzle': "It's drizzlin",
                    'rain': "It's rainin",
                    "shower": "It's rainin",
                    'snow': "It's snowin",
                    'sleet': "It's sleetin",
                    'clear sky': 'nothin',
                    'few clouds': "I see a cloud",
                    'scattered clouds': "There's clouds",
                    'broken clouds': "There's clouds",
                    'overcast clouds': "There's clouds",
                    'hail': "It's hailin",
                    'hot': "It's hot",
                    'haze': "It's hot",
                    'calm': 'nothin',
                    'breeze': "There's wind",
                    'gale': "There's wind",
                    'storm': "It's stormin",
                    'cold': "It's cold",
                    'hurricane': "There's a hurricane",
                    'tornado': "There's a tornado",
                    'fog': "I can't see"}


def ollify_text(text):
    try:
        return ollie_dictionary[text]
    except KeyError:
        for string in text.split():
            if string in ollie_dictionary.keys():
                return ollie_dictionary[string]

def draw_text(text, out_file, _font='extra\\impact.ttf', file='extra\\anchorman.jpg'):

    im = Image.open(file)
    point_size = 40
    fill_color = "white"
    shadow_color = "black"
    thickness = 1

    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype(_font, point_size)

    w, h = draw.textsize(text, font)
    width, height = im.size

    # text dimensions
    dimensions = ((width - w) / 2, (height - h) / 2)

    # outline dimensions
    tr_dimensions = (((width - w) / 2) + thickness, ((height - h) / 2) + thickness)
    tl_dimensions = (((width - w) / 2) - thickness, ((height - h) / 2) + thickness)
    br_dimensions = (((width - w) / 2) - thickness, ((height - h) / 2) - thickness)
    bl_dimensions = (((width - w) / 2) + thickness, ((height - h) / 2) - thickness)

    # create outline
    draw.text(tr_dimensions, text, font=font, fill=shadow_color)
    draw.text(tl_dimensions, text, font=font, fill=shadow_color)
    draw.text(br_dimensions, text, font=font, fill=shadow_color)
    draw.text(bl_dimensions, text, font=font, fill=shadow_color)

    # now draw the text over it
    draw.text(dimensions, text, font=font, fill=fill_color)
    im.save(out_file)

