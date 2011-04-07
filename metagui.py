#!/usr/bin/python
from Tkinter import *
from tkMessageBox import showinfo
import os, sys, thread
from form import *
import metagoofil

class MetaForm(Form):
	def __init__(self):
		root = Tk()
		root.title(self.title)
		labels = ['Domain', 'Limit', 'Filetype',
					'Output', 'LocalDir', 'Engine', 'Proxy']
		modes = [('Google', 1), ('Bing', 2), ('Yahoo!', 3)]
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
		print 'Engine\t=>\t', engine

		self.mutex.acquire()
		self.threads = self.threads + 1
		self.mutex.release()
		argv = ['-d', domain, '-l', limit, '-f',
			filetype, '-o', output, '-t', localdir, '-e', engine, '-p', proxy]
		targv = argv,
#		self.metatest(argv)
		thread.start_new_thread(self.metatest, targv)
	def onCancel(self):
		if self.threads == 0:
			Tk().quit()
		else:
			showinfo(self.title, 'Cannot exit: %d threads running' % self.threads)

class MetaGetForm(MetaForm):
	title = 'Hi 141'
	def test(self, argv):
		metagoofil.test(argv)

if __name__ == '__main__':
	MetaGetForm()
	mainloop()
