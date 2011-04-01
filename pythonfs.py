import fuse, os, sys, errno, stat

class PythonFS(fuse.Fuse):
  def __init__(self, *args, **kwargs):
    Fuse.__init__(self, *args, **kwargs)
  
  def getattr(self, path):
    return os.lstat('.' + path)
    
  def readlink(self, path):
    return os.readlink('.' + path)
    
  def readdir(self, path, offset):
    for e in os.listdir('.' + path):
      yield fuse.Direntry(e)
  
  def unlink(self, path):
    os.unlnk('.' + path)
    
  def rmdir(self, path):
    os.rmdir('.' + path)
    
  def symlink(self, path, link):
    os.symlink(path, '.' + path)
    
  def rename(self, path, name):
    os.rename('.' + path, '.' + name)
    
  def link(self, path, link):
    os.link('.' + path, '.' + link)
    
  def chmod(self, path, mode):
    os.chmod('.' + path, mode)
  
  def chown(self, path, user, group):
    os.chown('.' + path, user, group)
    
  def truncate(self, path, len):
    f = open('.' + path, 'a')
    f.truncate(len)
    f.close()
    
  def mknod(self, path, mode, dev):
    os.mknod('.' + path, mode, dev)
    
  def mkdir(self, path, mode):
    os.mkdir('.' + path, mode)
    
  def utime(self, path, times):
    os.utime('.' + path, times)
    
  def access(self, path, mode):
    if not os.access('.' + path, mode):
      return -errno.EACCES
      
  def statfs(self):
    return os.statvfs('.')
    
if __name__ == '__main__':
  fs = PythonFS()
