def read_mdp(file_name):
	f = open(file_name, "r")
	d = {"numStates":0,
		 "numActions":0,
		 "discountFactor":None,
		 "rewards":None,
		 "transitions":None,
		 "type":None}
	i = 0
	for line in f:
		line = line.strip("\n")
		if i==0:
			d["numStates"] = int(line)
		elif i == 1:
			d['numActions'] = int(line)
		elif i < d["numStates"]*d["numActions"]+2:
			line = line.strip("\n")
			

def lp_solver():


def policy_iteration():


