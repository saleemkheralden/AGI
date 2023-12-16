from Memory.KnowledgeGraph import KnowledgeGraph
from Memory.Node import Node
from skimage import img_as_ubyte
from skimage.util import random_noise
import numpy as np

class LTM:

	def __init__(self):
		self.kg = KnowledgeGraph()

	def add_ltm_memo(self, memo: Node):
		memo.str_score = 1.
		self.kg.add_node(memo)

	# might change it to another class
	def decay_image(self, image, score, max_noise_str=2):
		"""
		:param image: the original image
		:param score: the strength score of the image
		:param max_noise_str: normalization factor to convert the score from [0, 1] range to [0, max_noise_str] range
		(used to make the noise variance higher)
		:return: noisy image
		"""
		# Convert image to uint8 format for compatibility with random_noise
		image_uint8 = img_as_ubyte(image)

		# Calculate the amount of noise based on the score
		noise_strength = 1.0 - score

		# Add noise to the image
		noisy_image = random_noise(image_uint8, var=(max_noise_str * noise_strength) ** 2)

		# Clip the values to [0, 1] range
		noisy_image = np.clip(noisy_image, 0, 1)

		return noisy_image



