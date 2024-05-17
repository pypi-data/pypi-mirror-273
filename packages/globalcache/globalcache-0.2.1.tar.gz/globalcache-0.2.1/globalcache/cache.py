# -*- coding: utf-8 -*-
from functools import wraps
import inspect
import shelve
import os
from os.path import basename, dirname, join, splitext
from typing import Callable, NewType, TypeVar, Union, Any
from collections import OrderedDict
import logging
import shutil
from functools import cached_property
import warnings

logger = logging.getLogger(__name__)


DEFAULT_GLOBAL_CACHE_NAME = '__GLOBAL_CACHE__'
DEFAULT_SIZE_LIMIT = None
DEFAULT_DISABLE = False
DEFAULT_SAVE_DIR = '.globalcache'

# GLOBAL_CACHE_NAME = os.environ.get('GLOBAL_CACHE_NAME', 
#                                    '__GLOBAL_CACHE__')

# DISABLE = os.environ.get('GLOBAL_CACHE_DISABLE', '')
# if DISABLE == '1':
#     DISABLE = True
# else:
#     DISABLE = False

# SIZE_LIMIT = os.environ.get('GLOBAL_CACHE_SIZE_LIMIT', '10')
# SIZE_LIMIT = int(SIZE_LIMIT)
# if SIZE_LIMIT <= 0:
#     SIZE_LIMIT = None


# SAVE_DIR = os.environ.get('GLOBAL_CACHE_SAVE_DIR', '.globalcache')

class Settings:
    """Global settings for globalcache. 
    These will overwrite local settings if set. 
    
    Attributes
    ----------
    global_cache_name : str 
        Name of cache to be inserted into `globals()`
        Set to '' for default. 
    disable : bool
        True to disable global caching. 
    size_limit : int or None
        Maximum size of cache for each cached variable. Set SIZE_LIMIT <= 0
        for unlimited length. 
        Set None for default length.
    save_dir : str
        Directory path of shelve cache on disc.
        
    """
    global_cache_name = DEFAULT_GLOBAL_CACHE_NAME
    disable = DEFAULT_DISABLE
    size_limit = None
    save_dir = ''


# class Environ:
#     """Read any environmental variables."""
#     @staticmethod
#     def size_limit():
#         out = os.environ.get('GLOBAL_CACHE_SIZE_LIMIT', DEFAULT_SIZE_LIMIT)
#         return out
    
#     @staticmethod
#     def disable():
#         out = os.environ.get('GLOBAL_CACHE_DISABLE', '0')
#         if out == '1':
#             return True
#         return DEFAULT_DISABLE
    
#     @staticmethod
#     def save_dir():
#         out = os.environ.get('GLOBAL_CACHE_SAVE_DIR', '')
#         if out == '':
#             return DEFAULT_SAVE_DIR
#         else:
#             return out
        
        
def get_size_limit(size_limit: int) -> int:
    """Get size limit. Global limit will overwrite local setting."""
    # out = os.environ.get('GLOBAL_CACHE_SIZE_LIMIT', size_limit)
    if Settings.size_limit is not None:
        return Settings.size_limit
    
    if size_limit is not None:
        return size_limit
    else:
        return DEFAULT_SIZE_LIMIT


def get_disable() -> bool:
    """Get disable flag from global settings."""
    # out = os.environ.get('GLOBAL_CACHE_DISABLE', '0')
    return Settings.disable


def get_save_dir(save_dir: str) -> str:
    """Get save directory. Global save_dir will over-write local preference."""
    # out = os.environ.get('GLOBAL_CACHE_SAVE_DIR', save_dir)
    if Settings.save_dir != '':
        return Settings.save_dir
    if save_dir != '':
        return save_dir
    else:
        return DEFAULT_SAVE_DIR
    
        
    

class CacheError(Exception):
    pass



class LimitDict(OrderedDict):
    """Dictionary with limited size.
    
    Attributes
    ----------
    size_limit : int
        Max length of dict. You can re-set this on the fly.
    """
    def __init__(self, *args, _size_limit: int=None, **kwargs):
        self.size_limit = _size_limit
        super().__init__(*args, **kwargs)
        self._check_size_limit()
    
    
    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self._check_size_limit()
        
    
    def _check_size_limit(self):
        if self.size_limit is not None:
            while len(self) > self.size_limit:
                self.popitem(last=False)
                
CacheValue = TypeVar('CacheValue')
CacheDict = TypeVar('CacheDict', bound=dict[str, LimitDict[str, CacheValue] ])


class _GlobalSingleton:
    """A global object stored in globals() to coordinate the cache.
    
    Attributes
    ----------
    caches : dict[Cache]
        Repository of all Caches initialized so far. 
    global_dict : CacheDict
        Dictionary of 
    """
    def __init__(self, gdict: dict, name: str=''):
        self.caches = {}
        self.global_dict = {}
        if name == '':
            name = Settings.global_cache_name
        
        gdict[name] = self
        

        self.update(gdict, name)
    
    
    def update(self, gdict: dict, name: str=''):
        
        if name == '':
            name = Settings.global_cache_name
        
        if name in gdict:
            logger.debug('GlobalCache %r found in globals().', name)
            self.myself = gdict[name]    
            self.caches = self.myself.caches
            global_dict1 = self.myself.global_dict
            self.global_dict.update(global_dict1)
            
        else:
            logger.debug('GlobalCache %r not found', name )
            if gdict['__name__'] == '__main__':
                logger.debug('__main__ found.')
                gdict[name] = self

        return self
    
    
    def reset(self):
        cache : Cache
        for name, cache in self.caches.items():
            cache.reset()
            
    def delete_shelve(self):
        cache : Cache
        for name, cache in self.caches.items():
            cache.delete_shelve()
            
    def set_size_limit(self, size_limit: int):
        cache: Cache
        for cache in self.caches.values():
            cache.set_size_limit(size_limit)
            
            
    
    
    
            
            
# Initialize the singleton.
global_singleton = _GlobalSingleton(globals())

def reset():
    global_singleton.reset()
    
def delete_shelves():
    global_singleton.delete_shelve()
    
def set_global_size_limit(size_limit: int):
    global_singleton.set_size_limit(size_limit)


class Cache:
    """Global cache to cache values in ipython session.
    
    Parameters
    ----------
    g : dict
        Must be set to `globals()`.
    name : str, optional
        Name of dictionary stored in globals(). 
        Defaults to `DEFAULT_GLOBAL_CACHE_NAME`.
    reset : bool, optional
        Force reset of globalcache. The default is False.
        
    """    
    
    _global_vars : set[str]
    size_limit : int

    def __init__(self,
                 g: dict, 
                 name: str='', 
                 reset: bool=False,
                 size_limit: int=None,
                 save_dir='',
                 ):
        self._globals = g
        self.name = name
        logger.debug('Creating cache %s', self)
        
        # if name is None:
        #     name = DEFAULT_GLOBAL_CACHE_NAME    
            
        # self.cdict = {}
        self.size_limit = size_limit
        self.save_dir = save_dir
        self.is_main = False
        self._is_main_found = False
        self._function_caches = set()
        self.set_globals(g, name, size_limit, save_dir)
        
        if reset:
            self.reset()
            
            
    def __repr__(self):
        g = self._globals
        try:
            gname = g['__name__']
        except KeyError:
            gname = '...'
        out = f"Cache('{gname}','{self.name}')"
        return out
    
            
    def init(self,
            g: dict,
            name: str = '', 
            size_limit: Union[int, None] = None,
            save_dir: str='',
            ):
        """Call this to initialize gcache for each script it is imported into.
        
        >>> from globalcache import gcache
        >>> gcache.init(globals())
        
        Parameters
        ----------
        g : dict
            Input globals() here.
        name : Union[str, None], optional
            Name of cache's dictionary key in globals().
            The default is None and will take the name '__GLOBAL_CACHE__'.
        size_limit : Union[int, None], optional
            Default max number of items to store in cache dictionary. The default is None.
        save_dir : str, optional
            Directory path to save data. By default this path is '.globalcache'.

        Returns
        -------
        None.

        """
        self.set_globals(
            g=g, name=name,
            size_limit=size_limit, save_dir=save_dir)
        
    
    def set_globals(
            self, 
            g: dict,
            name: str = '', 
            # reset: bool = False,
            size_limit: Union[int, None] = None,
            save_dir: str='',
            ):
        """Use this method to re-set the globals() dict for the cache.
        
        Initialization are probably a random mix of outside of __main__ and not. 
        """
        
        self.global_singleton = global_singleton.update(g, name=name)
        module_name = g['__name__']
        self.global_singleton.caches[module_name] = self
        
        self.size_limit = size_limit
        self.save_dir = save_dir
                    
        self._function_cache_names  = {}
                        
        return
    
    
    def var(self,
            name: str, 
            args: tuple=(),
            kwargs: dict={}, 
            size_limit=None,
            save: bool = False,
            module: str = '',
            ) -> 'CacheVar':
        """Create cached variable. 

        Parameters
        ----------
        name : str
            Name of variable. Must be unique.
        args : tuple, optional
            Hashable arguments for result identification. The default is ().
        kwargs : dict, optional
            Hashable kwargs for result identification. The default is None.
        size_limit : int, optional
            Max size of cached results. The default is None.
        save : bool, optional
            True to save cache to disk. Default is False. 
        module : str
            Rename the module label. Default is ''.
            
            
        Raises
        ------
        ValueError
            Raised if you repeat a variable name.

        Returns
        -------
        CacheVar
        """
        if size_limit is None:
            size_limit = self.size_limit
        logger.debug('Creating CacheVar %s', name)
        return CacheVar(self, name=name, args=args, kwargs=kwargs,
                        size_limit=size_limit, save=save, module=module)
            
        
    
    def decorate(self,
                 fn : Union[None, Callable] = None,
                 size_limit: Union[None, int] = None, 
                 reset: bool = False,
                 save: bool = False,
                 name: str = '',
                 ) -> Callable:
        """Decorate an expensive function to cache the result. 

        Parameters
        ----------
        fn : Callable
            Function to decorate.
            
        size_limit : int, optional
            Max cache size (keyword argument not supported)
            
        reset : bool, optional
            True to reset globals() cache. Default is False.
            
        save : bool, optional
            True to save cache to disk. Default is False. 

        Returns
        -------
        func : Callable 
            Decorated function. Note this function has an additional 
            attribute `fn_cache` to retrieve the FunctionCache object.
        """        
        if size_limit is None:
            size_limit = self.size_limit
        
        if callable(fn):
            return self._sub_decorate(
                fn, 
                size_limit=size_limit,
                reset=False,
                save=False,
                )
        else:
            
            def func(fn):
                return self._sub_decorate(
                    fn, 
                    size_limit=size_limit,
                    reset=reset,
                    save=save,
                    name=name,
                    )
        return func
        
                            
    def _sub_decorate(self, fn: Callable, 
                      size_limit: int,
                      reset : bool,
                      save : bool,
                      name: str = '',
                      ):
        logger.debug('Initializing function %s', fn)
        fn_cache = FunctionCache(self,
                                 fn=fn,
                                 size_limit=size_limit,
                                 save=save, 
                                 name=name
                                 )
        
        # key = fn_cache.module + '-' + fn_cache.name
        self._function_caches.add(fn_cache)
        if reset:
            fn_cache.reset()
           
        @wraps(fn)
        def func(*args, **kwargs):
            return fn_cache(*args, **kwargs)
        
        
        func.fn_cache = fn_cache
            
        return func
    

    def reset(self):
        """Reset the global cache dict."""
        logger.debug('Resetting cache %s', self)
        self.global_singleton.global_dict.clear()
        # self.cdict.clear()
        for fun_cache in self._function_caches:
            fun_cache.reset()
        
        
    def delete_shelve(self):
        """Delete persistent shelve file data."""
        dir1  = self.save_dir
        dir1 = get_save_dir(dir1)

        if os.path.exists(dir1):
            shutil.rmtree(dir1)
            
        # Reset to reinitiatlize FunctionCache
        for fn_cache in self._function_caches:
            fn_cache._is_first_run = True
        
        
        
    @property
    def module_names(self) -> list[str]:
        """Names of all cached modules."""
        cdict = self.global_singleton.global_dict
        return list(cdict.keys())
    
    def module_names_short(self) -> list[str]:
        names = [splitext(basename(path))[0] for path in self.module_names]
        out = rename_duplicates(names)
        return out
    
    
    def get_module_short_name(self, name: str):
        """Take module name and return a shortened version."""
        d = dict(zip(self.module_names, self.module_names_short()))
        return d[name]
    
    @property
    def function_caches(self) -> list['FunctionCache']:
        return list(self._function_caches)
    
    
    def print_status(self):
        print('globals() is initialized in main scope:', self.is_main)
        print('')
        print('Cached functions list:')
        for fcache in self.function_caches:
            print(fcache)
            print('Module = ', fcache.module)
            print('Cached entries = ', len(fcache.fcache))
            print('')
        print('')       
        
        
    def set_size_limit(self, size_limit: int):
        self.size_limit = size_limit
        for fn_cache in self.function_caches:
            fn_cache.fcache.size_limit = size_limit
            
    
        
def get_name(fn : Callable) -> str:
    """Create a name for a callable function."""
    # name = fn.__name__
    name = fn.__qualname__
    while True:
        try:
            parent = fn.__self__
            fn = parent.__class__
            # parent_name = fn.__name__
            parent_name = fn.__qualname__
            name = parent_name + '.' + name
            breakpoint()
        except AttributeError:
            break
    return name
        
        
def rename_duplicates(lst: list) -> list:
    """Rename duplicates in a list. From ChatGTP"""
    seen_elements = {}
    renamed_list = []

    for element in lst:
        if element in seen_elements:
            seen_elements[element] += 1
            new_element = f"{element}_{seen_elements[element]}"
        else:
            seen_elements[element] = 1
            new_element = element

        renamed_list.append(new_element)

    return renamed_list


            

class FunctionCache:
    """Cache function output into globals(). Should not be directly called,
    create using Cache.decorate(...)
    

    Parameters
    ----------
    cache : Cache
        Cache from globalcache.
    fn : Callable
        Function to cache.
    size_limit : int
        Maximum number of values to store.
    save : bool
        Save output to file? True for yes.
    name : str, optional
        Name of function. The default is '' and uses inspect to get the name.
    module : str, optional
        Name of module. The default is '' and uses inspect to get the module..


    Raises
    ------
    CacheError
        Raised if you attempt to define a cache for a function multiple times.

    Attributes
    ----------
    
    shelve_name : str
        Name of file corresponding to shelve file storage.
    fcache : LimitDict
        Cache dictionary for function.
        

    """
    fcache: LimitDict
    def __init__(self, cache: Cache,
                 fn : Callable,
                 size_limit: int,
                 save: bool,
                 name: str = '',
                 module: str = '',
                 ):

        # Initialize deafault settings
        if module == '':
            module = inspect.getsourcefile(fn)
        if name == '':
            name = get_name(fn)       
        size_limit = get_size_limit(size_limit)
        
        self.size_limit = size_limit
        self.name = name
        self.save = save
        self.module = module        
        self._cache = cache
        self.fn = fn
        self._is_first_run = True
        
        # Initialize global dicts
        self.reinit_dicts()
        
        # Read shelve data        
        self.shelve_name = cache.get_module_short_name(module)
            
        # Track definitions to prevent redefinition.
        function_list = cache._function_cache_names.setdefault(module, [])

        if name in function_list:
            raise CacheError(f'{name} cannot be redefined for module {module}')
        else:
            function_list.append(name)
            
            
    def __repr__(self):
        return f"FunctionCache({self.fn})"
    
    def __hash__(self):
        return hash(self.module + '-' + self.name)
        
            
    def reinit_dicts(self):
        """Reinitialize dictionaries to make sure they are in the right
        globals() dict."""
        cache = self._cache
        global_dict = cache.global_singleton.global_dict
        
        # Get module-level dictionary
        # self.module_dict = cache.m
        self.module_dict = global_dict.setdefault(self.module, {})
        # self.module_dict = cache.cdict.setdefault(self.module, {})
        
        # Get argument-value dictionary
        self.fcache = self.module_dict.setdefault(
            self.name,
            LimitDict(_size_limit=self.size_limit)
            )
        
        
        
        
            
            
    def is_cached(self, *args, **kwargs) -> bool:
        """Check whether given arguments for function has cached value."""
        if kwargs is not None:
            kwargs2 = frozenset(kwargs.items())
        else:
            kwargs2 = None
            
        key = (args, kwargs2)
        
        
        if key in self.fcache:
            return True
        if self.save:
            shelve_key = str((self.name, args, kwargs))
            if self.is_shelved(shelve_key):
                return True
            
        return False
        
    
        
    def __call__(self, *args, **kwargs):
        """Call the function with caching.

        Parameters
        ----------
        *args : 
            Function arguments.
        **kwargs : 
            Function keyword arguments.

        Raises
        ------
        CacheError
            Raised if you try to use unhashable arguments in function.

        Returns
        -------
        out :
            Function `fn` output.

        """
        
        # Reun as-is if caching is disabled by environ variable. 
        name = self.name
        self.reinit_dicts()
        
        if get_disable():
            logger.debug('Disable flag detected. Disabling cache.')
            return self.fn(*args, **kwargs)
        
        # globalcache will not work if globals() are not from __main__ script
        # if not self._cache.is_main:
        #     logger.info('gcache has not yet been initialized with globals(). Cache is disabled')
        #     logger.debug('globals() not set. Disabling cache.')
        #     return self.fn(*args, **kwargs)
            
        
        # Initialize file persistence
        if self._is_first_run:
            self._is_first_run = False
            if self.save:
                logger.debug('Initializing shelve for %s', name)
                self.shelve_init()
                
            
        if kwargs is not None:
            kwargs2 = frozenset(kwargs.items())
        else:
            kwargs2 = None
            
        key = (args, kwargs2)
        try:
            try:
                output = self.fcache[key]
            except TypeError:
                raise CacheError(f'Arguments {args} and {kwargs} for function {self.name} must be hashable.')
                
            logger.debug('Retrieved key=%s from fcache %s', key, name)
            return output
        except KeyError:
            
            if self.save:
                shelve_key = str((self.name, args, kwargs))
                try:
                    output = self.shelve_read(key, shelve_key)
                    logger.debug('Read key=%s from shelve for %s', key, name)
                except KeyError:
                    logger.debug('key=%s not found in shelve cache. Running function %s', key, name)
                    output = self.fn(*args, **kwargs)
                    self.shelve_save(shelve_key, output)
            else:
                logger.debug('key=%s not found in cache. Running function %s', key, name)
                output = self.fn(*args, **kwargs)
            
            self.fcache[key] = output
            return output
                
    
    def shelve_init(self):
        """Initialize shelve file persistence."""
        save_dir = self._cache.save_dir
        save_dir = get_save_dir(save_dir)
        dir1 = save_dir
        
        os.makedirs(dir1, exist_ok=True)
        
    
    @cached_property
    def shelve_path(self) -> str:
        """Get shelve file path."""
        save_dir = self._cache.save_dir
        save_dir = get_save_dir(save_dir)
        dir1 = save_dir
        
        path = join(dir1, self.shelve_name)
        return path
    
    
    def shelve_save(self, shelve_key: str, output: Any):
        """Save cache variable to shelve"""

        with shelve.open(self.shelve_path) as db:
            db[shelve_key] = output
            
            
    def shelve_read(self, key: tuple, shelve_key: str) -> Any:
        """Read from shelve."""
        with shelve.open(self.shelve_path) as db:
            out =  db[shelve_key]
            self.fcache[key] = out
        return out
    
    
    def is_shelved(self, shelve_key: str) -> bool:
        """Check if data has been cached to file."""
        with shelve.open(self.shelve_path) as db:
            return shelve_key in db
    
    def reset(self):
        """Delete globals() cache."""
        self.fcache.clear()
        
    
    
class CacheVar:
    """Cache variables. Usually use Cache.var(...) to create this.
    
    Parameters
    ----------
    cache : Cache
        Cache object.
    name : str
        Name of variable cache.
    args : tuple
        arguments.
    kwargs : dict
        keyword arguments.
    size_limit : int
        Max size limit of cache.
    save : bool
        Save to disk?
    module : str, optional
        Module name. The default is ''.
        
        
    Attributes
    ----------
    key : tuple
        Hashable key used to map arguments to output dictionary
    fn_cache : FunctionCache
        FunctionCache object used to drive calculations
    

    """
    fn_cache : FunctionCache
    
    def __init__(self, cache: Cache,
                 name : str,
                 args : tuple,
                 kwargs: dict,
                 size_limit: int,
                 save: bool,
                 module: str = '',
                 ):

        
        self.cache = cache
        self.name = name
        self.args = args
        self.kwargs = kwargs
        self.save = save

        def fn(*args, **kwargs):
            raise CacheError('This dummy function should not ever be called.')

        kwargs2 = frozenset(kwargs.items())
            
        self.key = (args, kwargs2)
        self.fn_cache = FunctionCache(
            cache = cache, 
            fn = fn,
            size_limit = size_limit,
            save = save, name = name, module = module
            )
    
    def set(self, output: Any):
        """Set cached variable data."""

        self.fn_cache.fcache[self.key] = output
    
        
    @property
    def is_cached(self) -> bool:    
        """Check whether cached values are found."""
        if get_disable():
            return False
        
        return self.fn_cache.is_cached(*self.args, **self.kwargs)
    
    
    @property
    def not_cached(self) -> bool:
        """Return False if no cached values are found."""
        return not self.is_cached
        
    
    def get(self) -> Any:
        return self.fn_cache.fcache[self.key]

        
        

                 
class __CacheVarOLD:
    """Create dictionary structure for cache variable.
    
    Parameters
    ----------
    cache : Cache
        Cache.
    module : str
        Python module name.
    name : str
        Python function name.
    args : tuple
        Python function arguments.
    kwargs : dict
        Python function keyword arguments.
    size_limit : int
        Maximum cache size.
    save : bool, optional
        Save results to file. The default is False.
    
    Attributes
    ----------
    module_dict : dict[str, dict]
        Cache for a Python module
        
    fcache : dict[str, LimitDict]
        Cache for a function in the module.
        
    key : tuple
        Function arguments used for fcache key.
        
    name : str
        Name of function. 
        
        
    """
    
    module_dict : dict[str, dict]
    
    def __init__(self, 
                 cache: Cache, 
                 module: str,
                 name: str, 
                 args: tuple, 
                 kwargs: dict,
                 size_limit: int,
                 save: bool = False,
                 reset: bool = False,
                 ):
        
        # print('CacheVar:', module, name)
        # Get module-level dictionary
        self.module_dict = cache.cdict.setdefault(module, {})
        
        # Get argument-value dictionary
        self.fcache = self.module_dict.setdefault(
            name,
            LimitDict(_size_limit=size_limit)
            )
        
        if kwargs is not None:
            kwargs = frozenset(kwargs.items())
        
        self.key = (args, kwargs)
        self.name = name
        self._cache = cache
        
        
        module_hash = hash(module)
        module_fname = splitext(basename(module))[0]
        # self.shelve_name = self.
        self.shelve_key = str((name, args, kwargs))
        self.save = save
        
        if reset:
            self.reset()
            
        if save:
            try:
                self.shelve_read()
            except FileNotFoundError:
                logger.debug('No file found in shelve for %s %s %s', module, name, self.key)
            except KeyError:
                logger.debug('No key found in shelve for %s %s %s', module, name, self.key)
            
        
        
    def get(self) -> CacheValue:
        """Retrieve cached value if it exists.
        
        Raises
        ------
        ValueError
            Raised if cache has not yet been set.
        """
        key = self.key
        try:
            logger.debug('Retrieving %s %s from cache', self.name, key)
            return self.fcache[key]
        
        except KeyError:
            raise ValueError('Variable not yet set.')
            
            
    @property
    def is_cached(self) -> bool:
        """Check whether a value has been cached."""
        if Settings.DISABLE:
            return False
        # breakpoint()
        return self.key in self.fcache
    
    
    @property
    def not_cached(self) -> bool:
        """Check that a value is not cached."""
        if Settings.DISABLE:
            return True
        # breakpoint()

        return self.key not in self.fcache
    
    
    def set(self, data):
        """Set data into cache.
        
        Returns
        -------
        data : 
            Return input argument.
        """
        logger.debug('Saving %s %s into cache', self.name, self.key)
        self.fcache[self.key] = data
        if self.save:
            self.shelve_save()
            
        return data
    
    def reset(self):
        """Reset cache."""
        if self.key in self.fcache:
            del self.fcache[self.key]
            
            
    def shelve_save(self):
        """Save cache variable to shelve"""
        dir1 = self._cache.save_dir
        # dir1 = os.path.dirname(path)
        os.makedirs(dir1, exist_ok=True)
        path = join(dir1, self.shelve_name)
        with shelve.open(path,) as db:
            db[self.shelve_key] = self.get()
            
            
    def shelve_read(self):
        """Read from shelve."""
        dir1 = self._cache.save_dir
        path = join(dir1, self.shelve_name)
        with shelve.open(path) as db:
            out =  db[self.shelve_key]
            self.fcache[self.key] = out
        return out
    
        
        
        
    def __bool__(self):
        """Return self.is_cached."""
        
        return self.is_cached
        
    
# %% Create a cache here 


gcache = Cache(globals())
