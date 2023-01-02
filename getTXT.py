import requests
from requests.exceptions import RequestException
from lxml import etree
import random
import math

headers = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54',
]

def get_page(url,host,c):
	try:
		header = {
			'Cookie': c,	
			'Host': host,	
			'User-Agent': random.choice(headers),	
		}
		r = requests.get(url, headers=header)
		if r.status_code == 200:
			#r.encoding = 'utf-8'
			r = r.content
			return etree.HTML(r)
		print(r.status_code)
		return 1
	except RequestException:
		print("Fail")
		return None

def get_page_r(url,host,c,ref):
	try:
		header = {	
			'Cookie': c,	
			'Host': host,
			'Referer': ref,	
			'User-Agent': random.choice(headers),	
			'X-Requested-With': 'XMLHttpRequest',
		}
		r = requests.get(url, headers=header)
		if r.status_code == 200:
			r = r.content
			return etree.HTML(r.decode('utf-8'))
		print(r.status_code)
		return 1
	except RequestException:
		print("Fail")
		return None

def getJ(bid,e): #获取免费章节
	host = "www.jjwxc.net"
	for i in range(1,e+1):
		url = "http://www.jjwxc.net/onebook.php?novelid="+bid+"&chapterid="+str(i)
		html = get_page(url,host,'')
		text = str(i)+"."
		if html == 1:
			text = text+"获取失败\n"
			print(text)
		else:
			title = html.xpath('//h2/text()')
			if len(title)==0:
				text = text+"获取失败\n"
				print(text)
			else:
				print(text)
				context = html.xpath('//div[@class="noveltext"]/text()')
				text = text+title[0]+"\n"+'\n'.join(context[4:-4])
		with open("./tmp.txt","a") as f:
			f.write(text+"\n")
		
#def getL():
		
def getP(bid,e,c): #获取免费和已购买章节
	host = "www.po18.tw"
	p = math.ceil(e/100)
	for j in range(1,p+1):
		link = "https://www.po18.tw/books/"+bid+"/articles?page="+str(j)
		print("Page"+str(j))
		lhtml = get_page(link,host,c)
		if lhtml == 1:
			print("章回列表获取失败")
		else:
			chapter = lhtml.xpath('//a[@class="btn_L_blue"]/@href')
			counter = lhtml.xpath('//a[@class="btn_L_blue"]/../../div[@class="l_counter"]/text()')
			for i in range(0,len(chapter)):
				print(i)
				print(counter[i])
				ref = "https://www.po18.tw"+chapter[i]
				url = 'https://www.po18.tw'+'articlescontent'.join(chapter[i].split('articles'))
				text = counter[i]+"."
				html = get_page_r(url,host,c,ref)
				if html == 1:
					text = text+"获取失败\n"
					print(text)
				else:
					print(text)
					title = html.xpath('//h1/text()')
					print(title[0])
					context = html.xpath('//p/text()')
					text = text+title[0]+"\n\n"+'\n'.join(context)+"\n\n"
					text = text.replace(u'\xa0','')
				with open("./tmp1.txt","a", encoding='utf-8') as f:
					f.write(text)
		
if __name__ == '__main__':
	#getJ("6301310",88)
	getP("698163",10,'') #cookie
	print("结束")
	input()
		