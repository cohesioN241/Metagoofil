#!/usr/bin/python
from Tkinter import *
from tkMessageBox import showinfo
import os, sys, thread
from form import *
import metagoofil
#from widget import *
import ackSearcher

class MetaForm(Form):
	def __init__(self):
		root = Tk()
		root.title(self.title)
		labels = ['Domain', 'Limit', 'Filetype',
					'Output', 'LocalDir', 'Proxy', 'Level']
		modes = [('Google', 1), ('Bing', 2), ('Yahoo!', 3), ('ACK', 4)]
		Form.__init__(self, labels, modes, root)
		self.mutex = thread.allocate_lock()
		self.threads = 0
	def metatest(self, argv):
		self.test(argv)
		
		self.mutex.acquire()
		self.threads = self.threads - 1
		self.mutex.release()
	def onSubmit(self):
		Form.onSubmit(self)
		domain = self.content['Domain'].get()
		limit = self.content['Limit'].get()
		filetype = self.content['Filetype'].get()
		output = self.content['Output'].get()
		localdir = self.content['LocalDir'].get()
		level = self.content['Level'].get()
		#engine = self.content['Engine'].get()
		proxy = ''
		if self.useProxy() == 1:
			proxy = self.content['Proxy'].get()
			print "Using proxy: " + proxy
		engine = self.whichEngine()
		if engine == 1:
			engine = 'google.com'
		elif engine == 2:
			engine = 'bing.com'
		elif engine == 3:
			engine = 'yahoo.com'
		elif engine == 4:
			engine = 'ACK'
			ack = 1
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
#		self.progressbar()
#		self.update_progress()
	
	def runAck(self, *args):
		self.acktest(*args)
		
		
	def progressbar(self):
		t = Tk()
		self.progval = IntVar(t)
		progmsg = StringVar(t); progmsg.set("Compute in progress...")
		b = Button(t, relief=LINK, text="Quit (using bwidget)", command=t.destroy)
		b.pack()
		t.withdraw()
		self.c = ProgressDialog(t, title="Please wait...",
		                   type="infinite",
		                   width=20,
		                   stop="Stop",
		                   textvariable=progmsg,
		                   variable=self.progval,
		                   command=lambda: self.c.destroy()
		                   )
	
	def update_progress(self):
		self.progval.set(2)
		self.c.after(20, self.update_progress)
		
	def onCancel(self):
		if self.threads == 0:
			Tk().quit()
		else:
			showinfo(self.title, 'Cannot exit: %d threads running' % self.threads)

class MetaGetForm(MetaForm):
	title = 'Hi 141'
	def test(self, argv):
		metagoofil.test(argv)
	def acktest(self, *args):
		ackSearcher.run(*args)

if __name__ == '__main__':
	MetaGetForm()
	mainloop()
