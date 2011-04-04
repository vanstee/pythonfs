import xmlrpclib, SimpleXMLRPCServer, threading
import pythonfs

server = SimpleXMLRPCServer.SimpleXMLRPCServer(('localhost', 7388))
server.register_instance(pythonfs.PythonFS())
server.serve_forever()
