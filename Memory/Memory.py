import numpy as np

from Memory.MemoryEncoder import MemoryEncoder
from Memory.MemoryDecoder import MemoryDecoder
from Memory.KnowledgeGraph import KnowledgeGraph, Node
from hashlib import sha3_512 as sha
import torch
import torch.nn as nn
import matplotlib.pyplot as plt

class Memory:
    def __init__(self, _size=(3, 100, 100)):
        self.encoder = MemoryEncoder(_size)
        self.decoder = MemoryDecoder(
            self.encoder.ann_input_size(_size),
            self.encoder.cnn_output_size(_size))
        self.knowledge_graph = KnowledgeGraph()
        self.image_idx = 0
        self.text_idx = 0

        self.images = []
        self.images_cap = 1000

    def perceive_image(self, image):
        self.images.append(image)
        if len(self.images) > self.images_cap:
            self.images.pop(0)

        self.knowledge_graph.add_node(Node(id=self.hash(f"image_{self.image_idx}"),
                                           type="image",
                                           attributes={"encoding": self.encoder.encode_image(image)}))
        self.image_idx += 1

    def unstack(self, img: np.ndarray):
        s = img.shape[-1]
        return np.array([img[:, :, i] for i in range(s)])


    def train_vision(self, plot_flag=False):
        learning_rate = 0.001
        weight_decay = 0.5

        loss_plot = []


        criterion = nn.MSELoss()
        encoder_optimizer = torch.optim.Adam(self.encoder.parameters(), lr=learning_rate, weight_decay=weight_decay)
        decoder_optimizer = torch.optim.Adam(self.decoder.parameters(), lr=learning_rate, weight_decay=weight_decay)


        for image in self.images:
            latent_x = self.encoder(image)
            recon_image = self.decoder(latent_x)

            if image.shape != recon_image.shape:
                raise Exception('image.shape != recon_image.shape')

            loss = criterion(recon_image, image)
            loss.backward()
            encoder_optimizer.step()
            decoder_optimizer.step()

            if plot_flag:
                loss_plot.append(loss.item())

        if plot_flag:
            plt.plot(np.arange(len(loss_plot)), loss_plot)




    def perceive_text(self, text):
        self.knowledge_graph.add_node(Node(id=self.hash(f"text_{self.text_idx}"),
                                           type="text",
                                           attributes={"encoding": self.encoder.encode_text(text)}))
        self.text_idx += 1

    def hash(self, str):
        return sha(f'{str}'.encode('utf-8')).hexdigest()


