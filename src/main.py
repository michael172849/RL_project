import numpy as np
from deviceAction.tempAction import TempAction
from env import Env
from baselineEnv import BaselineEnv
from agents.agent import Agent
from agents.n_sarsa_agent import nSarsaAgent
from agents.e_trace_agent import ETraceAgent
from agents.tc_q import QFuncMixed
from rules.seqRule import SeqRule
from rules.ovenRule import OvenRule
from dataModel import DataModel
import sys
def main(moreFeature=False, option="oven"):
    actions = []
    rules = []
    actions.append(TempAction(
        name = 'preheat',
        time_cost=300
    ))
    # actions.append(TempAction(
    #     name = 'coffee',
    #     time_cost=300
    # ))
    ovenSequence = [[{'loc_cate':'home_bed', 'act_truth':'Sleeping'}],
                    [{'loc_cate':'home_kitchen', 'act_truth':'Breakfast'}],]
    ovenRule = SeqRule(
        ovenSequence,
        200.,
        0.5,
        ovenAction,
        seqWaitTime=1500,
        name="OvenRule",
    )
    coffeeSequence = [[{'loc_cate':'Restaurant', 'act_truth':'LunchOutside'}, {'loc_cate':'home_kitchen', 'act_truth':'LunchAtHome'}],
                    [{'loc_cate':'Office', 'act_truth':'AfternoonWork'}],]
    coffeeRule = SeqRule(
        coffeeSequence,
        200.,
        0.5,
        coffeeAction,
        seqWaitTime=3600,
        name="CoffeeRule",
    )

    if "oven" in option:
        actions.append(ovenAction)
        rules.append(ovenRule)
    if "coffee" in option:
        actions.append(coffeeAction)
        rules.append(coffeeRule)
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
    if "sarsa" in option:
        agent = nSarsaAgent(
            actions,
            q_f,
            10,
            0.9,
            0.1,
        )
    if "etrace" in option:
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
    if len(sys.argv) < 2:
        print('Please provide option in one string. Execute the code like:  python3 main.py \"oven coffee etrace extraFeature\"')
        print('Avaiable options are:')
        print('oven: enable oven rule')
        print('coffee: enable coffee rule')
        print('etrace/sarsa: use n-step-sarsa algorithm or eligibility trace')
        print('extraFeature: enable extra features to make better predictions')
        exit(1)
    option = sys.argv[1]
    main("extraFeature" in option, option)
    # baseline()