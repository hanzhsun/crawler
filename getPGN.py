import requests
from requests.exceptions import RequestException
import threading
import random
import json
from time import sleep

e = "Balatonbereny open"
d = "./bala/" 

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

def parsePGN(i,g):
	print(i)
	match g['result']:
		case 'd':
			r = "1/2-1/2"
		case 'w':
			r = "1-0"
		case other:
			r = "0-1"
	pgn = "[Event \""+g['event']+"\"]\n[Site \""
	pgn += g['site']+"\"]\n[Round \""
	#pgn += g['round']+"\"]\n[Date \""
	pgn += i+"\"]\n[Date \"" # for tornelo website
	pgn += g['date']+"\"]\n[White \""
	pgn += g['white']+"\"]\n[Black \""
	pgn += g['black']+"\"]\n[WhiteElo \""
	pgn += str(g['elowhite'])+"\"]\n[BlackElo \""
	pgn += str(g['eloblack'])+"\"]\n[Result \""
	pgn += r+"\"]\n\n"
	pgn += " ".join(g['moves_san'])
	pgn += "  "+r+"\n"
	with open(d+i+"_"+str(g['game_id'])+".pgn","w") as f:
		f.write(pgn)
	f.close()

def getL(p):
	url = "http://old.chesstempo.com/requests/gameslist.php?" #https --> http
	data = {
		'startIndex': 0,
		'results': 500,
		'currentFen': "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
		#'yearMax': 1990,
		'eventInput': e,
		'subsetMinRating': "all"	
	}
	headers = {
		"User-Agent": getUA()
	}
	print(p)
	proxies = {
		'http': 'http://'+p
    }
	try:
		r = requests.post(url, data=data, headers=headers, proxies=proxies)
		if r.status_code == 200:
			print("Success")
			j = r.json()["result"]
			n = j["total_games"]
			g = j["games"]
			'''
			with open("result.json",'w') as f:
				json.dump(g,f)
			f.close()
			'''
			threads = []
			for i in range(n):
				t = threading.Thread(target=parsePGN, args=(str(i+1),g[i]))
				threads.append(t)
			for task in threads:
				task.start()
			for task in threads:
				task.join()
		print(r.status_code)
	except RequestException as err:
		print(err)
		print("Fail")

		
if __name__ == '__main__':
	p = "checked.txt"
	proxy = readList(p)
	getL(random.choice(proxy))
	print("Finish")
		