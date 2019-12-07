# Time, Location(Room Label), Posture
# 
from typing import Iterable
from agents.agent import Agent
from action import Action
from rules.rule import Rule
from model import Model
class Env():
    def __init__(self, 
                actions: Iterable[Action],
                rules: Iterable[Rule],
                agent: Agent,
                model: Model,
                ):
        self.actions = actions
        self.agent = agent
        self.rules = rules
        self.model = model
        self.state = None
        self.done = False

    def reset(self):
        self.model.reset()
        self.state, self.done = self.model.step(0)

    def step(self, a):
        if self.done:
            return self.state, 0, self.done
        a['act'](self.state['time'])
        r = 0
        for action in self.actions:
            r += action.stepReward(self.state['time'])
        
        for rule in self.rules:
            r += rule.check(self.state)
        s, done = self.model.step()
        return s, r, done

    def run(self, days):
        for i in range(days):
            flag = False
            self.reset()
            while not self.done:
                if self.state['act_truth'] == "Wake up" and flag == False:
                    flag = True
                    print (i, self.state)
                a = self.agent.getAction(self.state)
                s_p, r, self.done = self.step(a)
                self.agent.update(r,a,self.state)
                self.state = s_p
                # if r > 0:
                    # print(i, self.state['time'], r)
        
    