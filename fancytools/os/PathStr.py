# -*- coding: utf-8 -*-
import os
import shutil


class PathStr(str):
	'''
	**os.path** and **shutil** wrapper for the rest of us
	... copy, move, remove, paste, rename, iterating, tree printing etc.
	
	create a path via::
	
		p = PathStr('MY_PATH')
	
	copy::
	
		dst = p.copy('MY_DEST')
	
	all outputs are returned as PathStr - also dst
	
	list all files in a folder::
		
	for f in p:
		print f
	
	
	'''


	#WRAPPED OS.PATH METHODS
	def join(self, *args):
		return PathStr(os.path.join(self,*args))

	def exists(self):
		return os.path.exists(self)

	def abspath(self):
		return PathStr(os.path.abspath(self))

	def dirname(self):
	#	if os.path.isdir(self):
	#		return self
		return PathStr(os.path.dirname(self))

	def basename(self):
		return PathStr(os.path.basename(self))

	def isfile(self):
		return os.path.isfile(self)


	def isdir(self):
		return os.path.isdir(self)

	#EXTENDED OS.PATH / SHUTIL METHODS

	def listdir(self):
		if os.path.isdir(self):
			d = self
		else:
			d = os.path.dirname(self)
		return os.listdir(d)


	def mkdir(self, dname):
		n = self.join(dname)
		if not n.exists():
			os.mkdir(n)
		return n

	#NEW THINGS

	@staticmethod
	def home():
		return PathStr(os.path.expanduser("~"))

#	@staticmethod
#	def curdir():
#		return PathStr(os.curdir)

	def load(self, size):
		if os.path.exists(self):
			return eval( open(self).read(size) )

	def copy(self, dst, override=False):
		'''copy self to a given destination - return copy as PatStr'''
		p = PathStr(dst)
		if p.exists() and p.isfile():
			if not self.isfile():
				raise IOError("cannot copy folder '%s' into given file '%s'"
					%(self,dst))
			if not override:
				raise IOError("overriding destination is not allowed by given argument 'override'")
			p = p.join(self.basename)# dst if only the containg folder, so
									 # join this with the basename of self
			
		if self.isfile():
			shutil.copy2(self, dst)
		else:
			shutil.copytree(self, dst)
		return p



	def move(self, dst):
		shutil.move(self, dst)
		self = PathStr(dst).join(self.basename())
		return self


	def remove(self, name=None):
		f = self
		if name:
			f = self.join(name)
		try:
			os.remove(f)
		except OSError:
			os.rmdir(f)


	def filetype(self):
		if '.' in self:
			return self.split('.')[-1]
		return ''


	def __iter__(self):
		'''makes the class iterable'''
		#TODO: iter and listdir as generator object
		if self.exists():
			return iter(self.listdir())
		return iter([])


	def parentDir(self):
		'''returns the parent directory the PathStr'''
		
		p = self.abspath().dirname()
		if self.isfile():
			return p.dirname()
		return p


	def tree(self, max_depth_level=3):
		'''return a file structure tree'''
		s = ''
		from fancytools.os import osWalkLimited # import here to get the function and not the module

		for root, dirs, files in osWalkLimited(self, max_depth_level):
			level = root.replace(self, '').count(os.sep)
			indent = ' ' * 4 * (level)
			s += '\n{}{}/'.format(indent, os.path.basename(root))
			subindent = ' ' * 4 * (level + 1)
			for f in files:
				s += '\n{}{}'.format(subindent, f)
		return s[1:]
	

if __name__ == '__main__':
	print PathStr(os.curdir).tree()
	#p = PathStr('/home/karl/test')
	#u = p.parentDir().join(p+'_master')
	#print u
	#p.copy(u)



	#def __iter__(self):
		##TODO: iter and listdir as generator object
		#self._n = -1
		#if self.exists():
			#self._l = self.listdir()
		#else:
			#self._l =[]
		#return self
##			return os.walk(self.dirname())



	#def next(self):
		#self._n += 1
		#return self._l[self._n]
		#