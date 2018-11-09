#!/bin/bash
#
# Use this shell script to compile (if necessary) your code and then execute it. Below is an example of what might be found in this file if your program was written in Python
#
#python ./src/h1b_counting.py ./input/h1b_input.csv ./output/top_10_occupations.txt ./output/top_10_states.txt

#python ./src/h1b_counting.py -i ./input/H1B_FY_2016.csv -o1 ./output/top_10_occupations_H1B_FY_2016.txt  -o2 ./output/top_10_states_H1B_FY_2016.txt


python3 ./src/h1b_counting.py -i ./input/sample_data.csv -o1 ./output/top_10_occupations.txt -o2 ./output/top_10_states.txt
