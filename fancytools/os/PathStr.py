# -*- coding: utf-8 -*-
import os
import shutil
import sys

class PathStr(str):
#     def __init__(self, *args):
#         print os,998
#         str.__init__(self, *args)
#         print os,666
          #print os,555
#         for a in args:
#             self = self.join(a)

    @staticmethod
    def home():
        return PathStr(os.path.expanduser("~"))
    
    
#     @staticmethod    
#     def curdir():
#         return PathStr( os.path.abspath(os.curdir) )

    @staticmethod
    def getcwd(moduleName=None):
        '''
        get current path either from the temp folder used by pyinstaller
        apps 'sys._MEIPASS' if packed with --onefile option
        or os.getcwd()
        '''
        try:
            p = PathStr(sys._MEIPASS)
            if moduleName != None:
                #pyinstaller create one temp folder
                #to separate e.g. media directories from each package it is usefull
                #to build its file-tree like this /temp/[mainPackage]/
                #to get the main package PathStr need a derived instance
                return p.join(moduleName.split('.')[0])
            return p
        except AttributeError:
            return PathStr(os.getcwd())

    def join(self, *args):
        return PathStr(os.path.join(self,*args))


    def exists(self):
        return os.path.exists(self)


    def abspath(self):
        return PathStr.join(PathStr.getcwd(), self)
        #return PathStr(os.path.abspath(self))


    def load(self, size):
        if os.path.exists(self):
            return eval( open(self).read(size) )

    def dirname(self):
    #    if os.path.isdir(self):
    #        return self
        return PathStr(os.path.dirname(self))





    def basename(self):
        return PathStr(os.path.basename(self))

    def move(self, dst):
        shutil.move(self, dst)
        self = PathStr(dst).join(self.basename())
        return self

    def mkdir(self, dname):
        n = self.join(dname)
        if not n.exists():
            os.mkdir(n)
        return n

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


    def isfile(self):
        return os.path.isfile(self)


    def isdir(self):
        return os.path.isdir(self)


    def listdir(self):
        if os.path.isdir(self):
            d = self
        else:
            d = os.path.dirname(self)
        return os.listdir(d)


    def __iter__(self):
        #TODO: iter and listdir as generator object
        if self.exists():
            return iter(self.listdir())
        return iter([])




# if __name__ == '__main__':
#     print os, PathStr('.').dirname()

        #