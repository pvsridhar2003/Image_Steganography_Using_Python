#!/usr/bin/python

import os, sys
from PIL import Image

def main():
	"""
	Opens an image which contains information of a hidden image,
	recovers the hidden image and saves it in a specified or
	default location.

	"""
	if len(sys.argv) < 2 or len(sys.argv) > 3:
		print ("")
		print ("DECODING THE IMAGE :")
		print ("To recover a concealed image, specify the")
		print ("path to the image in which it is hidden.")
		print ("As an optional argument, you can specify the")
		print ("path to save the restored image to.")
		print ("If not specified then the image will be stored")
		print ("by default as C:/Users/Username/Decoded_image.png")
		print ("")
		print ("Enter the Data in the following format in Terminal :")
		print ("python path/to/Decode.py path/to/image/to/restore/from path/to/save/the/image/to")
		print ("")
		print ("Example:")
		print ("python C:/Users/Decode.py C:/Users/output.png C:/Users/res.png")
		print ("")
		return
	if len(sys.argv) >= 2:
		img_path = sys.argv[1]
	if len(sys.argv) >= 3:
		output_path = sys.argv[2]
		filename = os.path.splitext(output_path)
		output_path = filename[0] + '.png'
	else:
		output_path = 'Decoded_image.png'
	decoded_image = decode(Image.open(img_path), img_path)
	decoded_image.save(output_path)
	print ("")
	print ("Image Decoded")
	print ("")
 
def add_leading_zeros(binary_number, expected_length):
	"""
	Adds leading zeros to a binary number so that the number of characters
	in the binary string matches the specified expected length and the value
	of the binary sring remains unchanged.

	"""
	length = len(binary_number)
	return (expected_length - length) * '0' + binary_number

def rgb_to_binary(r, g, b):
	"""
	Converts decimal numbers representing RGB values of a pixel into
	binary numbers of the same values.

	"""
	return add_leading_zeros(bin(r)[2:], 8), add_leading_zeros(bin(g)[2:], 8), add_leading_zeros(bin(b)[2:], 8)

def extract_hidden_pixels(image, width_visible, height_visible, pixel_count):
	"""
	Extracts a sequence of bits representing a sequence of binary values of 
	all pixels of the hidden image.
	The information representing a hidden image is stored in the 4 least significant
	bits of a subset of pixels of the visible image.

	"""
	hidden_image_pixels = ''
	idx = 0
	for col in range(width_visible):
		for row in range(height_visible):
			if row == 0 and col == 0:
				continue
			r, g, b = image[col, row]
			r_binary, g_binary, b_binary = rgb_to_binary(r, g, b)
			hidden_image_pixels += r_binary[4:8] + g_binary[4:8] + b_binary[4:8]
			if idx >= pixel_count * 2:
				return hidden_image_pixels
	return hidden_image_pixels

def reconstruct_image(image_pixels, width, height):
	"""
	Recontructs the hidden image using the extracted string of pixel binary values.

	"""
	image = Image.new("RGB", (width, height))
	image_copy = image.load()
	idx = 0
	for col in range(width):
		for row in range(height):
			r_binary = image_pixels[idx:idx+8]
			g_binary = image_pixels[idx+8:idx+16]
			b_binary = image_pixels[idx+16:idx+24]
			image_copy[col, row] = (int(r_binary, 2), int(g_binary, 2), int(b_binary, 2))
			idx += 24
	return image
	
def decode(image, img_path):
	"""
	Loads the image to recover a hidden image from, retrieves the information about the
	size of the hidden image stored in the top left pixel of the visible image,
	extracts the hidden binary pixel values from the image and reconstructs the hidden image.

	"""
	image = Image.open(img_path)
	image_copy = image.load()
	width_visible, height_visible = image.size
	r, g, b = image_copy[0, 0]
	r_binary, g_binary, b_binary = rgb_to_binary(r, g, b)
	w_h_binary = r_binary + g_binary + b_binary
	width_hidden = int(w_h_binary[0:12], 2)
	height_hidden = int(w_h_binary[12:24], 2)
	pixel_count = width_hidden * height_hidden
	hidden_image_pixels = extract_hidden_pixels(image_copy, width_visible, height_visible, pixel_count)
	decoded_image = reconstruct_image(hidden_image_pixels, width_hidden, height_hidden)
	return decoded_image

if __name__ == '__main__':
	main()
