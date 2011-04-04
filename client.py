import  fuse, xmlrpclib, pickle, optparse

fuse.fuse_python_api = (0, 2)

class PythonFS(fuse.Fuse):
  def __init__(self, proxy, *args, **kwargs):
    fuse.Fuse.__init__(self, *args, **kwargs)
    self.proxy = proxy    
    
  def __getattr__(self, method):
    func = getattr(self.proxy, method)
    return lambda *args, **kwargs: pickle.loads(func(*args, **kwargs))

proxy = xmlrpclib.ServerProxy('http://localhost:7388', allow_none=True)

parser = optparse.OptionParser()
parser.set_usage('python client.py [options] volume1')
parser.add_option('-m', '--mount-point', dest='mount_point', help='Path to mount raw device', metavar='PATH', default='.')
options, args = parser.parse_args()

sys.argv = [sys.argv[0], options.mount_point, '-f']

fs = PythonFS(proxy, args, usage='USAGE', version=fuse.__version__)
