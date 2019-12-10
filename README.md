# Project for Reinforcement Learning CS394R
## Facilitating Delayed-effect Requests on Trigger-ActionProgramming Frameworks
## Group Member: Jie Hua(jh67336), Sangsu Lee(sl44566)

### Dependencies:
Our program only needs `numpy` to run. 
### Go to the source folder
To run the program, go the source folder
```
cd src
```
### Configurations
We support different configurations in our program in order to run experiments easily.

To get the available options:
```
python3 main.py
```
The options are:
* **oven**: To enable oven rule.
* **coffee**: To enable coffee rule.
* **etrace/sarsa**: Choose the algorithm, "etrace" is Sarsa($$\lambda$$), "sarsa" is n-step Sarsa
* **extraFeature**: enable Extra features
* **baseline**: Run baseline approach
### Examples:
1. Run with oven environment, N-step Sarsa:
```
python3 main.py "oven sarsa"
```
2. Run with oven environment, N-step Sarsa and extra features:
```
python3 main.py "oven sarsa extraFeature"
```
3. Run with coffee environment, Sarsa($$\lambda$$):
```
python3 main.py "coffee etrace"
```
4. Run with both rules, N-step Sarsa and extra features(This one is slow):
```
python3 main.py "coffee oven sarsa extraFeature
```
