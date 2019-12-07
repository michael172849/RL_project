from rules.rule import Rule
class OvenRuleWithCooling(Rule):
    def __init__(self, reward, decay, targetAction, timeLimit = 900, maxWaitTime = 600):
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
    def sec_to_str(self, sec):
        return str(int(sec/60/60)) + ":" + str(int(sec/60%60)) + ":" + str(int(sec%60))
    def check(
            self,
            s):
        if self.seqIdx == len(self.sequence):
            return self.isMet(s)
        if s['time'] - self.last > self.timeLimit:
            self.reset()
            return 0
        if (s['loc_cate'] == self.sequence[self.seqIdx]['loc_cate'] and
            s['act_truth'] == self.sequence[self.seqIdx]['act_truth']):
            self.seqIdx += 1
            if self.seqIdx == len(self.sequence): 
                print('Oven Rule met at time:{}'.format(self.sec_to_str(s['time'])))
            self.last = s['time']
        return 0
