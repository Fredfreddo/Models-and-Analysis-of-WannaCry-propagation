import matplotlib.pyplot as plt 
import random
import numpy as np
import networkx as nx
# let user input 5 parameters
total_nodes_number=int(input('Size of graph, positive integer larger than 1: \n'))
prob=float(input('Float, probability of spreading to neighbors, 0<p<=1: \n'))
A=float(input("Alpha for quasi-linear PA model, positive float: \n"))
total_time=int(input('Total time of spreading: \n'))
threshold=float(input('Threshold for immunizing, positive float: \n'))
def run(total_nodes_number,prob,A,total_time,threshold): #main function
	adj_mat=[[0,1],[1,0]] #initial graph adjacency matrix
	i=3
	degree=[1,2] #initial degrees by configuration model
	table={1:1,2:1} #initial degree dictionary
	while i<=total_nodes_number:
		for row in adj_mat:
			row.append(0)
		adj_mat.append([0]*i) #update matrix size from n*n to (n+1)*(n+1)
		weight=[] #weight for deciding which node to link
		alpha=A
		values=list(table.values())
		total=0
		for value in values:
			total+=value**alpha # total=sum of old degrees**A
		exist=list(table.keys())
		for node in exist:
			weight.append(table[node]**alpha/total) #assign weight according to sub-linear PA model
		new_link=random.choices(exist,weights=weight,k=1)[0] #choose new link to establish
		degree.append(new_link) #update configuration model
		degree.append(i) #update configuration model
		table[i]=1
		table[new_link]+=1 # update degree dictionary
		node_name=new_link
		adj_mat[node_name-1][i-1]=1
		adj_mat[i-1][node_name-1]=1 #update adjacency matrix
		i+=1
	healthy=list(range(2,total_nodes_number+1))
	imm=[]
	infected=[1] #initialize three types of nodes
	time=1
	infsize=[]
	healsize=[]
	immsize=[]
	mark_time=[] #to mark vaccination starting point
	while time<=total_time:
		potential=[] 
		for nodes in infected:
			i=0
			while i<=total_nodes_number-1:
				if adj_mat[nodes-1][i]==1:
					potential.append(i+1) # find all neighbors of already infected nodes
				i+=1
		infection=[]
		for man in potential:
			d=prob
			bi=random.random()
			if bi<=d:
				infection.append(man) #decide whether to infect or not by probability p
		for guys in infection:
			if guys in healthy:
				infected.append(guys)
				healthy.remove(guys) # update nodes' types
		if len(table)>0 and len(healthy)>0 and len(infected)>=total_nodes_number*threshold:
			mark_time.append(time) # mark vaccination starting point
			mx=0
			for k in table.keys():
				if k in healthy and table[k]>mx:
					mx=table[k]
					sel=k # find the healthy node with highest degree
			print('{},{}'.format(sel,time)) #print vaccination object and time
			healthy.remove(sel)
			imm.append(sel) # update node type
			del table[sel]
		infsize.append(len(infected))
		healsize.append(len(healthy))
		immsize.append(len(imm)) #store numbers of node types
		time+=1
	if len(mark_time)>0:
		markt=mark_time[0] # mark vaccination starting time
	else:
		markt=time
	plt.plot(range(1,total_time+1),infsize,label='infected number, infected ratio={}'.format(len(infected)/total_nodes_number))
	plt.plot(range(1,total_time+1),healsize,label='healthy number')
	plt.plot(range(1,total_time+1),immsize,label='immunized number, start t={}, immunized ratio={}'.format(markt,len(imm)/total_nodes_number))
	plt.xlabel('time')
	plt.ylabel('number of infected/healthy/immunized under probability p')
	plt.title('{} nodes, p={}, a={}, threshold={}'.format(total_nodes_number,prob,A,threshold))
	plt.legend(loc='best')
	plt.show()
run(total_nodes_number,prob,A,total_time,threshold)
