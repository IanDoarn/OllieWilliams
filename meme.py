from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

def draw_text(text, out_file, font='impact.ttf', file='ollie-williams.jpg'):

    im = Image.open(file)
    point_size = 50
    fill_color = "white"
    shadow_color = "black"

    width, height = im.size
    x = width / point_size
    y = 12

    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype(font, point_size)

    # thin border
    draw.text((x-1, y), text, font=font, fill=shadow_color)
    draw.text((x+1, y), text, font=font, fill=shadow_color)
    draw.text((x, y-1), text, font=font, fill=shadow_color)
    draw.text((x, y+1), text, font=font, fill=shadow_color)

    # thicker border
    draw.text((x-1, y-1), text, font=font, fill=shadow_color)
    draw.text((x+1, y-1), text, font=font, fill=shadow_color)
    draw.text((x-1, y+1), text, font=font, fill=shadow_color)
    draw.text((x+1, y+1), text, font=font, fill=shadow_color)

    # now draw the text over it
    draw.text((x, y), text, font=font, fill=fill_color)

    im.save(out_file)

draw_text('IT GONE RAIN', 'forecast.jpg')