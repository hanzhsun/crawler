import requests
from requests.exceptions import RequestException
from lxml import etree
import random
import math
import re

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
		return 1

def get_page_s(path,host):
	try:
		header = {
			'authority': host,
			'path': '/lyd47299/2734821.html',
			'scheme': 'https',	
			'user-agent': random.choice(headers),	
		}
		r = requests.get("https://"+host+path, headers=header)
		if r.status_code == 200:
			#r.encoding = 'utf-8'
			r = r.content
			return etree.HTML(r)
		print(r.status_code)
		return 1
	except RequestException:
		print("Fail")
		return None

def getD(bid,e): #顶点小说
	host = "www.dingdianorg.com"
	b = 2734819
	for i in range(1,e+1):
		path = '/'+bid+'/'+str(i+b)+'.html'
		html = get_page_s(path,host)
		text = ""
		if html == 1:
			text = text+"获取失败\n"
			print(text,end='',flush=True)
		else:
			title = html.xpath('//h1/text()')
			if len(title)==0:
				text = text+"获取失败\n"
				print(text,end='',flush=True)
			else:
				print(str(i),end='.',flush=True)
				context = html.xpath('//div[@class="showtxt"]/text()')
				text = text+title[0]+"\n"+'\n'.join(context[:-2])+"\n"
		with open("./tmp.txt","a") as f:
			f.write(text+"\n")

def getJ(bid,e): #获取免费章节
	host = "www.jjwxc.net"
	for i in range(1,e+1):
		url = "http://www.jjwxc.net/onebook.php?novelid="+bid+"&chapterid="+str(i)
		html = get_page(url,host,'')
		#text = str(i)+"."
		text = ""
		if html == 1:
			text = text+"获取失败\n"
			print(text,end='',flush=True)
		else:
			title = html.xpath('//h2/text()')
			if len(title)==0:
				text = text+"获取失败\n"
				print(text,end='',flush=True)
			else:
				print(text,end='',flush=True)
				context = html.xpath('//div[@class="noveltext"]/text()')
				text = text+title[0]+"\n"+'\n'.join(context[4:-4])+"\n"
		with open("./tmp.txt","a") as f:
			f.write(text+"\n")
		
#def getL():

def getChapter(lhtml,host,c):
	chapter = lhtml.xpath('//a[@class="btn_L_blue"]/@href')
	counter = lhtml.xpath('//a[@class="btn_L_blue"]/../../div[@class="l_counter"]/text()')
	alltext = ''
	i = 0
	while i < len(chapter):
		ref = "https://www.po18.tw"+chapter[i]
		url = 'https://www.po18.tw'+'articlescontent'.join(chapter[i].split('articles'))
		text = counter[i]+"."
		html = get_page_r(url,host,c,ref)
		if html == 1:
			text = text+"获取失败\n"
			print(text,end='',flush=True)
		else:
			print(text,end='',flush=True)
			title = html.xpath('//h1/text()')
			context = html.xpath('//p/text()')
			text = text+title[0]+"\n\n"+'\n'.join(context)+"\n\n"
			text = text.replace(u' \xa0 ','')
			alltext = alltext+text
			i = i+1
	return alltext
		
def getP(b,c): #获取免费和已购买章节
	host = "www.po18.tw"
	print("Page1.",end='',flush=True)
	bhtml = get_page(b+"/articles",host,c)
	if bhtml == 1:
		print("获取失败")
	else:
		name = bhtml.xpath('//h1/text()')
		author = bhtml.xpath('//h2/a/text()')
		file = name[0]+"by"+author[0]
		text = getChapter(bhtml,host,c)
		status = bhtml.xpath('//dd/span/text()')
		with open("./"+file+".txt","w", encoding='utf-8') as f:
			f.write(file+" "+status[0]+"\n\n"+text)
		num = re.findall(r'\d+',status[0])
		p = math.ceil(int(num[0])/100)
		for j in range(2,p+1):
			link = b+"/articles?page="+str(j)
			print("Page"+str(j)+".",end='',flush=True)
			lhtml = get_page(link,host,c)
			if lhtml == 1:
				print("获取失败")
			else:
				ntext = getChapter(lhtml,host,c)
				with open("./"+file+".txt","a", encoding='utf-8') as f:
					f.write(ntext)
		
if __name__ == '__main__':
	b = 
	c = 
	getP(b,c) #cookie
	print("结束")
	input()
		