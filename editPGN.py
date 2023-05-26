from chess import pgn

def fromS(a,s,n):
	file = open(a+".pgn")
	name = a+"_"+str(n)
	ns = s+n
	print(ns)
	for i in range(s,ns):
		g = pgn.read_game(file)
		w = g.headers['White']
		b = g.headers['Black']
		d = g.headers['Date']
		g.headers['White'] = w+" "+d
		g.headers['Black'] = b+" "+d
		g.headers['Round'] = str(i)
		print(g, file=open(name+".pgn", "a"), end="\n\n")
	print(name+"D!")
		
if __name__ == '__main__':
	a = "09-3"
	n = 670
	s = 1
	fromS(a,s,n)
	