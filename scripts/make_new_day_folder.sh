#!/usr/bin/env bash
#
# Creates a new day folder

DAY_FOLDER="src/day-$1"
DAY1_TASKS_FILE="src/day-1/tasks.py"

mkdir $DAY_FOLDER $DAY_FOLDER/inputs

touch $DAY_FOLDER/inputs/input.txt
touch $DAY_FOLDER/inputs/sample.txt
touch $DAY_FOLDER/inputs/test1.txt
touch $DAY_FOLDER/inputs/test2.txt
touch $DAY_FOLDER/__init__.py

cp $DAY1_TASKS_FILE $DAY_FOLDER/$(basename $DAY1_TASKS_FILE)
