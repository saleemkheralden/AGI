import numpy as np

class MemoryUnit:

    def __init__(self,
                 id,
                 str_score=1.,
                 str_decay_factor=0.,
                 str_rein_factor=0.,):

        self.id = id
        self.init_score = 1
        self.str_score = str_score
        self.str_decay_factor = str_decay_factor
        self.str_rein_factor = str_rein_factor

        self.t = 1
        self.k = 1.84
        self.c = 1.25

    def linear_decay(self):
        self.str_score = self.str_score  - self.str_decay_factor
        return self.str_score

    def decay(self):
        self.str_score = self.str_score * self.str_decay_factor
        return self.str_score

    def ebbinghaus_decay(self, t=None):
        """
        :param t: time elapsed since the last decay
        :return:
        """
        if not t:
            t = 1
        self.t = self.t + t
        self.str_score = self.ebbinghaus_curve(self.t)
        return self.str_score

    def ebbinghaus_curve(self, t):
        return self.k / ((np.log(t) ** self.c) + self.k)

    def reinforce(self):
        self.str_score = self.str_score * (1 + self.str_rein_factor)
        return self.str_score
        # make the self.k higher








