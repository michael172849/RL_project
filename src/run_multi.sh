#! /bin/bash
for i in {0..5}
do
    python3 main.py "oven sarsa" > results/ocse${i}.txt &
done