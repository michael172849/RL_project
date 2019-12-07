import numpy as np
from agents.agent import Agent
from agents.tc_q import QFuncMixed
class nSarsaAgent(Agent):
    """
    Base class for agent
    """
    def epsilon_greedy_policy(self, s_cont, s_cate, tc_Q, epsilon=.0):
        Q = [tc_Q.compute_value(s_cont, s_cate, a) for a in range(self.nA)]
        if np.random.rand() < epsilon:
            return np.random.randint(self.nA)
        else:
            return np.argmax(Q)
    def __init__(
        self, 
        actions : list,
        Q_func):
        self.actions = actions      #List of actions
        self.nA = len(self.actions) * 2
        self.eps = 0.01
        self.tc_Q = Q_func

    def getAction(self, s_cont, s_cate):
        action = self.epsilon_greedy_policy(s_cont, s_cate, self.tc_Q, self.eps)
        return {'act':self.actions[0].startAction, 'id':0}
    
    def update(self, s_cont, s_cate, reward, action):
        pass

    def finishEpisode(self):
        pass
