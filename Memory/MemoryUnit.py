import numpy as np

class MemoryUnit:

    def __init__(self,
                 id,
                 str_score=0.,
                 str_decay_factor=0.,
                 str_rein_factor=0.,):

        self.id = id
        self.init_score = str_score
        self.str_score = str_score
        self.str_decay_factor = str_decay_factor
        self.str_rein_factor = str_rein_factor

        self.t = 1
        self.k = 1.84
        self.c = 1.25

    def linear_decay(self):
        self.str_score = self.str_score  - self.str_decay_factor

    def decay(self):
        self.str_score = self.str_score * self.str_decay_factor

    def ebbinghaus_decay(self):
        self.str_score = self.init_score * self.ebbinghaus_curve()
        self.t = self.t + 1

    def ebbinghaus_curve(self):
        return self.k / ((np.log(self.t) ** self.c) + self.k)

    def reinforce(self):
        self.str_score = self.str_score * (1 + self.str_rein_factor)
        # make the self.k higher








