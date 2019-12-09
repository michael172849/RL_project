from rules.rule import Rule
from util import sec_to_str
class SeqRule(Rule):
    def __init__(self, sequence, reward, decay, targetAction, seqWaitTime = 1200, maxWaitTime = 600, name='SequencialRule'):
        super().__init__(reward, decay)
        self.sequence = sequence
        self.seqWaitTime = seqWaitTime          #max time difference between sequence in seconds
        self.targetAction = targetAction
        self.maxWaitTime = maxWaitTime
        self.name = name
        self.reset()

    def reset(self):
        self.seqIdx = 0
        self.last = 10000000
        self.last_check_time = None

    def isMet(self, s):
        if s['time'] - self.last > self.maxWaitTime:
            self.reset()
            return 0
        if self.last_check_time is None:
            self.last_check_time = s['time']
        if self.targetAction.isReady(s):
            self.reset()
            return self.reward
        else:
            step_r = -self.decay * (s['time'] - self.last_check_time)
            self.last_check_time = s['time']
            return step_r

    def check(
            self,
            s):
        if self.seqIdx == len(self.sequence):
            return self.isMet(s)
        if self.seqIdx > 0:
            if (s['act_truth'] in [ac['act_truth'] for ac in self.sequence[self.seqIdx-1]]):
                self.last = s['time']
        if s['time'] - self.last > self.seqWaitTime:
            self.reset()
            return 0
        if (s['act_truth'] in [ac['act_truth'] for ac in self.sequence[self.seqIdx]]):
            self.seqIdx += 1
            if self.seqIdx == len(self.sequence): 
                print(self.name + ' met at time:{}'.format(sec_to_str(s['time'])))
            self.last = s['time']
        return 0
