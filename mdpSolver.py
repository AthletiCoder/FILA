def read_mdp(file_name):
	f = open(file_name, "r")
	d = {"numStates":0,
		 "numActions":0,
		 "discountFactor":None,
		 "rewards":None,
		 "transitions":None,
		 "type":'sad'}
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
	return None

def policy_iteration(file_name):
	return None
