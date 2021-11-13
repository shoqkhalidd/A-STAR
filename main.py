###########################################################################################################################
#               Hassan Shahzad
#               18i-0441
#               CS-D
#               FAST-NUCES ISB
#               chhxnshah@gmail.com
###########################################################################################################################

###################################################### Node Class #########################################################

class Node:
        
    def __init__(self, name, parent, g, h, f):                                          # Initializing the class
        self.name = name
        self.parent = parent
        self.g = g                                                                      # Distance to start node
        self.h = h                                                                      # Distance to goal node
        self.f = f                                                                      # Total cost
            
    def __eq__(self, other):                                                            # Comparing two nodes
        return self.name == other.name
    
    def __lt__(self, other):                                                            # Sorting nodes
        return self.f < other.f
    
    def __repr__(self):                                                                 # Printing nodes
        return ('({0},{1})'.format(self.name, self.f))
    
   

###########################################################################################################################

###################################################### Graph Class ########################################################

class Graph:
    
    def __init__(self, graph_dict=None):                                 # Initialize the class
        self.graph_dict = graph_dict or {}
 
                
    def make_undirected(self):                                                          # Create an undirected graph by adding symmetric edges
        for a in list(self.graph_dict.keys()):
            for (b, dist) in self.graph_dict[a].items():
                self.graph_dict.setdefault(b, {})[a] = dist
                    
    def connect(self, A, B, distance=1):                                                # Add a link from A and B of given distance, and also add the inverse link if the graph is undirected
        self.graph_dict.setdefault(A, {})[B] = distance
        self.graph_dict.setdefault(B, {})[A] = distance
               
    def get(self, a, b=None):                                                           # Get neighbors or a neighbor
        links = self.graph_dict.setdefault(a, {})
        if b is None:
            return links
        else:
            return links.get(b)
            
    def nodes(self):                                                                    # Return a list of nodes in the graph
        s1 = set([k for k in self.graph_dict.keys()])
        s2 = set([k2 for v in self.graph_dict.values() for k2, v2 in v.items()])
        nodes = s1.union(s2)
        return list(nodes)

    def getNode(self, city, heuristics, end):                                           # Get a specific neighbour which has minimum cost
        nodes = list()
        min = 90
        
        for (b,dist) in self.graph_dict[city].items():
            if(b == end):
                return Node(city, b, dist, heuristics[b], dist+heuristics[b] )
            nodes.append(Node(city, b, dist, heuristics[b], dist+heuristics[b] ))
            if (dist+heuristics[b]) <= min:
                min = dist+heuristics[b]
                minnode = Node(city, b, dist, heuristics[b], dist+heuristics[b] )     
        return minnode
        
    def printgraph(self):                                                               # Function to print each edge in the entire graph
         for a in list(self.graph_dict.keys()):
            for (b, dist) in self.graph_dict[a].items():
                print (self.graph_dict.setdefault(a,{})[b], end = " : ")
                print(a, end = " - ")
                print(b)


###########################################################################################################################

################################################## A* Implementation ######################################################
        

def A_Star(graph, heuristics, start, end):
    open_list = list()
    closed_list = list()  
    path = list()                                                                       # Will store the path we are taking
    curr_node = graph.getNode(start,heuristics, end)                                    # Starting node
    open_list.append(curr_node)
    totalcost = 0

    if(end not in graph.graph_dict):                                                    # Incase the goal state does not exist
        print("\n\n---------------------------\nGOAL STATE DOES NOT EXIST\n---------------------------\n\n")
        return  None

    while(curr_node.name != end):                                                       # Runs Until we cannot find the goal state or

        totalcost += curr_node.g
        path.append(curr_node.name)
        curr_node = open_list.pop()
        closed_list.append(curr_node)
        curr_node = graph.getNode(curr_node.parent,heuristics, end)
        open_list.append(curr_node)
        if(curr_node.name == end):
            path.append(curr_node.name)
            break

    print("FINAL COST -> " + str(totalcost),end = " ")
    return path
    
###########################################################################################################################

########################################################## Main ###########################################################


# The main entry point for this module
def main():
    # Create a graph
    graph = Graph()
        
    # Create graph connections (Actual distance)
    graph.connect('Bus Stop', 'Riyadh Boulevard', 10)
    graph.connect('Bus Stop', 'Qariat Zaman', 23)
    graph.connect('Bus Stop', 'The Groves', 12)
    graph.connect('Winter Wonderland', 'Riyadh Boulevard', 7)
    graph.connect('Riyadh Boulevard', 'Riyadh Front', 24)
    graph.connect('Riyadh Front', 'Qariat Zaman', 17)
    graph.connect('Qariat Zaman', 'khulawha', 9)
    graph.connect('Qariat Zaman', 'Winter Wonderland', 15)
    graph.connect('Via Riyadh', 'The Groves', 3)
    graph.connect('Al Murabba','Via Riyadh', 14)
    graph.connect('Al Murabba','Al Salam Tree', 6)
    graph.connect('Al Salam Tree', 'Via Riyadh',18)
    #graph.connect('Nabd Al Riyadh', 'Al Murabba', 5)
    #graph.connect('Al Salam Tree','Nabd Al Riyadh', 3)
    graph.connect('Al Murabba','Qariat Zaman', 29)
    graph.connect('Al Murabba', 'khulawha', 36)
 
        
        
    # Make graph undirected, create symmetric connections
    graph.make_undirected()
        
    # Create heuristics (straight-line distance, Bus-Ride distance) for Destination Bus Stop
    SLheuristics = {}
    SLheuristics['Riyadh Front'] = 21.3
    SLheuristics['Qariat Zaman'] = 19.8
    SLheuristics['khulawha'] = 26.3
    SLheuristics['Winter Wonderland'] = 8.28
    SLheuristics['Riyadh Boulevard'] = 5.38
    SLheuristics['Via Riyadh'] = 7.4
    SLheuristics['Al Murabba'] = 16.6
    SLheuristics['Nabd Al Riyadh'] = 16.9
    SLheuristics['The Groves'] = 5.34
    SLheuristics['Al Salam Tree'] = 17
    SLheuristics['Bus Stop'] = 0
    
    # Create heuristics time based for Destination Bus Stop
    
    Theuristics = {}
    Theuristics['Riyadh Front'] = 36 
    Theuristics['Qariat Zaman'] = 28
    Theuristics['khulawha'] = 40
    Theuristics['Winter Wonderland'] = 20
    Theuristics['Riyadh Boulevard'] = 17
    Theuristics['Via Riyadh'] = 31
    Theuristics['Al Murabba'] = 26
    Theuristics['The Groves'] = 33
    Theuristics['Al Salam Tree'] = 45
    Theuristics['Bus Stop'] = 0
    
    
        
    # Print Graph Nodes
    #graph.printgraph()
    #print("--------------------------------\n\n")
    # Run search algorithm
    SLpath = A_Star(graph, SLheuristics, 'Al Murabba', 'Bus Stop') 
    print("KM")       
    print("PATH: " ,end = " ")
    print(SLpath)

    Tpath = A_Star(graph, Theuristics, 'Al Murabba', 'Bus Stop') 
    print("min")       
    print("PATH: " ,end = " ")
    print(Tpath)

# Tell python to run main method
if __name__ == "__main__": 
    main()
