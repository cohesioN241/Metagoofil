# a reusable form class, used by getfilegui (and others)

from Tkinter import *
import Image, ImageTk
entrysize = 40

class FormTest:                                           # add non-modal form box
    def __init__(self, labels, parent=None):          # pass field labels list
	#box = Frame(parent)
        self.content = {}
	Label(text='Metagui', font=("Helvetica", 24)).grid(row=0, column=1, sticky=W+E)
	Label(text='', width=7).grid(row=0, column=2)
	r = 1
	self.filetype = StringVar()
	self.engine = StringVar()
        for label in labels:
        	Label(text=label, width=7).grid(row=r, column=0)
		if label=='Filetype':
			self.filetype.set('all')
			OptionMenu(parent, self.filetype, 'all','pdf','doc','xls','ppt','sdw','mdb','sdc','odp','ods','docx','xlsx','pptx', 'zip').grid(row=r, column=1, sticky=W)
		elif label=='Engine':
			self.engine.set('Google')
			OptionMenu(parent, self.engine, 'Google', 'Bing', 'Yahoo!', 'ACK').grid(row=r, column=1, sticky=W)
		else:
        		entry = Entry(width=entrysize)
			entry.grid(row=r, column=1, sticky=W)
        		self.content[label] = entry
		r = r+1
		if label=='Domain':
			Label(text='example: microsoft.com').grid(row=r, column=1, sticky=W)
		elif label=='Limit':
			Label(text='# of files you wish to retrieve').grid(row=r, column=1, sticky=W)
		elif label=='Filetype':
			Label(text='filetype you wish to search for').grid(row=r, column=1, sticky=W)
		elif label=='Engine':
			Label(text='search engine you wish to use').grid(row=r, column=1, sticky=W)
		elif label=='Output':
			Label(text='example: microsoft.html').grid(row=r, column=1, sticky=W)
		elif label=='LocalDir':
			Label(text='example: microsoft-files').grid(row=r, column=1, sticky=W)
		elif label=='Proxy':
			Label(text='example: 75.64.56.207:41277').grid(row=r, column=1, sticky=W)
		elif label=='Level':
			Label(text='for ACK only. specify depth of search').grid(row=r, column=1, sticky=W)
		r = r+1
	Button(text='Cancel', command=self.onCancel).grid(row=r, column=1, sticky=E)
	Button(text='Submit', command=self.onSubmit).grid(row=r, column=2, sticky=E)
        #box.master.bind('<Return>', (lambda event, self=self: self.onSubmit()))

    def whichEngine(self):
	return self.engine.get()

    def whatFiletype(self):
	return self.filetype.get()

    def onSubmit(self):                                      # override this
        for key in self.content.keys():                      # user inputs in 
            print key, '\t=>\t', self.content[key].get()     # self.content[k]

    def onCancel(self):                                      # override if need
        Tk().quit()                                          # default is exit

class DynamicForm(FormTest):
    def __init__(self, labels=None):
        import string
        labels = string.split(raw_input('Enter field names: '))
        FormTest.__init__(self, labels)
    def onSubmit(self):
        print 'Field values...'
        FormTest.onSubmit(self)           
        self.onCancel()              
        
if __name__ == '__main__':
    import sys
    if len(sys.argv) == 1:
        FormTest(['Name', 'Age', 'Job'])     # precoded fields, stay after submit
    else:
        DynamicForm()                    # input fields, go away after submit
    mainloop()    
