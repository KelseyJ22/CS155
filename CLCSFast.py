# All strings will consist solely of uppercase letters from the English alphabet.
# All strings will be of length at most 2000 (you may use this fact to preallocate your arrays).
# We also will only require that you output the length of CLCS, not the subsequence itself.

import sys
import numpy as np

# Here, SINGLESHORTESTPATH(A,B,m, pl, pu) computes pm by running the DP on the table
# bounded by pl and pu. Finally, to solve the full problem, we call FINDSHORTESTPATHS(A,B, p,0,m),
# then return the common subsequence associated with the shortest pi.

arr = np.zeros((2048, 2048), dtype=int)

def LCS(A,B):
	m = len(A)
	n = len(B)

	for i in range(1,m+1):
		for j in range(1,n+1):
			if A[i-1] == B[j-1]:
				arr[i][j] = arr[i-1][j-1]+1
			else:
				arr[i][j] = max(arr[i-1][j], arr[i][j-1])

	return arr[m][n]


def FindShortestPaths(A, B, p, l, u):
	if(u-l <= 1) return 1 # TODO: check this
	mid = (l+u)/2
	p[mid] = SingleShortestPath(A, B, mid, p[l], p[u])
	FindShortestPaths(A,B, p,l,mid)
	FindShortestPaths(A,B, p,mid,u)

def SingleShortestPath(A, B, m, pl, pu):	
	pass

def CLCS(A, B):
	FindShortestPaths(A, B, p, 0, len(A)) # TODO: what's p?

def main():
	if len(sys.argv) != 1:
		sys.exit('Usage: `python LCS.py < input`')
	
	for l in sys.stdin:
		A,B = l.split()
		print LCS(A,B)
	return

if __name__ == '__main__':
	main()