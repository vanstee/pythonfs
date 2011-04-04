import xmlrpclib, SimpleXMLRPCServer, threading
import pythonfs

class Server(threading.Thread):
  def __init__(self, server):
    self.server = server
    self.killed = False
    threading.Thread.__init__(self)
    
  def run(self):
    self.server.serve_forever()
    
  def shutdown(self):
    self.server.shutdown()
      

fsserver = SimpleXMLRPCServer.SimpleXMLRPCServer(('localhost', 7388))
fsserver.register_instance(pythonfs.PythonFS())
fsthread = Server(fsserver)

fileserver = SimpleXMLRPCServer.SimpleXMLRPCServer(('localhost', 7389))
fileserver.register_instance(pythonfs.PythonFile())
filethread = Server(fileserver)

try:
  fsthread.start()
  filethread.start()
except KeyboardInterrupt:
  fsthread.shutdown()
  filethread.shutdown()
