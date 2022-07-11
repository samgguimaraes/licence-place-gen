from PIL import Image, ImageDraw
import yaml
import time
import sys
import os

import image_creator
import descriptor_parser


def build_from_descriptor(description: list):
    '''Generate an image from the description
    '''
    img = Image.new('RGBA', description['size'], color='#FFFFFF00')
    draw = ImageDraw.Draw(img)
    
    for component in description['components']:
        comp_name = list(component.keys())[0]
        content = component[comp_name]
        if comp_name == 'concenctric_rectangles':
            image_creator.draw_concenctric_rectangles(draw,
                                        content['center'],
                                        content['size'],
                                        content['roundness'],
                                        [list(d.items())[0] for d in content['components']])
        elif comp_name == 'text':
            image_creator.draw_text(draw,
                      content['content'],
                      content['center'],
                      content['size'],
                      content['font'],
                      content['color'])
        elif comp_name == 'rectangle':
            image_creator.draw_rectangle(draw,
                           content['center'],
                           content['size'],
                           content['roundness'],
                           content['color'])
        elif comp_name == 'image':
            image_creator.stamp_image(img,
                        content['center'],
                        content['size'],
                        content['path'])

    return img


def gen_plates(descriptor_path: str):
    '''Reads the descriptor yaml and generated and save the images
    '''
    with open(descriptor_path, encoding='utf8') as f:
        desc = yaml.load(f, Loader=yaml.FullLoader)
    
    generated = set()
    config = desc['config']
    total = config.get('generate_n', 1)
    output_dir = config.get('output_dir', '.')
    
    for _ in range(total):
        licence = None
        while not licence or licence in generated:
            plate_desc, keys = descriptor_parser.get_values(desc['plates'])
            licence = keys['licence_number']
        img = build_from_descriptor(plate_desc)
        img.save(os.path.join(output_dir, f'{int(time.time())}_{licence}.png'))

if __name__ == '__main__':
    if len(sys.argv) > 1:
        gen_plates(sys.argv[1])