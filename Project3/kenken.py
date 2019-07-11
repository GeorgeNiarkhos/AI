from csp import *
import time
import sys

size2 = 4

clique2 = {(0,0): (0,"-",1),(0,1): (1,"/",2),(0,2): (2,"*",12),(0,3): (2,"*",12),(1,0): (0,"-",1),(1,1): (1,"/",2),(1,2): (3,"none",3),(1,3): (2,"*",12),(2,0): (4,"none",4),(2,1): (5,"+",9),(2,2): (5,"+",9),(2,3): (6,"/",2),(3,0): (7,"+",4),(3,1): (7,"+",4),(3,2): (5,"+",9),(3,3): (6,"/",2)	
}

size1 = 3

clique1 = {
	(0,0): (0,"-",1),(0,1): (0,"-",1),(0,2): (1,"-",2),(1,0): (2,"+",5),(1,1): (2,"+",5),(1,2): (1,"-",2),(2,0): (3,"none",3),(2,1): (4,"/",2),(2,2): (4,"/",2)
}

size3 = 6

clique3 = {
	(0,0): (0,"+",11),
	(0,1): (1,"/",2),
	(0,2): (1,"/",2),
	(0,3): (2,"*",20),
	(0,4): (3,"*",6),
	(0,5): (3,"*",6),
	(1,0): (0,"+",11),
	(1,1): (4,"-",3),
	(1,2): (4,"-",3),
	(1,3): (2,"*",20),
	(1,4): (5,"/",3),
	(1,5): (3,"*",6),
	(2,0): (6,"*",240),
	(2,1): (6,"*",240),
	(2,2): (7,"*",6),
	(2,3): (7,"*",6),
	(2,4): (5,"/",3),
	(2,5): (3,"*",6),
	(3,0): (6,"*",240),
	(3,1): (6,"*",240),
	(3,2): (8,"*",6),
	(3,3): (9,"+",7),
	(3,4): (10,"*",30),
	(3,5): (10,"*",30),
	(4,0): (11,"*",6),
	(4,1): (11,"*",6),
	(4,2): (8,"*",6),
	(4,3): (9,"+",7),
	(4,4): (9,"+",7),
	(4,5): (12,"+",9),
	(5,0): (13,"+",8),
	(5,1): (13,"+",8),
	(5,2): (13,"+",8),
	(5,3): (14,"/",2),
	(5,4): (14,"/",2),
	(5,5): (12,"+",9),
}


class KenKen(CSP):

	def __init__(self, test):
		self.size = 0
		self.cliques = []
		if (test == "1"):		##test 3x3
			global size1
			self.size = size1
			global clique1
			self.cliques = clique1
		elif (test == "2"):		##test 4x4
			global size2
			self.size = size2	
			global clique2
			self.cliques = clique2
		elif (test == "3"):		##test 6x6 ergasias3
			global size3
			self.size = size3
			global clique3
			self.cliques = clique3
		
		self.vars = []
		self.cliqueInfo = defaultdict(list)		##preinitialized dicts
		self.domains = defaultdict(list)
		self.neighbours = defaultdict(list)
		for i in range(self.size):
			for j in range(self.size):
				self.vars.append((i,j))	#init vars
				

		for i in self.vars:
			for k in range(self.size):
				self.domains[i].append(k+1)	#init each vars domain
			self.cliqueInfo[self.cliques[i][0]].append(i)	#from cliques init cliqueInfo key:0 var:list((x,y),..)	
		
		for i in self.vars:		
			for j in self.vars:
				if (i != j):
					if (i[0] == j[0] or i[1] == j[1]):	#same rows and col neighbours
						self.neighbours[i].append((j))
			for j in self.cliqueInfo:					#same clique neighbours
				if (i in self.cliqueInfo[j]):
					for k in self.cliqueInfo[j]:
						if (k != i and k not in self.neighbours[i]):	##no duplicates
							self.neighbours[i].append(k)
					break;

		CSP.__init__(self,self.vars,self.domains,self.neighbours,self.constraints)

	def constraints(self,A,a,B,b):
		if (A[0] == B[0] or A[1] == B[1]): # if on same row or col then value a,b should differ
			if (a == b):
				return False
		     
		if (self.cliques[A][0] == self.cliques[B][0]):		#same clique id
			# print(A,a,"---",B,b)
			assignments = self.infer_assignment()
			count = 0
			cliqueId = self.cliques[A][0]
			operation = self.cliques[A][1]
			cliqueTarget = self.cliques[A][2]
			
			if (operation == "+"):
				target = 0	##add
				for i in self.cliqueInfo[cliqueId]:
					if (i != A and i != B and i in assignments):	##except A, B
						count += 1
						target += assignments[i]
				target +=  a + b
				if (count+2 == len(self.cliqueInfo[cliqueId])):
					return target == cliqueTarget
				elif (count+2 < len(self.cliqueInfo[cliqueId])):
					return target < cliqueTarget
				else:
					return False
			elif (operation == "-"):
				return abs(a-b) == cliqueTarget
			elif (operation == "*"):
				target = 1	##mult
				for i in self.cliqueInfo[cliqueId]:
					if (i != A and i !=B and i in assignments):	##except A, B
						count += 1
						target *= assignments[i]
				target *=  a * b
				if (count+2 == len(self.cliqueInfo[cliqueId])):
					return target == cliqueTarget
				elif (count+2 < len(self.cliqueInfo[cliqueId])):
					return target <= cliqueTarget	##situation of 7 * 1 = 7 for = in <=
				else:
					return False
			elif (operation == "/"):
				if (a > b):		##select bigger to divide
					return a/b == cliqueTarget
				else:
					return b/a == cliqueTarget
		return True
		
	
	def print(self,r):
		if (r == None):
			print ("Result is empty")
			return
		sort = sorted(r.items())
		for j in sort:
			print(j[1]," ",end='\0')
			if (j[0][1] == self.size-1):	##switch line
				print("\n", end='\0')


test = sys.argv[1]	
k = KenKen(test)

### BT
start = time.clock()
r = backtracking_search(k)
t = time.clock() - start
print("BT Time: %s sec"% t)
print("BT Assignments: %s"% k.nassigns)
k.print(r)

###BT+FC
k = KenKen(test)
start = time.clock()
r = backtracking_search(k, inference=forward_checking)
t = time.clock() - start
print("FC Time: %s sec"% t)
print("FC Assignments: %s"% k.nassigns)
k.print(r)

###BT+FC+MRV
k = KenKen(test)
start = time.clock()
r = backtracking_search(k, select_unassigned_variable=mrv,inference=forward_checking)
t = time.clock() - start
print("FC+MRV Time: %s sec"% t)
print("FC+MRV Assignments: %s"% k.nassigns)
k.print(r)

###BT+MAC
k = KenKen(test)
start = time.clock()
r = backtracking_search(k, inference=mac)
t = time.clock() - start
print("MAC Time: %s sec"% t)
print("MAC Assignments: %s"% k.nassigns)
k.print(r)

### BT+MRV
k = KenKen(test)
start = time.clock()
r = backtracking_search(k, select_unassigned_variable=mrv)
t = time.clock() - start
print("BT+MRV Time: %s sec"% t)
print("BT+MRV Assignments: %s"% k.nassigns)
k.print(r)

###MINCON
k = KenKen(test)
start = time.clock()
r = min_conflicts(k)
t = time.clock() - start
print("MINCON Time: %s sec"% t)
print("MINCON Assignments: %s"% k.nassigns)
k.print(r)

