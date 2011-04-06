import xmlrpclib, SimpleXMLRPCServer
import pythonfs

server = SimpleXMLRPCServer.SimpleXMLRPCServer(('0.0.0.0', 80))
server.register_instance(pythonfs.PythonFS())
server.serve_forever()
