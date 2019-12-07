from agents.agent import Agent

# def epsilon_greedy_policy(s,tc_Q,done, epsilon=.0):
#     nA = env.action_space.n
#     Q = [tc_Q.compute_value(s, a, done) for a in range(nA)]
#     if np.random.rand() < epsilon:
#         return np.random.randint(nA)
#     else:
#         return np.argmax(Q)
class nSarsaAgent(Agent):
    """
    Base class for agent
    """
    def __init__(
        self, 
        actions : list):
        self.actions = actions      #List of actions


    def getAction(self, state):
        return {'act':self.actions[0].startAction, 'id':0}
    
    def update(self, reward, action, state):
        pass
