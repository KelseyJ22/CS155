#!/usr/bin/env bash

if [ $# -ne 1 ]; then
  echo "Usage: ./runsample.sh PYTHONSOURCEFILE"
  exit
fi

echo "Running python file $1. Timing results:"
time python $1 < sample_again.in | python judge.py sample_again.out
