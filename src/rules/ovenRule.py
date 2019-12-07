from rules.rule import Rule
class OvenRule(Rule):
    def __init__(self, reward, decay, targetAction, timeLimit = 900, maxWaitTime = 900):
        super().__init__(reward, decay)
        self.sequence = [{'loc_cate':'home_bedroom', 'act_truth':'Wake up'},
                    {'loc_cate':'home_bathroom', 'act_truth':'PersonalGrooming'},
                    {'loc_cate':'home_kitchen', 'act_truth':'Breakfast'},]
        self.timeLimit = timeLimit          #max time difference between sequence in seconds
        self.targetAction = targetAction
        self.maxWaitTime = maxWaitTime
        self.reset()

    def reset(self):
        self.seqIdx = 0
        self.last = 10000000

    def isMet(self, s):
        if s['time'] - self.last > self.maxWaitTime:
            self.reset()
            return 0
        if self.targetAction.isReady(s):
            return self.reward - self.decay * (s['time'] - self.last)
        else:
            return 0
    def check(
            self,
            s):
        if self.seqIdx == len(self.sequence):
            return self.isMet(s)
        if s['time'] - self.last > self.timeLimit:
            self.reset()
            return 0
        print (s)
        if (s['loc_cate'] == self.sequence[self.seqIdx]['loc_cate'] and
            s['act_truth'] == self.sequence[self.seqIdx]['act_truth']):
            print(s['time'])
            self.seqIdx += 1
            self.last = s['time']
        return 0
