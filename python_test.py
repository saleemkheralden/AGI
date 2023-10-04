import cv2 as cv
from Memory.Memory import Memory
import numpy as np
import torch
import matplotlib.pyplot as plt

memo = Memory(_size=(3, 480, 640))

cap = cv.VideoCapture(0)
flag = True
if not cap.isOpened():
    flag = False
    print("NO")

last_frame = None
i = 0
max_i = 10
while flag:
    ret, frame = cap.read()
    if not ret:
        print("No frame")
        break

    frame = cv.flip(frame, 1)

    memo.perceive_image(torch.FloatTensor(memo.unstack(frame)))
    if i == max_i:
        i = 0

        # memo.train_vision(plot_flag=True)

        x = memo.encoder.encode_image(torch.FloatTensor(memo.unstack(frame)))
        recon_frame = memo.decoder.decode_image(x).detach().numpy()
        print(frame.shape)
        print(recon_frame.shape)

        fig, ax = plt.subplots(1, 2)

        ax[0].imshow(frame)
        ax[1].imshow(np.stack(*recon_frame, axis=-1))
        plt.show()

        print("MAXI")
    print(i)

    cv.imshow('frame', frame)
    if cv.waitKey(1) == ord('q'):
        break
    i += 1

cap.release()
cv.destroyAllWindows()