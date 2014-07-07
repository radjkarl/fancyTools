# -*- coding: utf-8 -*-

#from pyqtgraph.pgcollections import OrderedDict
from ordereddict import OrderedDict


class NestedOrderedDict(OrderedDict):
	'''
	an ordered dict allowing the acces of nested items e.g.
	
	structure
	---------
	one
		two
		three
			four
	'''

	def __init__(self):
		super(NestedOrderedDict, self).__init__()
		self.path = ''

	#TODO: überarbeiten
	#def __getitem__(self, key):
		#if not key:
			#return self
		#if isinstance(key,str):
			#key = key.split(', ')
			#return self[key[0]].__getitem__(l[1:])
		#return self[key]


	def __setitem__(self, key, value):
		super(NestedOrderedDict, self).__setitem__(key, value)
		if isinstance(value,self.__class__):
			if self.path:
				value.path = self.path + ', ' + key
			else:
				value.path = key



	def __repr__(self):
		'''limit the number of shown items to 5 and give it a more dict-like view'''
		contents = ''
		n = 0
		for n, (key, item) in enumerate(self.iteritems()):
			contents += '%s: %s, ' %(key,item)
			if n == 5:
				break
		if contents:
			contents = contents[:-2]
		if n == 5:
			contents += ', ...'
		return '%s({%s})' %(self.__class__.__name__, contents)


if __name__ == '__main__':

	one = NestedOrderedDict()
	two = 'something'
	three = NestedOrderedDict()
	four = NestedOrderedDict()
	five = 'something else'

	#set items:
	one['2'] = two
	one['3'] = three
	three['4'] = four
	four['5'] = five

	#get items:
	print one
	print four.path
#	print one['2, 3']
