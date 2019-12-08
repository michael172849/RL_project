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
        self.nA = len(self.actions) * 2
        self.eps = 0.
        self.resetTrace()

    def resetTrace(self):
        self.new = True

    def getAction(self, s):
        act_id = self.epsilon_greedy_policy(s[0], s[1], self.q_func, self.w, self.eps)
        if act_id % 2 == 0:
            return {'act':self.actions[act_id // 2].stopAction, 'id':act_id}
        else:
            return {'act':self.actions[act_id // 2].startAction, 'id':act_id}

    def update(self, s, reward, action, s_p):
        a = action['id']
        if self.new:
            self.new = False
            self.x = self.q_func(s[0],s[1], a)
            self.z = np.zeros((self.q_func.feature_vector_len()))
            self.Q_old = .0

        a_n = self.getAction(s_p)
        x_n = self.q_func(s_p[0],s_p[1], a_n['id'])
        Q = np.dot(self.w, self.x)
        Q_n = np.dot(self.w, x_n)
        delta = reward + self.gamma * Q_n - Q
        self.z = self.gamma * self.lam * self.z +\
                (1-self.alpha*self.gamma*self.lam*np.dot(self.z, self.x))*self.x
        self.w += self.alpha * (delta + Q - self.Q_old) * self.z - \
                self.alpha*(Q - self.Q_old) * self.x
        self.Q_old = Q_n
        self.x = x_n

        return a_n

    def finishEpisode(self, doneState):
        #debug
        l = 10
        # Q = []
        # for i in range(l):
        #     Q = [np.dot(self.w, self.q_func([], [i], a)) for a in range(self.nA)]
        #     print(Q, i)

        

