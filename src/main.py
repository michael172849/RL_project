import numpy as np
from deviceAction.tempAction import TempAction
from env import Env
from baselineEnv import BaselineEnv
from agents.agent import Agent
from agents.n_sarsa_agent import nSarsaAgent
from agents.e_trace_agent import ETraceAgent
from agents.tc_q import QFuncMixed
from agents.nn_q import QModelWithNN
from rules.seqRule import SeqRule
from rules.ovenRule import OvenRule
from dataModel import DataModel

def main(moreFeature=False):
    actions = []
    rules = []
    actions.append(TempAction(
        name = 'preheat',
        time_cost=300
    ))
    actions.append(TempAction(
        name = 'coffee',
        time_cost=300
    ))
    ovenSequence = [[{'loc_cate':'home_bed', 'act_truth':'Sleeping'}],
                    [{'loc_cate':'home_kitchen', 'act_truth':'Breakfast'}],]
    ovenRule = SeqRule(
        ovenSequence,
        200.,
        0.5,
        actions[0],
        seqWaitTime=1500,
        name="OvenRule",
    )
    coffeeSequence = [[{'loc_cate':'Restaurant', 'act_truth':'LunchOutside'}, {'loc_cate':'home_kitchen', 'act_truth':'LunchAtHome'}],
                    [{'loc_cate':'Office', 'act_truth':'AfternoonWork'}],]
    coffeeRule = SeqRule(
        coffeeSequence,
        200.,
        0.5,
        actions[1],
        seqWaitTime=1500,
        name="CoffeeRule",
    )

    rules.append(coffeeRule)
    rules.append(ovenRule)
    model = DataModel("coffee_guy")
    if moreFeature:
        nL = [model.get_num_locations(), model.get_num_locations()]
        nL.extend([2]*len(rules))
        nA = len(actions) * 2
        low, high = model.get_cont_low_high()
        low.append(0)
        high.append(1800)
        q_f = QFuncMixed(low, high, nL, nA, 5, np.array([4800, 120]))
    else:
        nL = [model.get_num_locations()]
        nA = len(actions) * 2
        low, high = model.get_cont_low_high()
        q_f = QFuncMixed(low, high, nL, nA, 5, np.array([4800]))
    # nn_f = QModelWithNN(low, high, nL, nA, 0.001)
    agent = nSarsaAgent(
        actions,
        q_f,
        10,
        0.9,
        0.1,
    )
    agent = ETraceAgent(
        actions,
        q_f,
        0.9,
        0.5,
        0.1,
    )

    environ = Env(actions, rules, agent, model)
    environ.run(300, moreFeature)
    
def baseline():
    actions = []
    rules = []
    actions.append(OvenAction(
        name = 'preheat',
        time_cost=300
    ))
    rules.append(OvenRule(
        200.,
        0.5,
        actions[0],
    ))
    model = DataModel("coffee_guy")
    env = BaselineEnv(actions, rules, model)
    env.run(500)
if __name__ == "__main__":
    main(True)
    # baseline()