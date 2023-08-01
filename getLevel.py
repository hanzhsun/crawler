import requests
from requests.exceptions import RequestException
import threading
import random
import json
from time import sleep
from csv import DictWriter
import logging


dpath = './level/'
# tid = '44758719-2664-4c1c-89fb-e35cb72b2493'
tname = 'xvimagistral'
dt = dpath+tname
logging.basicConfig(filename=dt+'.log', level=logging.INFO)
glist = dt+"_l.txt"
pl = {}
level = {}

headers = {
	"Cookie": 'pvc_visits[0]=1690291503b6218; _gcl_au=1.1.2014855022.1690205104; _ga=GA1.1.884072037.1690205105; _ga_JF2WP22T0B=GS1.1.1690205104.1.0.1690205117.47.0.0; sid=s%3A7sFKIQrN9-d9ieZNGIbbXet4ndl_Qg61.Ug4SL%2BOMbI5DxTtIUdpGLZnc9A0IQdNYhB0nWuquprg; _ga_MJ3R6B59N3=GS1.1.1690205118.1.1.1690206091.0.0.0'
}

def parseP(l):
	player = {}
	gl = []
	for gid in l:
		game = l[gid]
		if ('whitePlayerRating' not in game) or ('blackPlayerRating' not in game):
			logging.info('No rating: '+game['whitePlayerFirstName']+' '+game['whitePlayerLastName']
				+' vs '+game['blackPlayerFirstName']+' '+game['blackPlayerLastName'])
			continue
		if ('whiteAnalyzedMoves' not in game) or ('blackAnalyzedMoves' not in game):
			logging.info('0 move: '+game['whitePlayerFirstName']+' '+game['whitePlayerLastName']
				+' vs '+game['blackPlayerFirstName']+' '+game['blackPlayerLastName'])
			continue
		if game['whiteAnalyzedMoves'] + game['blackAnalyzedMoves'] < 8:
			logging.info('<=7 moves: '+game['whitePlayerFirstName']+' '+game['whitePlayerLastName']
				+' vs '+game['blackPlayerFirstName']+' '+game['blackPlayerLastName'])
			continue
		gl.append(gid)
		wid = game['whitePlayerId']
		if wid not in player:
			player[wid] = {
				'rating': game['whitePlayerRating'],
				'name': game['whitePlayerFirstName']+' '+game['whitePlayerLastName'],
				'result': 0,
				'sum': game['whiteAnalyzedMoves'],
				'games': [gid]
			}
		else:
			player[wid]['games'].append(gid)
			player[wid]['sum'] += game['whiteAnalyzedMoves']

		bid = game['blackPlayerId']
		if bid not in player:
			player[bid] = {
				'rating': game['blackPlayerRating'],
				'name': game['blackPlayerFirstName']+' '+game['blackPlayerLastName'],
				'result': 0,
				'sum': game['blackAnalyzedMoves'],
				'games': [gid]
			}
		else:
			player[bid]['games'].append(gid)
			player[bid]['sum'] += game['blackAnalyzedMoves']

		match game['result']:
			case "1-0":
				player[wid]['result'] += 1
			case "0-1":
				player[bid]['result'] += 1
			case "1/2-1/2":
				player[bid]['result'] += 0.5
				player[wid]['result'] += 0.5

	with open(glist,'w') as f:
		f.write('\n'.join(gl))
	f.close()	
	with open(dt+'.json', 'w') as out:
		json.dump(player, out)
	out.close()

def getT(tid):
	url = f"https://tornelo.com/api/tournaments/{tid}/fair-play?gamesOnly=true"
	try:
		r = requests.get(url, headers=headers)
		if r.status_code == 200:
			print("Success")
			parseP(r.json()['games'])
		print(r.status_code)
	except RequestException as err:
		print(err)
		print("Fail")

def readList(file):
	with open(file) as f:
		l = f.readlines()
	l = [i.strip() for i in l]
	f.close()
	return l

def getG(gid):
	sleep(random.randint(1,5))
	url = f"https://tornelo.com/api/games/{gid}/engine-assessments?includePending=true"
	try:
		r = requests.get(url, headers=headers)
		if r.status_code == 200:
			a = r.json()['assessments']
			for i in a:
				level[i['blackPlayerId']][i['depth']][gid] = {
					'moves': i['blackAnalyzedMoves'],
					'cpl': i['blackCpl'],
					'mm': i['blackMm'] 
				}
				level[i['whitePlayerId']][i['depth']][gid] = {
					'moves': i['whiteAnalyzedMoves'],
					'cpl': i['whiteCpl'],
					'mm': i['whiteMm'] 
				}
			print(gid)
		print(r.status_code)
	except RequestException as err:
		print(err)
		print("Fail")

def getL(l):
	with open(dt+'.json', 'r') as f:
		pl = json.load(f)
	for pid in pl:
		level[pid] = {
			12:{},
			14:{},
			16:{},
			18:{}
		}
	threads = []
	for gid in l:
		t = threading.Thread(target=getG, args=(gid,))
		threads.append(t)
	for task in threads:
		task.start()
	for task in threads:
		task.join()
	with open(dt+'_g.json', 'w') as out:
		json.dump(level, out)
	out.close()

def genP(al,flag):
	with open(dt+'.json', 'r') as f:
		pl = json.load(f)
	with open(dt+'_g.json', 'r') as f:
		gdata = json.load(f)
	f.close()
	fp = []
	for pid in pl:
		player = pl[pid]
		for i in al:
			n = len(player['games'])
			if len(gdata[pid][str(i)]) < n:
				if flag == "NO":
					logging.info("NO "+player['name']+" "+str(i))
				continue
			if flag == "YES":
				if i == 16 or i == 18:
					logging.info("YES "+player['name']+" "+str(i))
			cpl = 0
			mm = 0
			for j in player['games']:
				if j not in gdata[pid][str(i)]: 
					if j not in gdata[pid][str(i+2)]:
						tmp = gdata[pid][str(i+4)][j]
					else:
						tmp = gdata[pid][str(i+2)][j]
				else:
					tmp = gdata[pid][str(i)][j]
				w = tmp['moves']/player['sum']
				cpl += float(tmp['cpl'])*w
				mm += float(tmp['mm'])*w
			match i:
				case 12:
					analysis = "A"
				case 14:
					analysis = "B"
				case 16:
					analysis = "C"
				case 18:
					analysis = "D"
			fp.append({
				'Name': player['name'],
				"Rating": player['rating'],
				"Games": n,
				"Result": player['result'],
				'Moves': player['sum'],
				'CPL': round(cpl),
				'MM': round(mm),
				'Sort Score': round(mm)-round(cpl),
				'Analysis': analysis
			})
	with open(dt+'.csv', 'w+', newline='') as out:
		writer = DictWriter(out, fieldnames=fp[0].keys())
		writer.writeheader()
		writer.writerows(fp)
	
if __name__ == '__main__':
	# getT(tid)

	# getL(readList(glist))

	genP([12,14,16,18],"NO") #yes for fics, no for master
	print("Finish")