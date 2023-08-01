import requests
import threading
from time import sleep

MAX_TEST_THREADS = 100

class TestThread(threading.Thread):
	def __init__(self, st):
		self.st = st
		super(TestThread, self).__init__()

	def run(self):
		self.st = [_ for _ in self.st if self.checkIP(_)]

	def checkIP(self, ip):
		proxy = {'https': "https://"+ip}
		try:
			requests.adapters.DEFAULT_RETRIES = 3
			r = requests.get("https://icanhazip.com/", timeout=100, proxies=proxy)
			p = r.text.strip()
			if p==ip.split(':')[0]:
				return True
			else:
				print(ip+"F")
				return False
		except:
			return False

def readList(file):
	with open(file) as f:
		l = f.readlines()
	l = [i.strip() for i in l]
	f.close()
	return l

if __name__ == '__main__':
	pf = "https_proxies.txt"
	pl = readList(pf)

	threads = []
	avg = int(len(pl) / MAX_TEST_THREADS)
	if len(pl) % MAX_TEST_THREADS != 0:
		avg+=1
	for i in range(MAX_TEST_THREADS):
		thread = TestThread(pl[i*avg:(i+1)*avg])
		threads.append(thread)
		thread.start()

	while threading.active_count() > 1:
		sleep(10)

	pl = []
	for t in threads:
		pl.extend(t.st)

	pl = set(pl)
	print(len(pl))
	with open("checkedS.txt",'w') as f:
		f.write('\n'.join(pl))
	f.close()