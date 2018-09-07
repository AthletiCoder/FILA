#!/bin/bash
POSITIONAL=()
while [[ $# -gt 0 ]]
do
key="$1"

case $key in
    -m|--mdp)
    MDP_FILE_PATH="$2"
    shift # past argument
    shift # past value
    ;;
    -a|--algorithm)
    ALGORITHM="$2"
    shift # past argument
    shift # past value
    ;;
    *)    # unknown option
    POSITIONAL+=("$1") # save it in an array for later
    shift # past argument
    ;;
esac
done

echo $(python3 mdpSolver.py "${MDP_FILE_PATH}" "${ALGORITHM}")