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
    os.unlink('.' + path)
  
  def rmdir(self, path):
    os.rmdir('.' + path)
  
  def symlink(self, path, link):
    os.symlink(path, '.' + link)
  
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
    
  def open(self, path, flags):
    os.fdopen(os.open('.' + path, flags))
      
  def create(self, path, flags, mode):
    os.fdopen(os.open('.' + path, flags, mode))

  def read(self, path, length, offset, fh=None):
    f = os.fdopen(os.open('.' + path, 'r'))
    f.seek(offset)
    data = f.read(length)
    f.close()
    return data
    
  def write(self, path, buffer, offset, fh=None):
    f = os.fdopen(os.open('.' + path, 'w'))
    f.seek(offset)
    f.write(buffer)
    f.close()
    return len(buffer)
    
  def fgetattr(self, path, fh=None):
    f = os.fdopen(os.open('.' + path, 'r'))    
    fd = f.fileno()
    return os.fstat(fd)
    
  def ftruncate(self, path, length, fh=None):
    f = os.fdopen(os.open('.' + path, 'r'))
    f.truncate(length)

  def flush(self, path, fh=None):
    f = os.fdopen(os.open('.' + path))    
    f.flush()
    
  def release(self, path, fh=None):
    f = os.fdopen(os.open('.' + path))    
    f.flush()
        
  def fsync(self, fdatasync, fh=None):
    f = os.fdopen(os.open('.' + path))
    fd = f.fileno()
    if fsyncfile and hasattr(os, 'fdatasync'):
      os.fdatasync(fd)
    else:
      os.fsync(fd)