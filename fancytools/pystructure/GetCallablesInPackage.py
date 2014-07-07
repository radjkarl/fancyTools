'''
Created on 3 Jul 2014

@author: elkb4
'''
import fancytools
from fancytools.fcollections import NestedOrderedDict
import inspect


class GetCallablesInPackage(NestedOrderedDict):
    '''
    *exclude 'private' modules beginning with '_'
    '''
    def __init__(self, mainModule, modules_in_structure=False, 
                 include_classes=True, include_functions=False, 
                 max_level=None, del_empty_pck=True):
        NestedOrderedDict.__init__(self)
        self._include_classes = include_classes
        self._include_functions = include_functions

        self._mainmod = mainModule
        self._modules_in_structure = modules_in_structure
        self._max_level = max_level
        self._objects = [mainModule]
        
        self._buildLimitsRecursive(mainModule, self, 0)
        
        if del_empty_pck:
            self._cleanRecursive(self)
      
            
    def _cleanRecursive(self, subSelf):
        '''
        delete all NestedOrderedDict that haven't any entries
        '''
        for key, item in subSelf.iteritems():
            if isinstance(item, NestedOrderedDict):
                if not item:
                    subSelf.pop(key)
                else:
                    self._cleanRecursive(item)
            
    
    
    def _buildLimitsRecursive(self, module, subSelf, level):

        for (name, obj) in inspect.getmembers(module):
            # take only 'public' modules
            if name[0] == '_':
                continue
           # print name, level
            if inspect.ismodule(obj):
                #don't handle modules thats have been used before:
                if obj in self._objects:
                    continue
                self._objects.append(obj)

                if obj.__name__.startswith(self._mainmod.__name__):
                    #either use module for submenus or check whether module is actually a package:
                    if self._modules_in_structure or obj.__file__.endswith('__init__.pyc'):
                      #  is_pck = True
                      #  #limit max recursion level
                        if not self._max_level or level <= self._max_level:
                        #if self._max_level:
                            l = subSelf[name] = NestedOrderedDict()
                            self._buildLimitsRecursive(obj, l, level+1)
                    else:
                        #use same menu for all classes of all files on one folder/module
                        self._buildLimitsRecursive(obj, subSelf, level)
                    
            else: 
                    # if object is a class 
                    if ( not self._include_classes or ( self._include_classes and inspect.isclass(obj) ) or 
                    # and/or a function 
                       ( not self._include_functions or ( self._include_functions and inspect.isfunction(obj)) ) ):
                        # if object belongs to its parent module (mod is not imported)
                        # OR module paths are the same (in case of from mod import cls and cls.name == mod.name)
                        if obj.__module__ == module.__name__ or obj.__module__.startswith(module.__name__):
                            subSelf[name] = obj


    
    def buildHirarchy(self, horizontal_operation=None, vertical_operation=None):
        def buildRecursive(pkey, pval):
            if isinstance(pval, NestedOrderedDict):
                if vertical_operation:
                    vertical_operation(pkey, pval) 
                for key, val in pval.iteritems():
                    #if not isinstance(val, NestedOrderedDict):
                    buildRecursive(key, val)
            else:
                if horizontal_operation:
                    horizontal_operation(pkey, pval) 
    
        buildRecursive(self._mainmod.__name__, self)       

 



if __name__ == '__main__':
    import sys
    g = GetCallablesInPackage(fancytools, include_functions=True)
    print g
    
    class printClassStructure(object):
        def __init__(self): 
            self.indent = ''
            self._hor_as_last_called = True

        def hor(self, key, item):
            sys.stdout.write("%s%s - " %(self.indent,key) )
            self.indent = ''
            self._hor_as_last_called = True

        def vert(self, key, item):
            if self._hor_as_last_called:
                print ''
            print "%s-> %s" %(self.indent,key)
            self.indent += '\t'
            self._hor_as_last_called = False
            
    p = printClassStructure()
    
    g.buildHirarchy(horizontal_operation=p.hor, 
                    vertical_operation=p.vert)
