import torch
import torch.nn as nn

class MemoryEncoder(nn.Module):
    def __init__(self, _size=(3, 100, 100)):
        super(MemoryEncoder, self).__init__()
        self.vision_cnn_encoder = nn.Sequential(
            nn.Conv2d(3, 16, kernel_size=5),
            nn.ReLU(),
            nn.MaxPool2d(2, stride=2),
            nn.Conv2d(16, 16, kernel_size=5),
            nn.ReLU(),
            nn.MaxPool2d(2, stride=2),
            nn.Conv2d(16, 32, kernel_size=3),
            nn.ReLU(),
            nn.Conv2d(32, 64, kernel_size=2),
            nn.ReLU(),
        )

        self.vision_ann_encoder = nn.Sequential(
            nn.Linear(self.ann_input_size(_size), 512),
            nn.Sigmoid(),
            nn.Linear(512, 300),
            nn.Sigmoid(),
            nn.Linear(300, 5),
        )

    def cnn_output_size(self, _size):
        return self.vision_cnn_encoder(torch.rand(1, *_size)).size()

    def ann_input_size(self, _size):
        _encoder_input = self.vision_cnn_encoder(torch.rand(1, *_size))
        _encoder_input = _encoder_input.data.view(1, -1).size(1)
        return _encoder_input



    def encode_image(self, image):
        x = self.vision_cnn_encoder(image)
        x = x.view(x.size(0) if len(x.size()) == 4 else 1, -1)
        return self.vision_ann_encoder(x)

    def forward(self, x):
        return self.encode_image(x)

    # def encode_audio(self, audio):
    #     return np.random.randn(10)




