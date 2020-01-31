class Socket():
    def __init__(self, owner):
        """. 
            "Trigger" for Trigger nodes.
            "Read" represents read type, 
            "Write" for write type
        """
        self.owner_node = owner
        self.type = 'Trigger'# defines trigger type
        
        self.connected_sockets = []
        
#    def trigger(self):
#        """Called when triggered"""
#        pass
    def is_valid_connection(self, socket):
        return True
    def connect(self, socket):
        if self.is_valid_connection(socket):
            self.connected_sockets.append(socket)
        
    def value(self):
        return self.owner_node.value
    
    def on_request(self, req):
        if req == "EXECUTE":
            self.owner_node.execute()
            
    def request(self, req):
        for socket in self.connected_sockets:
            socket.on_request(req)
class Node():
    def __init__(self):
        self.data = None
        self.data_type = "int"
        
        self.trigger_sockets = []
        self.value_sockets = []
    
    @property
    def value():
        return self.data
    
    @value.setter
    def value():
        return self.data
    
class NodeTree():
    def __init__(self):
        self.nodes_list = []
        
    def add_node(self, node_obj):
        self.nodes_lis.append(node_obj)
    
    def create_node(self, node_type):
        pass
    
#    def update(): # Required?
#        pass

#class TimeLineNode( Node ):
#    def __init__(self):
#        Node.__init__(self):
#        self.value = None
#    
#    def trigger(self, socket):
#        self.value.start()

class PrintNode( Node ):
    def __init__(self):
        self.socket_list = []
    
    def add_socket(self):
        self.socket_list.append(Socket(self))
    
    def execute(self):
        print ("printed")
    
class ProgramNode( Node ):
    """Contains several other nodes that are supposed to execute."""
    
    def __init__(self): 
        Node.__init__(self)
        self.socket_list = []
    
    def add_socket(self):
        self.socket_list.append(Socket(self))
        
    def execute(self):
        for sockets in self.socket_list:
            sockets.request("EXECUTE")

print_node = PrintNode()
print_node.add_socket()
print_socket = print_node.socket_list[0]


prog_node = ProgramNode()
prog_node.add_socket()
prog_socket = prog_node.socket_list[0]

prog_socket.connect(print_socket)

prog_node.execute()



