import fuse, xmlrpclib, pickle, optparse, sys, pythonfs

fuse.fuse_python_api = (0, 2)

class PythonFS(fuse.Fuse):
  def __init__(self, proxy, options, volumnes, *args, **kwargs):
    fuse.Fuse.__init__(self, *args, **kwargs)
    self.proxy = proxy    
    
  def __getattr__(self, name):
    if name in dir(pythonfs.PythonFS):
      func = getattr(self.proxy, name)
      return lambda *args, **kwargs: pickle.loads(func(*args, **kwargs))
    else:
      return getattr(self, name)

proxy = xmlrpclib.ServerProxy('http://localhost:7388', allow_none=True)

from optparse import OptionParser
parser = OptionParser()
parser.set_usage('python pythonfs.py [options] volume1 volume2 [volume3..]')
parser.add_option('-m', '--mount-point', dest='mount_point', help='Path to mount raw device', metavar='PATH', default='.')
options, args = parser.parse_args()

sys.argv = [sys.argv[0], options.mount_point, '-f']

fs = PythonFS(proxy, options, args, version=fuse.__version__, dash_s_do='setsingle')
fs.parse(errex=1)
fs.main()
