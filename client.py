import  fuse, xmlrpclib, pickle

fuse.fuse_python_api = (0, 2)

class PythonFS(fuse.Fuse):
  def __init__(self, *args, **kwargs):
    fuse.Fuse.__init__(self, *args, **kwargs)
    self.proxy = proxy    
    
  def __getattr__(self, method):
    func = getattr(self.proxy, method)
    return lambda *args, **kwargs: pickle.loads(func(*args, **kwargs))

proxy = xmlrpclib.ServerProxy('http://localhost:7388', allow_none=True)
fs = PythonFS(proxy, usage='')
