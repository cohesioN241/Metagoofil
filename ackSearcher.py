#Author : Chen
#Version : 0.1
#Class : ackSearcher
#
#Description : Looking into /robots.txt file in most sites. Be bad and find the "Disallow" links.
#				Going to these links, recursively with tunable child links and deepth. To find 
#				files with the types you can specify. Once you find one file, the program will
#				start a new thread to download it.
#Tricky Part : Thread synchronization, avoid duplicated download and also links, recursion
#				How to decide the # of limit and level and which links to search? Add some
#				kind of AI.

import urllib
import httplib
import re
import random
import socket
import thread
import time
import sys

class ackSearcher(object):
	#I think it's a simple but nice regex
	r1 = re.compile('href="(http://.{1,80}?)"')

	def __init__(self, url, type, limit=3, botfile='./robots.txt', timeout=3, proxy={}):
		self.childRex = self.r1
		self.site = url
		self.limit = limit
		#read the robots.txt
		self.badList = self.readBot(botfile)
		self.contentType = []
		self.contentType = type

		#initially intended to limit the time used to open urls
		socket.setdefaulttimeout(timeout)
		#two lists to avoid doing the same work twice
		self.filelist = []
		self.donelist = []

		self.proxy = proxy
		
		#thread stuffs
		self.mutex = thread.allocate_lock()
		self.threads = 0

	def readBot(self, botfile):
		abdir = []
		try:
			urllib.urlretrieve('http://'+self.site+'/robots.txt', botfile)
		except:
			print 'No robot file. You can use the handy engines.'
			exit(0)

		bot = open(botfile, 'r')
		for l in bot.readlines():
			print l
			try:
				allow, dir = l.split(':')[0].strip(), l.split(':')[1].strip()
			except:
				pass

			if allow.find('isa') > 0:
				dir =  'http://' + self.site + dir
				abdir.append(dir)
		print abdir
		return abdir

	def getUrl(self, dir):
		print 'Try URL : ' + dir
		try:
			h = httplib.HTTP(self.site)
				
			h.putrequest('GET', dir)
			h.putheader('Host', self.site)
			h.endheaders()
			returncode, returnmsg, headers = h.getreply()
			data = h.getfile().read()
			res = []
			file = []
			r = self.childRex.findall(data)
#			print 'who has : '
		
			if r != []:
				#filter same links
				r = filter(self.noDupLink, r)
				#get the file url and start a thread to do that
				file = filter(self.isContentType, r)
				file = filter(self.noDupFile, file)
				self.filelist.extend(file)
				map(self.download, file)

				#so, pass back only links	
				r = filter(self.isLink, r)
				#since there could be many links. So stupidly randomly get self.limit links
				if len(r) >= self.limit:
					num = random.randint(0,len(r)-1)
					for i in range(self.limit):
						res.append(r[(num+i)%len(r)])

#			for s in res: print s
			self.donelist.extend(res)
			return res
		except httplib.InvalidURL:
			print 'Nothing'
		except socket.timeout:
			print 'Time out'
			return []
		
	def isContentType(self, URLorFile):
	#Is it a file (as wanted)?
		for t in self.contentType:
			if URLorFile.find('.'+t) > -1:
				return True
		return False

	def isLink(self, URLorFile):
		return not self.isContentType(URLorFile)

	def play(self, lst, level=3):
	#It's neccessary to do the filter again since there could be
	#dups with the links found in other pages
		l = filter(self.noDupLink, lst)

		l = map(self.getUrl, lst)
		#now l is a list of lists
		l = self.flatten(l)
		#now it's not :)

		if level > 0:
			level = level - 1
			self.play(l, level)
		else:
			print 'Finished search with given deepth'
			print 'Here is Files found'
			for file in self.filelist: print file
	
	def flatten(self, list):
		ll = []
		for l in list:
			ll.extend(l)
		return ll
	
	def noDupLink(self, link):
		try:
			self.donelist.index(link)
			return False
		except ValueError:
			return True

	def noDupFile(self, link):
		try:
			self.filelist.index(link)
			return False
		except ValueError:
			return True

	def download(self, url):
		self.mutex.acquire()
		self.threads = self.threads + 1
		self.mutex.release()

		thread.start_new_thread(self.retrieve, (url,))
	
	def retrieve(self, url):
		filename = url.split('/')[-1]
		try:
			handler = urllib.urlopen(url, proxies = self.proxy)
			body = handler.read()
			handler.close()
			file = open('./temp/' + filename)
			file.write(body)
			file.close()

			print '\nDownloading => ', url, '\n'
		except: 
			print 'Fail to download : ', url
			pass

		self.mutex.acquire()
		self.threads = self.threads - 1
		self.mutex.release()
	
	def wait(self):
		while self.threads != 0:
			print 'Zzz... ',
			time.sleep(1)

if __name__ == '__main__':
	list = ['pdf','ppt','doc','jpg','txt']
	r = ackSearcher(sys.argv[1], list, limit=5)
	r.play(r.badList, level = 5)
	r.wait()
