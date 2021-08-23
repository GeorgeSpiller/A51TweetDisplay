from ImageManager import createTweetImage
from PIL import Image, ImageDraw, ImageFont

def get_text_dimensions(text_string, font):
    # https://stackoverflow.com/a/46220683/9263761
    ascent, descent = font.getmetrics()

    text_width = font.getmask(text_string).getbbox()[2]
    text_height = font.getmask(text_string).getbbox()[3] + descent

    return (text_width, text_height)

# combind images into 1920x1080 image base

img = Image.new('RGB', (1920,1080), color='white')
draw_interf = ImageDraw.Draw(img)

# draw A51 Text onto image
x=0
y=0
FONT_SIZE = 40
font = ImageFont.load_default()
FONT_TEXT =  ImageFont.truetype("D:\\Users\\geosp\Documents\\Code\\PY\\Projects\\TwitterScreenshot\\resources\\PALADINS.TTF",FONT_SIZE, encoding="utf-8") 
#ImageFont.truetype("arial.ttf", FONT_SIZE, encoding="utf-8")
COLOR_TEXT_LIGHT = (220, 220, 220)  # 192
COLOR_TEXT_DARK = (192, 192, 192)
LINE_MARGIN = 15
TEXT_SEG1 = "oopie "
TEXT_SEG2 = "doopie "
TEXT_SEG1_DIMENTIONS = get_text_dimensions(TEXT_SEG1, FONT_TEXT)[0]
TEXT_SEG2_DIMENTIONS = get_text_dimensions(TEXT_SEG2, FONT_TEXT)[0]


currentFill = COLOR_TEXT_LIGHT
for itter_y in range(20):
    # toggle fill each y line
    if (y % 2 == 0):
        currentFill = COLOR_TEXT_DARK
        x = 0
    else:
        currentFill = COLOR_TEXT_LIGHT
        x = -150

    for __ in range(8):
        # draw a line of text on the x
        draw_interf.text((x, y), TEXT_SEG1, font=FONT_TEXT, fill=currentFill)
        x += TEXT_SEG1_DIMENTIONS
        draw_interf.text((x, y), TEXT_SEG2, font=FONT_TEXT, fill=currentFill)
        x += TEXT_SEG2_DIMENTIONS

    y += FONT_SIZE + LINE_MARGIN
    x = 0
    

img.save('tmp-BK.png')
