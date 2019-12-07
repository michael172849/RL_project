import numpy as np
from agents.agent import Agent

class ETraceAgent(Agent):
    def epsilon_greedy_policy(self, s_cont, s_cate, q_func, w, epsilon=.0):
        Q = [np.dot(w, q_func(s_cont, s_cate, a)) for a in range(self.nA)]
        if np.random.rand() < epsilon:
            return np.random.randint(self.nA)
        else:
            return np.argmax(Q)
    def __init__(self, 
                actions,
                q_f,
                gamma = 1.,
                lam = 0.8,
                alpha = 0.01):
        super().__init__(actions)
        self.actions = actions
        self.gamma = gamma
        self.q_func = q_f
        self.lam = lam
        self.alpha = alpha
        self.w = np.zeros((self.q_func.feature_vector_len()))

    def resetTrace(self):
        self.rewards = []
        self.states = []
        self.act_ids = []
        self.t = 0
        self.T = float('inf')
