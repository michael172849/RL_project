from deviceAction.action import Action
from util import sec_to_str
class TempAction(Action):
    # define a device action like turn on the coffee machine.
    # We assume one device have one action

    def __init__(self, name, time_cost, step_cost = -1., step_time = 60., set_temp = 100.):
        self.name = name
        self.step_cost = step_cost
        self.temp_chg = [-0.5, set_temp / time_cost]
        self.set_temp = set_temp
        self.step_time = step_time      # the step time in seconds
        self.reset()

    def reset(self):
        self.last_check = -10.
        self.isOn = 0
        self.cur_temp = 0.

    def stepReward(self, time):
        if self.last_check < 0:
            self.last_check = time
        self.cur_temp += self.temp_chg[self.isOn] * (time - self.last_check)
        self.cur_temp = min(self.set_temp+20, max(self.cur_temp, 0))
        delta = time - self.last_check
        self.last_check = time
        if self.isOn == 0:
            return 0.
        return self.step_cost * (delta / self.step_time)

    def startAction(self, time):
        self.isOn = 1
    
    def stopAction(self, time):
        self.isOn = 0
    
    def isReady(self, state):
        # print (self.cur_temp, state['time'])
        if self.cur_temp >= self.set_temp:
            print ("Finish" + sec_to_str(state['time']))
            return True
        else:
            return False

    def isOn(self):
        return self.isOn == 1