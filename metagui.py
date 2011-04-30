from Tkinter import *
from tkMessageBox import showinfo
import os, sys, thread
from formtest import *
import metagoofil
#from widget import *
import ackSearcher

class MetaForm(FormTest):
	def __init__(self):
		root = Tk()
		root.title(self.title)
		labels = ['Domain', 'Limit', 'Filetype', 'Engine',
					'Output', 'LocalDir', 'Proxy', 'Level']
		FormTest.__init__(self, labels, root)
		self.mutex = thread.allocate_lock()
		self.threads = 0
	def metatest(self, argv):
		self.test(argv)
		
		self.mutex.acquire()
		self.threads = self.threads - 1
		self.mutex.release()
	def onSubmit(self):
		FormTest.onSubmit(self)
		domain = self.content['Domain'].get()
		limit = self.content['Limit'].get()
		#filetype = self.content['Filetype'].get()
		filetype = self.whatFiletype()
		output = self.content['Output'].get()
		localdir = self.content['LocalDir'].get()
		level = self.content['Level'].get()
		#engine = self.content['Engine'].get()
		proxy = self.content['Proxy'].get()
		engine = self.whichEngine()
		if engine == 'Google':
			engine = 'google.com'
		elif engine == 'Bing':
			engine = 'bing.com'
		elif engine == 'Yahoo!':
			engine = 'yahoo.com'
		elif engine == 'ACK':
			engine = 'ACK'
			#ack = 1
		print 'Engine\t=>\t', engine

		self.mutex.acquire()
		self.threads = self.threads + 1
		self.mutex.release()
		if engine != 'ACK':
			argv = ['-d', domain, '-l', limit, '-f',
			filetype, '-o', output, '-t', localdir, '-e', engine, '-p', proxy]
			targv = argv,
#			self.metatest(argv)
			thread.start_new_thread(self.metatest, targv)
		else:
			p = {}
			if proxy == '': p = {}
			else: p = {'http':'http://'+proxy}
			localdir='./' + localdir + '/'
			self.runAck(domain, filetype, limit, level, './robots.txt', 3, p, localdir)
	
	def runAck(self, *args):
		self.acktest(*args)
		
	def onCancel(self):
		if self.threads == 0:
			Tk().quit()
		else:
			showinfo(self.title, 'Cannot exit: %d threads running' % self.threads)

class MetaGetForm(MetaForm):
	title = 'Metagui'
	def test(self, argv):
		metagoofil.test(argv)
	def acktest(self, *args):
		ackSearcher.run(*args)

if __name__ == '__main__':
	MetaGetForm()
	mainloop()
