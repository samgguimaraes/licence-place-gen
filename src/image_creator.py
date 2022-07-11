from PIL import Image, ImageDraw, ImageFont
import numpy as np

def draw_rectangle(draw: ImageDraw,
                   centre: list[float],
                   size: list[float],
                   roundness: int,
                   colour: str):
    '''Draws a rectangle in the canvas. Centre and size parameter relative to the canvas size
    '''
    img = draw.im
    centre_abs = np.array([img.size[0] * centre[0], img.size[1] * centre[1]])
    size_abs = np.array([img.size[0] * size[0], img.size[1] * size[1]])/2
    corners = list((centre_abs - size_abs).astype(int)) + list((centre_abs + size_abs).astype(int))
    roundness_abs = round(max(size_abs) * roundness / 100)
    
    draw.rounded_rectangle(corners,
                            radius=roundness_abs,
                            fill=colour,
                            width=0)


def draw_concenctric_rectangles(draw: ImageDraw,
                                centre: list[float],
                                base_size: list[float],
                                roundness: int,
                                rects: list):
    '''Draws concentric rectangles with constant distance between the borders
    '''
    img = draw.im
    for rect in rects:
        border = (1 - rect[0]) * (img.size[0] * base_size[0])
        draw_rectangle(draw,
                       centre,
                       [rect[0] * base_size[0], base_size[1] - border/img.size[1]],
                       roundness,
                       rect[1])


def draw_text(draw: ImageDraw,
              text: str,
              centre: list[float],
              height: float,
              font_path: str,
              colour: str):
    '''Print a text with the given font and relative height to the image
    '''
    if not text:
        return
    
    font_size100 = ImageFont.truetype(font_path, 100).getsize(text)
    
    img = draw.im
    centre_abs = [img.size[0] * centre[0], img.size[1] * centre[1]]
    font_size = round(100 * height * img.size[1] / font_size100[1])
    text_size = ImageFont.truetype(font_path, font_size).getsize(text)
    
    font = ImageFont.truetype(font_path, font_size)
    
    draw.text((centre_abs[0] - text_size[0]/2, centre_abs[1] - text_size[1]/2), text, fill=colour, font=font)


def stamp_image(img: Image,
                centre: list[float],
                size: list[float],
                image_path: str = None,
                im: Image = None):
    '''Stamp an image into the target image
        If no image is provided the image_path is used to read it
    '''
    if im is None and image_path is None:
        return
    
    if im is None and image_path is not None:
        im = Image.open(image_path)
    
    size_abs = [round(size[0] * img.size[0]), round(size[1] * img.size[1])]
    
    im = im.resize(size_abs)
    
    half_size = (np.array(im.size)/2).astype(int)
    corner = (np.array(centre) * img.size - half_size).astype(int)
    
    mask = None
    if 'A' in im.getbands():
        mask = im
    img.paste(im, np.array(im.getbbox()).astype(int) + list(corner) * 2, mask=mask)