import numpy
from scipy import signal
import filtertools

# The point of using Gaussian derivative filters is that this computes a
# smoothing of the image, to a scale defined by the size of the filter, and the
# derivatives at the same time. The derivatives are less noisy than if computed
# with a simple difference filter on the original image.

# First add the corner response function to a file harris.py which will make
# use of the Gaussian derivatives above.


def compute_harris_response(image):
    """ compute the Harris corner detector response function 
        for each pixel in the image"""

    #derivatives
    imx, imy = filtertools.gauss_derivatives(image, 3)

    #kernel for blurring
    gauss = filtertools.gauss_kernel(3)

    #compute components of the structure tensor
    Wxx = signal.convolve(imx*imx, gauss, mode='same')
    Wxy = signal.convolve(imx*imy, gauss, mode='same')
    Wyy = signal.convolve(imy*imy, gauss, mode='same')

    #determinant and trace
    Wdet = Wxx*Wyy - Wxy**2
    Wtr = Wxx + Wyy

    if numpy.count_nonzero(Wtr) == 0:
        return
    print Wtr.shape
    print numpy.count_nonzero(Wtr)

    return Wdet / Wtr


# This gives an image with each pixel containing the value of the Harris
# response function. Now it is just a matter of picking out the information
# needed from this image. Picking all values above a threshold with the
# additional constraint that corners must be separated with a minimum distance
# is an approach that often gives good results. To do this, take all candidate
# pixels, sort them in descending order of corner response values and mark off
# regions too close to positions already marked as corners. Add this function
# to harris.py.


def get_harris_points(harrisim, min_distance=10, threshold=0.1):
    """ return corners from a Harris response image
        min_distance is the minimum nbr of pixels separating 
        corners and image boundary"""

    #find top corner candidates above a threshold
    corner_threshold = max(harrisim.ravel()) * threshold
    harrisim_t = (harrisim > corner_threshold) * 1

    #get coordinates of candidates
    candidates = harrisim_t.nonzero()
    coords = [ (candidates[0][c],candidates[1][c]) for c in range(len(candidates[0]))]
    #...and their values
    candidate_values = [harrisim[c[0]][c[1]] for c in coords]

    #sort candidates
    index = numpy.argsort(candidate_values)

    #store allowed point locations in array
    allowed_locations = numpy.zeros(harrisim.shape)
    allowed_locations[min_distance:-min_distance,min_distance:-min_distance] = 1

    #select the best points taking min_distance into account
    filtered_coords = []
    for i in index:
        if allowed_locations[coords[i][0]][coords[i][1]] == 1:
            filtered_coords.append(coords[i])
            allowed_locations[(coords[i][0]-min_distance):(coords[i][0]+min_distance),(coords[i][1]-min_distance):(coords[i][1]+min_distance)] = 0

    return filtered_coords


# Now you have all you need to detect corner points in images. To make it
# easier to show the corner points in the image you can add a plotting function
# using matplotlib (PyLab) as follows.


def save_harris_points(image, filtered_coords):
    """ plots corners found in image"""
    import pylab

    pylab.figure()
    pylab.gray()
    pylab.imshow(image)
    pylab.plot([p[1] for p in filtered_coords],[p[0] for p in filtered_coords],'*')
    pylab.axis('off')
    pylab.savefig('shown_corners.png')

def plot_harris_points(image, filtered_coords):
    """ plots corners found in image"""
    import pylab

    pylab.figure()
    pylab.gray()
    pylab.imshow(image)
    pylab.plot([p[1] for p in filtered_coords],[p[0] for p in filtered_coords],'*')
    pylab.axis('off')
    pylab.show()
