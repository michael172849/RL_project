#! /bin/bash
ROOT="${HOME}/protemp/Courses/ReinforcementLearning/RL_project"
cd ${ROOT}
for d in $(find data/ -type d)
do
    cd ${ROOT}
    cd ${d}
    for z in *.zip
    do
        dir="${z%%.*}"
        mkdir ${dir}
        unzip ${z} -d ${dir}
    done
done