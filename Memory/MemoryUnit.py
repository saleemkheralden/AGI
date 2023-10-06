class MemoryUnit:

    def __init__(self,
                 imp_score=.0,
                 imp_spike_factor=.0,
                 imp_spike_add=.0,
                 imp_decay_factor=.0,
                 core_thresh=.0,
                 ob_thresh=.0,

                 act_score=.0,
                 act_decay_factor=.0,):

        self.imp_score = imp_score
        self.imp_spike_factor = imp_spike_factor
        self.imp_spike_add = imp_spike_add
        self.imp_decay_factor = imp_decay_factor

        self.core_thresh = core_thresh
        self.ob_thresh = ob_thresh

        self.act_score = act_score
        self.act_decay_factor = act_decay_factor



    def excite(self):
        self.act_score = 1

    def strengthen(self):
        self.imp_score = self.imp_score * self.imp_spike_factor + self.imp_spike_add

    def imp_decay(self):
        self.imp_score = self.imp_score * self.imp_decay_factor

    def act_decay(self):
        self.act_score = self.act_score * self.act_decay_factor









