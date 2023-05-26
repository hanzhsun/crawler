import os
		
if __name__ == '__main__':
	d = "./master"
	n = "master.csv"
	f = open(n,'w')
	files = os.listdir(d)
	for file in files:
		for l in open(d+"/"+file):
			f.writelines(l)
		f.write("\n")
	f.close()
		