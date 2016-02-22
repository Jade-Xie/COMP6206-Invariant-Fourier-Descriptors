from __future__ import division

# External libraries.
import copy
import cv2
import numpy as np
import pprint

# Image directory.
img_dir	= '../images/'

# Images for testing.
gumby	= 'gumby.jpg'
penguin	= 'penguin.jpg'
star	= 'star.jpg'

img_orig		= cv2.imread(img_dir + star, 0)

# Converts an RGB image into greyscale.
# Then converts the greyscale image into a binary one, and returns the threshold image.
def clean(image, src_rgb):
	img_clone	= fresh_image()

	if src_rgb:
		img_clone	= cv2.cvtColor(img_clone, cv2.COLOR_BGR2GRAY)

	ret, threshold	= cv2.threshold(img_clone, 127, 255, cv2.THRESH_BINARY)

	return threshold

# Finds and returns the contours.
# TODO: Expand to other parameters:
# Most exhaustive parameters fed in, change later if possible - specifically CHAIN_APPROX_NONE to CHAIN_APPROX_SIMPLE.
def find_contours(image):
	img_clone	= fresh_image(image)

	contours, hierarchy	= cv2.findContours(img_clone, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

	return contours

# Basic image display for a single image.
# Closes all images after use.
def display_image(image, title):
	cv2.imshow(title, image)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

# Returns a clone of an image, or the original image if no argument passed.
def fresh_image(image = img_orig):
	return copy.deepcopy(image)

threshold_img	= clean(img_orig, False)
contours		= find_contours(threshold_img)

# BELOW HERE LIES SCARY TESTING.

# [0] strips out the array we care about.
# Advanced indexing in numpy: [:, 0]
# : gets ALL 'rows'.
# 0 grabs the first element in each 'row'.
contour			= contours[0][:, 0]

# Creates an empty np struct.
# shape gives (len, 1, 2), i.e. an array of pairs length len.
# [:-1] gives an array of elements length len.
contour_complex			= np.empty(contour.shape[:-1], dtype = complex)
contour_complex.real	= contour[:, 0]
contour_complex.imag	= contour[:, 1]

fourier_val		= np.fft.fft(contour_complex)
fourier_freq	= np.fft.fftfreq(len(contour_complex))
#fourier_result	= np.fft.fftfreq(len(contour_complex))
#print fourier_result

frequencies		= []
for index, val in enumerate(fourier_freq):
	frequencies.append([index, val])

frequencies.sort(key = lambda tuple: abs(tuple[1]))

percentage	= 10
to_get		= int(len(frequencies) * (percentage / 100))

to_reverse	= []
for i in range(0, to_get):
	to_reverse.append(fourier_val[i])

test	= np.fft.ifft(to_reverse)
print test

#print fourier_freq[0]

#test			= np.fft.ifft(fourier_result)

#print test