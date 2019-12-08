# Time, Location(Room Label), Posture
# 
import numpy as np
from typing import Iterable
from deviceAction.action import Action
from rules.rule import Rule
from model import Model
from util import sec_to_str
class BaselineEnv():
    def __init__(self, 
                actions: Iterable[Action],
                rules: Iterable[Rule],
                model: Model,
                ):
        self.actions = actions
        self.rules = rules
        self.model = model
        self.state = None
        self.done = False

    def reset(self):
        self.model.reset()
        for action in self.actions:
            action.reset()
        self.rules_set = np.zeros(len(self.rules))
        self.state, self.done = self.model.step(0)

    def step(self, a):
        if self.done:
            return self.state, 0, self.done
        a['act'](self.state['time'])
        r = 0
        for action in self.actions:
            r += action.stepReward(self.state['time'])
        for i,rule in enumerate(self.rules):
            rr = rule.check(self.state)
            if rr > 0:
                self.rules_set[i] = 1
            r += rr
        s, done = self.model.step(30)
        return s, r, done

    def run(self, days, fix='Time'):
        for i in range(days):
            prev = "test"
            self.reset()
            r_s = 0
            print("======Day {}====================================================================".format(i))
            a = None
            while not self.done:
                if fix == 'Time':
                    if self.state['time'] >29290 and self.state['time'] < 29600 and self.rules_set[0] == 0:
                        a = {'act':self.actions[0].startAction, 'id':1}
                    else:
                        a = {'act':self.actions[0].stopAction, 'id':0}
                else:
                    if self.state['act_truth'] == 'Breakfast' and self.rules_set[0] == 0:
                        a = {'act':self.actions[0].startAction, 'id':1}
                    else:
                        a = {'act':self.actions[0].stopAction, 'id':0}
                s_p, r, self.done = self.step(a)
                self.state = s_p
                r_s += r
            print ("Return:{}!!!".format(r_s))
        
    