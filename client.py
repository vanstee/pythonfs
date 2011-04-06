import fuse, xmlrpclib, pickle, optparse, sys
import pythonfs

fuse.fuse_python_api = (0, 2)

host = sys.argv[-1:]
sys.argv[:-1]
proxy = xmlrpclib.ServerProxy('http://' + host, allow_none=True)

class PythonFS(fuse.Fuse):  
  def __getattr__(self, name):
    if name in dir(pythonfs.PythonFS):
      func = getattr(proxy, name)
      return lambda *args, **kwargs: pickle.loads(func(*args, **kwargs))
    else:
      return getattr(self, name)

fs = PythonFS(version=fuse.__version__, dash_s_do='setsingle')
fs.parse(errex=1)
fs.main()
