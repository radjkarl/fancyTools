# -*- coding: utf-8 -*-
'''
Execuce all py-scripts in the current module.
'''
if __name__ == '__main__':
	from fancytools.pystructure import runAllInDir
	import os
	
	runAllInDir(os.path.abspath(os.curdir))
	