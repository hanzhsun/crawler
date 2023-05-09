import requests
from requests.exceptions import RequestException
import threading
import random
from time import sleep

e = "37th Rilton Cup"
d = "./37thRilton/" 

def getUA():
	first = random.randint(55, 76)
	third = random.randint(0, 3800)
	fourth = random.randint(0, 140)
	os_type = [
		'(Windows NT 6.1; WOW64)', '(Windows NT 10.0; WOW64)', '(X11; Linux x86_64)',
		'(Macintosh; Intel Mac OS X 10_14_5)'
	]
	chrome_version = 'Chrome/{}.0.{}.{}'.format(first, third, fourth)
	ua = ' '.join(['Mozilla/5.0', random.choice(os_type), 'AppleWebKit/537.36',
		'(KHTML, like Gecko)', chrome_version, 'Safari/537.36'])
	return ua

def readList(file):
	with open(file) as f:
		l = f.readlines()
	l = [i.strip() for i in l]
	f.close()
	return l

def download(i,g,proxy):
	url = "http://old.chesstempo.com/requests/download_game_pgn.php?gameids="+g
	name = d+str(i)+"_"+g+".pgn"
	s = requests.Session()
	adapter = requests.adapters.HTTPAdapter(max_retries=5)
	s.mount('http://', adapter)
	flag = 0
	while flag == 0:
		headers = {
        	"User-Agent": getUA(),
    	}
		p = random.choice(proxy)
		proxies = {
			#'https': 'https://'+p,
			'http': 'http://'+p
    	}
		print(p)
		sleep(random.uniform(0.5, 1))
		r = s.get(url,headers=headers,proxies=proxies)
		if r.status_code == 200:
			if r.content != b'':
				with open(name,"wb") as pgn:
					pgn.write(r.content)
					pgn.close()
				flag = 1
			else:
				print(i, g, "F!")
		else:
			print(i, g, r.status_code)
	s.close()

def getPGN(gid,p):
	i = 0
	threads = []
	for g in gid:
		t = threading.Thread(target=download, args=(i,g,p))
		threads.append(t)
		i += 1
	for task in threads:
		task.start()
	for task in threads:
		task.join()

def getL(p):
	url = "http://old.chesstempo.com/requests/gameslist.php?" #https --> http
	data = {
		'startIndex': 0,
		'results': 500,
		'currentFen': "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
		'eventInput': e,
		'subsetMinRating': "all"	
	}
	headers = {
		"User-Agent": getUA()
	}
	print(headers)
	print(p)
	proxies = {
		#'https': 'https://'+p,
		'http': 'http://'+p
    }
	s = requests.Session()
	adapter = requests.adapters.HTTPAdapter(max_retries=5)
	s.mount('http://', adapter)
	try:
		r = s.post(url, data=data, headers=headers, proxies=proxies)
		if r.status_code == 200:
			print("Success")
			j = r.json()["result"]
			n = j["total_games"]
			g = j["games"]
			file = open("gid.txt",'w')
			for i in range(n):
				gid = str(g[i]['game_id'])
				file.write(gid+"\n")
			file.close()
			s.close()	
			return
		print(r.status_code)
		print(r.text)
		return
	except RequestException as err:
		print(err)
		print("Fail")
		return

		
if __name__ == '__main__':
	p = "checked.txt"
	proxy = readList(p)
	#getL(random.choice(proxy_list))
	l = "gid.txt"
	gid = readList(l)
	getPGN(gid,proxy)
	print("Finish")
		