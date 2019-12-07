
class Action():
    # define a device action like turn on the coffee machine.
    # We assume one device have one action

    def __init__(self, name, time_cost, step_cost = -1., step_time = 30.):
        self.name = name
        self.isOn = False
        self.onTime = 0
        self.step_cost = step_cost
        self.time_cost = time_cost
        self.step_time = step_time      # the step time in seconds
        self.last_check = 0.

    def stepReward(self, time):
        if not self.isOn:
            return 0.
        if self.last_check < self.onTime:
            self.last_check = self.onTime
        delta = time - self.last_check
        self.last_check = time
        return self.step_cost * (delta / self.step_time)

    def startAction(self, time):
        if not self.isOn:
            self.onTime = time
        self.isOn = True
    
    def stopAction(self, time):
        self.isOn = False
        self.onTime = 0
    
    def isReady(self, state):
        if self.isOn and state['time'] - self.onTime > self.time_cost:
            self.stopAction(state['time'])
            return True
        else:
            return False

    def isOn(self):
        return self.isOn