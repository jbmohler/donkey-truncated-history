from numpy import array
from PIL import Image
import harris

# Try running the following commands on an example image:

im = Image.open('sudoku_image_02.png').convert("L")
#im = im.rotate(5)#, expand=True)
im = array(im)
harrisim = harris.compute_harris_response(im)
filtered_coords = harris.get_harris_points(harrisim, 6)
harris.save_harris_points(im, filtered_coords)
