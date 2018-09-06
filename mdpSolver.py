from pulp import *

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
	V = [LpVariable("v"+str(i),0) for i in range(dB["numStates"])]
	for s in range(dB['numStates']):
		prob += sum(x for x in V), "Objective function"
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
	policy = optimal_policy(valueFunction, dB)
	for i in range(len(valueFunction)):
		print(valueFunction[i], policy[i])

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

def policy_iteration(file_name):
	return None


lp_solver(file_name = "/media/varunkumar/Entertainment/Courses/Sem7/CS747/assignments/assignment2/data/continuing/MDP10.txt")
