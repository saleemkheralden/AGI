import torch.nn as nn

class MemoryDecoder(nn.Module):
    def __init__(self, ann_output, cnn_input):
        super(MemoryDecoder, self).__init__()
        self.vision_cnn_decoder = nn.Sequential(
            nn.ReLU(),
            nn.ConvTranspose2d(64, 32, kernel_size=2),
            nn.ReLU(),
            nn.ConvTranspose2d(32, 16, kernel_size=3),
            nn.ConvTranspose2d(16, 16, kernel_size=2, stride=2),
            nn.ReLU(),
            nn.ConvTranspose2d(16, 16, kernel_size=5),
            nn.ConvTranspose2d(16, 16, kernel_size=2, stride=2),
            nn.ReLU(),
            nn.ConvTranspose2d(16, 3, kernel_size=5),
        )

        self.cnn_input = cnn_input

        self.vision_ann_decoder = nn.Sequential(
            nn.Sigmoid(),
            nn.Linear(5, 300),
            nn.Sigmoid(),
            nn.Linear(300, 512),
            nn.Sigmoid(),
            nn.Linear(512, ann_output),
        )


    def decode_image(self, latent_x):
        x = self.vision_ann_decoder(latent_x)
        x = x.reshape(*self.cnn_input)
        return self.vision_cnn_decoder(x)

    def forward(self, x):
        return self.decode_image(x)


    # def decode_audio(self, audio):
    #     return np.random.randn(10)



