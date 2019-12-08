import numpy as np
from agents.agent import Agent
class nSarsaAgent(Agent):
    def epsilon_greedy_policy(self, s_cont, s_cate, q_func, epsilon=.0):
        Q = [q_func.compute_value(s_cont, s_cate, a) for a in range(self.nA)]
        # print (Q)
        if np.random.rand() < epsilon:
            return np.random.randint(self.nA)
        else:
            return np.argmax(Q)

    def __init__(
        self, 
        actions : list,
        Q_func,
        n,
        gamma = 1.,
        alpha = 0.01):
        self.actions = actions      #List of actions
        self.nA = len(self.actions) * 2
        self.eps = 0.
        self.q_func = Q_func
        self.gamma = gamma
        self.alpha = alpha
        self.n = n
        self.resetTrace()

    def resetTrace(self):
        self.rewards = []
        self.states = []
        self.act_ids = []
        self.t = 0
        self.T = float('inf')


    def getAction(self, s):
        act_id = self.epsilon_greedy_policy(s[0], s[1], self.q_func, self.eps)
        if act_id % 2 == 0:
            return {'act':self.actions[act_id // 2].stopAction, 'id':act_id}
        else:
            return {'act':self.actions[act_id // 2].startAction, 'id':act_id}
    
    def update(self, s, reward, action, s_p):
        self.act_ids.append(action['id'])
        self.states.append(s)
        self.rewards.append(reward)
        tau = self.t - self.n
        self.t += 1
        if tau >= 0:
            returns = 0.
            if tau + self.n < self.T: 
                returns += self.q_func.compute_value(self.states[tau + self.n][0], 
                                                   self.states[tau + self.n][1],
                                                   self.act_ids[tau + self.n])
            for t_i in range(min(self.T, tau + self.n) - 1, tau - 1, -1):
                returns = returns * self.gamma + self.rewards[t_i]
            self.q_func.update(self.alpha, returns, self.states[tau][0], self.states[tau][1], self.act_ids[tau])
        return self.getAction(s_p)

    def finishEpisode(self, doneState):
        self.states.append(doneState)
        self.act_ids.append(self.getAction(doneState)['id'])
        self.T = self.t
        tau = self.t - self.n
        while tau < self.T - 1:
            if tau >= 0:
                returns = 0.
                if tau + self.n < self.T: 
                    returns += self.q_func.compute_value(self.states[tau + self.n][0], 
                                                    self.states[tau + self.n][1],
                                                    self.act_ids[tau + self.n])
                for t_i in range(min(self.T, tau + self.n) - 1, tau - 1, -1):
                    returns = returns * self.gamma + self.rewards[t_i]
                self.q_func.update(self.alpha, returns, self.states[tau][0], self.states[tau][1], self.act_ids[tau])
            self.t += 1
            tau = self.t - self.n
        self.resetTrace()


