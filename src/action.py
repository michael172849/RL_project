
class Action():
    # define a device action like turn on the coffee machine.
    # We assume one device have one action

    def __init__(self, name, step_cost = -1., step_time = 30.):
        self.name = name
        self.isOn = False
        self.onTime = 0
        self.step_cost = step_cost
        self.step_time = step_time      # the step time in seconds

    def reward(self, time):
        if not self.isOn:
            return 0.
        delta = time - self.onTime
        return step_cost * (delta / self.step_time)

    def startAction(self, time):
        self.isOn = True
        self.onTime = time
    
    def endAction(self, time):
        self.isOn = False
        self.onTime = 0