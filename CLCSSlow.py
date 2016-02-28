# all strings will consist solely of uppercase letters
# all strings will be of length at most 2000
# output the length of CLCS, not the subsequence itself

import sys
import numpy as np

# find the longest LCS(cut(A, k), cut(B,0)) over all possible choises of k

arr = np.zeros((2048, 2048), dtype=int)

# starter code
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


def cut(A, k):
	return A[k:] + A[:k] # reorder the string


def CLCS(A,B):
	longest = 0
	for k in range(0,len(A)): # try all values of k
		length = LCS(cut(A, k),B)
		if length >= longest:
			longest = length # track longest subsequence
	return longest


def main():
	if len(sys.argv) != 1:
		sys.exit('Usage: `python LCS.py < input`')
	
	for l in sys.stdin:
		A,B = l.split()
		print CLCS(A,B)
	return

if __name__ == '__main__':
	main()