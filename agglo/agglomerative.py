#! /usr/bin/python

import sys, math

#GLOBAL DICT TO MEMOIZE DISTANCES
distances = {}

def d(p1, p2):
	global distances
	ans = distances.get( (str(p1), str(p2)), False)
	if ans:
		return ans
	sum = 0
	for i in xrange(len(p1)):
		sum += (p1[i] - p2[i])**2
	distances[(str(p1), str(p2))] = math.sqrt(sum)
	distances[(str(p2), str(p1))] = distances[(str(p1), str(p2))]
	return distances[(str(p1), str(p2))]

def mean(c):
	mu = c[0]
	for i in xrange(1, len(c)):
		for j in xrange(len(mu)):
			mu[j] += c[i][j]

	for i in xrange(len(mu)):
		mu[i] = 1.0*mu[i]/len(c)

	return mu

def d1(c1, c2):
	min = d(c1[0], c2[0])
	for x1 in c1:
		for x2 in c2:
			temp = d(x1, x2) 
			if temp < min:
				min = temp
	return min

def d2(c1, c2):
	max = d(c1[0], c2[0])
	for x1 in c1:
		for x2 in c2:
			temp = d(x1, x2) 
			if temp > max:
				max = temp
	return max

def d3(c1, c2):
	n1 = len(c1)
	n2 = len(c2)
	sum = 0
	for x1 in c1:
		for x2 in c2:
			sum += d(x1, x2)
	return 1.0*sum/(n1*n2)

def d4(c1, c2):
	mu1 = mean(c1)
	mu2 = mean(c2)
	return d(mu1, mu2)

def agglomerative(data, no_of_clusters = 1, opt = 1):
	global distances
	distances = {}
	#INITIALIZE CLUSTERS
	clusters = []
	for each in data:
		clusters.append([each])

	#CHOOSE DIST FUNCTION
	fns = [d1, d2, d3, d4]
	f = fns[opt-1]
	print f

	total_clusters = len(data)
	while total_clusters != no_of_clusters:

		#FIND DIST B/W CLUSTERS
		nearest = []
		for i in xrange(len(clusters)):
			for j in xrange(len(clusters)):
				if i != j:
					nearest.append( (f(clusters[i], clusters[j]), i, j) )

		#MERGE CLOSEST CLUSTERS
		distance,i,j = min(nearest)
		rem = clusters[j]
		clusters[i].extend(clusters[j])
		clusters.remove(rem)
		total_clusters -= 1
		print total_clusters

	return clusters

if __name__ == "__main__":
	if len(sys.argv) != 2:
		print "Usage : python agglomerative.py <dataset>"
		sys.exit(1)
	f = open(sys.argv[1])
	raw_data = [each.strip('\n').strip('\r') for each in f.readlines()]
	data = [ [float(i) for i in each.split(',')] for each in raw_data[1:]]
	print agglomerative(data, 3, 1)
	print agglomerative(data, 3, 2)
	print agglomerative(data, 3, 3)
	print agglomerative(data, 3, 4)
