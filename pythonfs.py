import fuse, os, sys, errno, stat, pickle

class PythonFS:

  def _dispatch(self, method, args):
    return pickle.dumps(getattr(self, method)(*args))  
  
  def getattr(self, path):
    return os.lstat('.' + path)
  
  def readlink(self, path):
    return os.readlink('.' + path)
  
  def readdir(self, path, offset):
    return [fuse.Direntry(e) for e in os.listdir('.' + path)]

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
  
  def truncate(self, path, length):
    f = open('.' + path, 'a')
    f.truncate(length)
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
  
  class PythonFile:
    
    def __init__(self, path, flags, *mode):
      self.file = os.fdopen(os.open('.' + path, flags, *mode), None)
      self.fd = self.file.fileno()
      
    def read(self, length, offset):
      self.file.seek(offset)
      return self.file.read(length)
      
    def write(self, buffer, offset):
      self.file.seek(offset)
      self.file.write(buffer)
      return len(buffer)
      
    def release(self, flags):
      self.file.close()
      
    def _fflush(self):
      if 'w' in self.file.mode or 'a' in self.file.mode:
        self.file.flush()
        
    def fsync(self, isfsyncfile):
      self._fflush()
      if isfsyncfile and hasattr(os, 'fdatasync'):
        os.fdatasync(self.fd)
      else:
        os.fsync(self.fd)
        
    def flush(self):
      self._fflush()
      os.close(os.dup(self.fd))
    
    def fgetattr(self):
      return os.fstat(self.fd)
      
    def ftruncate(self, length):
      self.file.truncate(length)