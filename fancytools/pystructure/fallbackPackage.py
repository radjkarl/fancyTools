
import sys
import imp


class Loader():
    def __init__(self, name):
        self.data = imp.find_module(name)
        self.mod = __import__(name)
        self.i = len(name)+1
        sys.modules[name] = self.mod
    
    def load_module(self, name):
        ss = self.name.split('.')
        mod = getattr(self.mod, ss[1])
        if mod is None:
            mod = imp.load_module(self.name, *self.data)
        else:
            for sss in ss[2:]:
                mod = getattr(mod, sss)
        sys.modules[name] = mod
        return mod



class Finder(object):
    def __init__(self, package_name, fallback_package_name):
        self.package_name = package_name
        self.fallback_package_name = fallback_package_name
        self.l = Loader(fallback_package_name)

    def find_module(self, fullname, path=None):
        if fullname.startswith(self.package_name):
            fullname = fullname.replace(self.package_name, self.fallback_package_name)
            self.l.name = fullname
            return self.l



def fallbackPackage(package_name, fallback_package_name):
    '''
    if an import cannot be resolved
    import from fallback package
    
    example:
    from [package_name].doesnt_exist import Foo
    
    results in 
    from [fallback_package_name].doesnt_exist import Foo
    
    '''
    importer = Finder(package_name, fallback_package_name)
    sys.meta_path.append(importer)


if __name__ == '__main__':
    
    #fancytools does not have an item 'array',
    #so, if we do the following, we get an import error:
    try:
        from fancytools import array
    except ImportError as err:
        print (err)
    #now, if we set a fallpack package, it will work:
    fallbackPackage('fancytools', 'numpy')

    from fancytools import array
    print ('now it works:', array)
    
    #this is very useful of you need to modify a package where only
    #which only contains part of all items

    
    