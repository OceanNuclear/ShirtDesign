from numpy import array as ary; from numpy import log as ln
from numpy import cos, sin, pi, sqrt, exp, arccos
import numpy as np
from matplotlib.pyplot import colormaps # gives the names of all of them
from matplotlib.cm import get_cmap # get the actual palettes
import matplotlib.pyplot as plt
import os
from PIL import Image

def convert_color(image_array, source_color, target_color):
    """
    Converts a numpy array (3D, first two dimension denotes the xy (left-to-right, top-to-bottom) location of the pixel)
    """
    mask = (image_array==source_color).all(axis=2)
    image_array[mask] = target_color
    return image_array

def apply_transparency(image_array):
    """
    Take the brightness (i.e. mean RGB value) of the pixel colour, and use it as the transparency.
    """
    image_array[:,:,3] = np.mean(image_array[:,:,:3], axis=2)
    return image_array

black = ary([0,0,0,255])
white = ary([255,255,255,255])
transp= ary([0,0,0,0])

def pad_to_size(image_array, dimension, pad_color=transp):
    """
    Centre the image_array and pad the pad_color around it into a square
    """
    x_excess = dimension[1]-image_array.shape[1]
    y_excess = dimension[0]-image_array.shape[0]
    canvas = np.full((*dimension, 4), pad_color) # make blank canvas
    canvas[y_excess//2:image_array.shape[0]+y_excess//2,
            x_excess//2:image_array.shape[1]+x_excess//2] = image_array# draw on canvas
    return canvas

def turn_white_to_color(image_array, target_color):
    """
    Takes in a png with RGBA format, keep the transparency of each pixel the same,
    Next, rescale the "white" (FF, FF, FF) into the target_color
    This function works best when the image is only black and white, where all elements that you want to highlight are white.
    """
    decimal_array = ary(image_array, dtype='float')
    decimal_array[:,:,0] *= target_color[0]
    decimal_array[:,:,1] *= target_color[1]
    decimal_array[:,:,2] *= target_color[2]
    return ary(decimal_array, dtype='int64')

def get_mask(dimensions, m1, c1, m2, c2):
    pixel_loc = np.meshgrid(np.arange(dimensions[1]), np.arange(dimensions[0]))
    bool_mask = np.logical_and(pixel_loc[1]<(m1*pixel_loc[0]+c1), pixel_loc[1]>=(m2*pixel_loc[0]+c2))
    return bool_mask

# Color maps considered:
cubehelix = get_cmap('cubehelix')
viridis = get_cmap('viridis')
plasma = get_cmap('plasma')
cividis = get_cmap('cividis')

top_color = [int(i*255) for i in plasma(0.8)]
mid_color = [int(i*255) for i in viridis(0.4)]
bot_color = [int(i*255) for i in cividis(0.0)]
bg_color = [int(i*255) for i in cividis(0.3)]

if __name__=='__main__':
    side_length = 400
    dimensions = [side_length, side_length]
    if not os.path.exists('square_letter_P.png'):
        raw = Image.open("parkourHelvetica.PNG")
        img = 255-ary(raw.crop([0,0,288,375])) # crop out the letter p, AND invert the color
        trans_p = apply_transparency(img)
        square_p = pad_to_size(trans_p, dimensions)
        letter_p = Image.fromarray(ary(square_p, dtype='uint8'))
        letter_p.save('square_letter_P.png')
    else:
        letter_p = Image.open('square_letter_P.png')

    # create copies of the letter P as different layers, and then color them differently.
    p_ary = ary(letter_p, dtype='int64')
    top_layer = turn_white_to_color(p_ary, top_color)
    mid_layer = turn_white_to_color(p_ary, mid_color)
    bot_layer = turn_white_to_color(p_ary, bot_color)

    white_image = np.full([*dimensions, 4], white)
    transp_canvas = np.full([*dimensions, 4], transp)

    # define where each layer should be visible
    mask = get_mask(dimensions, 0.4, 20, 0.0, 0)
    transp_canvas[mask] = top_layer[mask]
    mask = get_mask(dimensions, 0.4, 29, 0.4, 23)
    transp_canvas[mask] = white_image[mask]
    mask = get_mask(dimensions, 0.4, 150, 0.4, 32)
    transp_canvas[mask] = mid_layer[mask]
    mask = get_mask(dimensions, 0.4, 159, 0.4, 153)
    transp_canvas[mask] = white_image[mask]
    mask = get_mask(dimensions, 0, 400, 0.4, 162)
    transp_canvas[mask] = bot_layer[mask]
    final_pic = transp_canvas
    # final_pic = convert_color(transp_canvas, transp, bg_color)

    icon = Image.fromarray(ary(final_pic, dtype='uint8'))
    icon.show()
    icon.save('icon.png')