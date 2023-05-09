import os
		
if __name__ == '__main__':
	d = "./37thRilton"
	n = "37thRilton.pgn"
	f = open(n,'w')
	files = os.listdir(d)
	for file in files:
		for l in open(d+"/"+file):
			f.writelines(l)
	f.close()
		