#!/bin/bash

ph="$1"

echo $(python3 extras/mdpSolver.py "${ph}")