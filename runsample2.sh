#!/usr/bin/env bash

if [ $# -ne 1 ]; then
  echo "Usage: ./runsample.sh PYTHONSOURCEFILE"
  exit
fi

echo "Running python file $1. Timing results:"
time python $1 < sample2.in | python judge.py sample2.out
echo "If user time + system time < 10 seconds, you should be fine for 
the real test."
