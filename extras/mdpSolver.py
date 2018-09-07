from pulp import *
import random
import sys

def read_mdp(file_name):
	f = open(file_name, "r")
	d = {"numStates":0,
		 "numActions":0,
		 "discountFactor":None,
		 "rewards":None,
		 "transitions":None,
		 "type":None}
	i = 0
	stateCount = 0
	actCount = 0	
	for line in f:
		line = line.strip("\n")
		if i==0:
			d["numStates"] = int(line)
		elif i == 1:
			d['numActions'] = int(line)
			d["rewards"] = [[None for i in range(d['numActions'])] for j in range(d["numStates"])]
			d["transitions"] = [[None for i in range(d['numActions'])] for j in range(d["numStates"])]
		elif i < d["numStates"]*d["numActions"]+2:
			line = line.rstrip()
			line = line.split("\t")
			d["rewards"][stateCount][actCount] = [float(x.rstrip()) for x in line]
			actCount = (actCount+1)%d['numActions']
			if actCount == 0:
				stateCount += 1
		elif i < 2*d["numStates"]*d["numActions"]+2:
			line = line.rstrip()
			if i == d["numStates"]*d["numActions"]+2:
				stateCount = 0
				actCount = 0
			line = line.split("\t")
			d["transitions"][stateCount][actCount] = [float(x.rstrip()) for x in line]
			actCount = (actCount+1)%d['numActions']
			if actCount == 0:
				stateCount += 1
		elif i == 2*d["numStates"]*d["numActions"]+2:
			d["discountFactor"] = float(line)
		elif i == 2*d["numStates"]*d["numActions"]+3:
			d["type"] = str(line)
		i += 1
	f.close()
	return d
			

def lp_solver(file_name):
	dB = read_mdp(file_name)
	prob = LpProblem("MDP Solver", LpMinimize)
	# initialising Lp variables which represent the value function of all states
	V = [LpVariable("v"+str(i),None) for i in range(dB["numStates"])]	 
	# defining the objective function as sum of all variables
	prob += sum(x for x in V), "Objective function"
	# constraints of optimal value function
	for s in range(dB['numStates']):
		for a in range(dB['numActions']):
			lhs = ""
			for sPrime in range(dB['numStates']):
				lhs += dB['transitions'][s][a][sPrime]*dB['rewards'][s][a][sPrime]+dB['transitions'][s][a][sPrime]*dB['discountFactor']*V[sPrime]
			prob += lhs <= V[s], "V-"+str(s)+","+str(a)
	prob.solve()
	valueFunction = []
	for var in prob.variables():
		valueFunction.append(value(var))
	# getting the optimal policy from optimal value function
	policy = optimal_policy(valueFunction, dB)
	for i in range(len(valueFunction)):
		print(valueFunction[i], policy[i])
	return valueFunction

def optimal_policy(valueFunction, dB):
	policy = []
	for s in range(dB['numStates']):
		maxSoFar = -99999999
		bestAction = None
		for a in range(dB['numActions']):
			Sum = 0
			for sPrime in range(dB['numStates']):
				Sum += dB['transitions'][s][a][sPrime]*(dB['rewards'][s][a][sPrime]+dB['discountFactor']*valueFunction[sPrime])
			if Sum > maxSoFar:
				maxSoFar = Sum
				bestAction = a
		policy.append(bestAction)
	return policy

def Q_evaluation(policy, file_name):
	dB = read_mdp(file_name)
	Q = [[None for a in range(dB['numActions'])] for s in range(dB['numStates'])]
	prob = LpProblem("MDP Solver", LpMinimize)
	# initialising Lp variables which represent the value function of all states
	V = [LpVariable("v"+str(i),None) for i in range(dB["numStates"])]	 
	# defining the objective function as sum of all variables
	prob += sum(x for x in V), "Objective function"
	# constraints of V_pi
	for s in range(dB['numStates']):
		lhs = ""
		for sPrime in range(dB['numStates']):
			lhs += dB['transitions'][s][policy[s]][sPrime]*dB['rewards'][s][policy[s]][sPrime]+dB['transitions'][s][policy[s]][sPrime]*dB['discountFactor']*V[sPrime]
		prob += lhs == V[s], "V-"+str(s)
	prob.solve()
	valueFunction = []
	for var in prob.variables():
		valueFunction.append(value(var))
	Q = [[None for i in range(dB['numActions'])] for j in range(dB['numStates'])]
	for s in range(dB['numStates']):
		for a in range(dB['numActions']):
			temp = 0
			for sPrime in range(dB['numStates']):
				temp += dB['transitions'][s][a][sPrime]*(dB['rewards'][s][a][sPrime] + dB['discountFactor']*valueFunction[sPrime])
			Q[s][a] = temp
	return Q



def policy_iteration(file_name):
	policy = []
	dB = read_mdp(file_name)
	for i in range(dB['numStates']):
		policy.append(random.randint(0,dB['numActions']-1))
	converged = False
	while converged!=True:
		converged = True
		Q = Q_evaluation(policy, file_name)
		for s in range(dB['numStates']):
			for a in range(dB['numActions']):
				if Q[s][a] > Q[s][policy[s]]:
					converged = False
					policy[s] = a
					break
	print(policy)
	return policy


if sys.argv[2] == "lp":
	lp_solver(sys.argv[1])
elif sys.argv[2] == "hpi":
	policy_iteration(sys.argv[1])
