import xmlrpclib, pickle

class FakeFS(object):
  def __init__(self, proxy):
    self.proxy = proxy
    
  def __getattr__(self, method):
    func = getattr(self.proxy, method)
    return lambda *args, **kwargs: pickle.loads(func(*args, **kwargs))

proxy = xmlrpclib.ServerProxy('http://localhost:7388', allow_none=True)
fs = FakeFS(proxy)
print fs.readddir('', 0)
