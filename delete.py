import os
		
if __name__ == '__main__':
	d = "./yzl"
	files = os.listdir(d)
	for file in files:
		if file.endswith('_*.txt'):
			try:
	 			os.remove(d+"/"+file)
			except FileNotFoundError:
				print(file)
				pass	