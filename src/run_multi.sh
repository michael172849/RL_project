#! /bin/bash
for i in {0..5}
do
    python3 main.py "oven coffee sarsa extraFeature" > results/ocse${i}.txt &
done
wait
for i in {0..5}
do
    python3 main.py "oven coffee sarsa" > results/ocs${i}.txt &
done