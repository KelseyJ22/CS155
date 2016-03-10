# All strings will consist solely of uppercase letters from the English alphabet.
# All strings will be of length at most 2000 (you may use this fact to preallocate your arrays).
# We also will only require that you output the length of CLCS, not the subsequence itself.

import sys
import numpy as np

DIAG = 1
UP = 2
LEFT = 3
longest = 0

dp_tables = {}
paths = {}


def clearDPSector(mid, l, u, m, n):
	global dp_tables
	global paths

	COL_MIN = 0
	COL_MAX = 1

	row = mid
	next_start_col = 1
	while row < mid+m:
		col = next_start_col # Set col to appropriate starting value for next row
		while col <= n:
			if isValidPos(row, col, l, u):
				dp_tables['c'][row,col] = 0
				dp_tables['bp'][row,col] = 0
			else:
				break
			if isOnPath(u, row, col):
				next_start_col = col
			col += 1

		if next_start_col <= n:
			if (row+1) > paths[u-1, next_start_col-1, COL_MAX]:
				next_start_col += 1
		row += 1

# Here, SINGLESHORTESTPATH(A,B,m, pl, pu) computes pm by running the DP on the table
# bounded by pl and pu. Finally, to solve the full problem, we call FINDSHORTESTPATHS(A,B, p,0,m),
# then return the common subsequence associated with the shortest pi.

def isValidPos(row, col, l, u):
	global paths
	COL_MIN = 0
	COL_MAX = 1
	if row >= paths[l-1][col-1][COL_MIN] and row <= paths[u-1][col-1][COL_MAX]:
		return True
	else:
		return False

def isOnPath(path, row, col):
	global paths
	COL_MIN = 0
	COL_MAX = 1
	if row <= paths[path-1][col-1][COL_MAX] and row >= paths[path-1][col-1][COL_MIN]:
		return True
	else:
		return False

def SingleShortestPath(A, B, mid, l, u):
	#find shortest path bounded by p_l and p_u
	global DIAG
	global UP
	global LEFT
	global dp_tables
	global paths
	COL_MIN = 0
	COL_MAX = 1
	m = len(A)
	n = len(B)

	#DEBUG
	# print "PATHCHECK"
	# print "L: ", paths[l]
	# print "U: ", paths[u]
	print "---------"

	row = mid
	next_start_col = 1
	while row < mid+m:
		col = next_start_col # Set col to appropriate starting value for next row
		while col <= n:

			#DEBUG:
			print "[", row, ",", col, "]"
			if isValidPos(row, col, l, u):
				print "valid"
				#DEBUG
				# print "3"
				# print "row", row
				# print "col", col
				# print "NSC", next_start_col
				# print "----"
				mod_row = (row - m) if row > m else row
				if A[mod_row - 1] == B[col-1]:
					dp_tables['c'][row,col] = dp_tables['c'][row-1, col-1] + 1
					dp_tables['bp'][row,col] = DIAG
				elif dp_tables['c'][row-1, col] >= dp_tables['c'][row, col-1]:
					dp_tables['c'][row,col] = dp_tables['c'][row-1, col]
					dp_tables['bp'][row,col] = UP
				else:
					dp_tables['c'][row,col] = dp_tables['c'][row, col-1]
					dp_tables['bp'][row,col] = LEFT

				#DEBUG
				print "C table:"
				print dp_tables['c']
			else:
				break
			if isOnPath(u, row, col):
				next_start_col = col
			col += 1

		# set next row and column
		if next_start_col <= n:
			if (row+1) > paths[u-1, next_start_col-1, COL_MAX]:
				next_start_col += 1
		row += 1

	# #DEBUG:
	# print "OUT OF THE WHILES"
	# # At end of iteration, record path attributes and clear DP tables
	addPath(mid, m, n)
	# print "finished addPath()"
	updateLongest(mid+m-1, n)
	# print "finished updateLongest()"
	clearDPSector(mid, l, u, m, n) #TODO: add args
	# print "finished clearDPSector()"


def FindShortestPaths(A, B, l, u):
	#DEBUG
	global dp_tables
	if(u-l <= 1):
		return
	mid = (l+u)/2
	#DEBUG
	# print "||||||||||||||||||"
	# print "l: ", l
	# print "u: ", u
	# print "m: ", mid
	#print "C: "
	#print dp_tables['c']
	#print "MID: ", mid
	SingleShortestPath(A, B, mid, l, u)
	FindShortestPaths(A, B, l, mid)
	FindShortestPaths(A, B, mid, u)


#TODO: edit this for proper indices
def addPath(source_row, m, n):
	global dp_tables
	global paths
	COL_MIN = 0
	COL_MAX = 1
	row = m - 1 + source_row
	col = n
	while col > 0 and row >= source_row:
		#record this node in the path
		#DEBUG
		#print "PATHS:"
		#print paths
		#print "------------"
		if paths[source_row-1, col-1, COL_MAX] <= 0:
			paths[source_row-1, col-1, COL_MIN] = row
			paths[source_row-1, col-1, COL_MAX] = row
		elif paths[source_row-1, col-1, COL_MAX] > 0 and row < paths[source_row-1, col-1, COL_MIN]:
			paths[source_row-1, col-1, COL_MIN] = row
		#backtrace to next node
		if dp_tables['bp'][row, col]:
			if dp_tables['bp'][row, col] == 1:
				row -= 1
				col -= 1
			elif dp_tables['bp'][row, col] == 2:
				row -= 1
			elif dp_tables['bp'][row, col] == 3:
				col -= 1
			else: #should never reach this point
				print "!!!!!!!!!!!!!!! ERROR !!!!!!!!!!!!!!!!"
				print "Invalid back pointer"
		else: #TODO: what should the else be here? perhaps it should trace all the way back to the source node?
			#TODO: the issue here is whether or not the bp's need to be set up along the edges of the graph
			break

def addPathM(m, n):
	global paths
	COL_MIN = 0
	COL_MAX = 1
	for col in range(0, n):
		paths[m, col, COL_MIN] = paths[0, col, COL_MIN] + m
		paths[m, col, COL_MAX] = paths[0, col, COL_MAX] + m

def updateLongest(row_idx, col_idx):
	global dp_tables
	global longest
	#DEBUG
	print "longest"
	#print row_idx, col_idx
	#print dp_tables['c']
	#print dp_tables['c'][row_idx, col_idx]
	print longest
	if dp_tables['c'][row_idx, col_idx] > longest:
		longest = dp_tables['c'][row_idx, col_idx]


# In bp[][], values are 1, 2, or 3. 0 indicates no back pointer.
# 1 = diagonal back pointer
# 2 = up back pointer
# 3 = left back pointer
def createDPTable(A, B):
	global DIAG
	global UP
	global LEFT
	# global m
	# global n
	m = len(A)
	n = len(B)

	c = np.zeros(((2*m)+1, n+1), dtype=int)
	bp = np.zeros(((2*m)+1, n+1), dtype=int)
	for i in range(1, m):
		for j in range(1, n):
			if A[i] == B[j]:
				c[i,j] = c[i-1, j-1] + 1
				bp[i,j] = DIAG
			elif c[i-1, j] >= c[i, j-1]:
				c[i,j] = c[i-1, j]
				bp[i,j] = UP
			else:
				c[i,j] = c[i, j-1]
				bp[i,j] = LEFT
	return {'c':c, 'bp':bp}


def CLCS(A, B):
	global dp_tables
	global paths
	global longest
	m = len(A)
	n = len(B)

	paths = np.zeros((m+1, n, 2), dtype=int) # m+1 paths because need p_0 / p_m duplicate bounding paths
	dp_tables = createDPTable(A, B) #Time: 7mn
	#DEBUG
	# print dp_tables['c']
	# print dp_tables['bp']

	updateLongest(m-1, n-1)
	addPath(1, m, n)
	addPathM(m, n)
	c = np.zeros(((2*m)+1, n+1), dtype=int)
	bp = np.zeros(((2*m)+1, n+1), dtype=int)
	dp_tables = {'c':c, 'bp':bp} #equivalent to calling clearDPSector() at this level

	FindShortestPaths(A, B, 1, len(A)+1)

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