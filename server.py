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
      

pythonfs = SimpleXMLRPCServer.SimpleXMLRPCServer(('localhost', 7388))
pythonfs.register_instance(pythonfs.PythonFS())
fsserver = Server(pythonfs)
fsserver.start()

pythonfile = SimpleXMLRPCServer.SimpleXMLRPCServer(('localhost', 7389))
pythonfile.register_instance(pythonfs.PythonFile())
fileserver = Server(pythonfile)

try:
  fsserver.start()
  fileserver.start()
except KeyboardInterrupt:
  fsserver.shutdown()
  fileserver.shutdown()
