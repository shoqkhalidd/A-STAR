
# 
# originally written by  Hassan Shahzad, contact chhxnshah@gmail.com
#
# modified by Shoug Alsuhibani, contact ssuhaibani@sm.imamu.edu.sa
#             Shouq Almutairi , contact skaalmutairi@sm.imamu.edu.sa
#             Noor Elmasry    , contact nelmasry@sm.imamu.edu.sa
#             Reema Aloqayli  , contact rmnaloqayli@sm.imamu.edu.sa
#
# in order to fillfull a CS361 Project specification            
#
###########################################################################################################################

###################################################### Node Class #########################################################

class Node:
        
    def __init__(self, name, parent, g, h, f):                                           # Initializing the class
        self.name = name
        self.parent = parent                                                             # node's parent
        self.g = g                                                                       # Distance to start node
        self.h = h                                                                       # Distance to goal node
        self.f = f                                                                       # Total cost
            
    def __eq__(self, other):                                                             # Comparing two nodes
        return self.name == other.name
    
    def __lt__(self, other):                                                             # Sorting nodes
        return self.f < other.f
    
    def __repr__(self):                                                                  # Printing nodes
        return ('({0},{1})'.format(self.name, self.f))
    
   

###########################################################################################################################

###################################################### Graph Class ########################################################

class Graph:
    
    def __init__(self, graph_dict=None):                                                 # Initialize the class
        self.graph_dict = graph_dict or {}
                    
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
        min = 9999
        
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
    open_list = list()                                                                  # candidate nodes
    closed_list = list()                                                                # visited nodes
    path = list()                                                                       # Will store the path we are taking
    curr_node = graph.getNode(start,heuristics, end)                                    # Starting node
    open_list.append(curr_node)
    totalcost = 0
    time=0

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
        time +=curr_node.h
        if(curr_node.name == end):
            path.append(curr_node.name)
            break

    print("Final cost: " + str(totalcost) + " KM")
    return path,time
  
###########################################################################################################################

########################################################## Main ###########################################################


# The main entry point for this module
def main():
    # Create a graph
    graph = Graph()
        
    # Create graph connections (Actual distance in KM)
    graph.connect('Bus Stop', 'Riyadh Boulevard', 10)
    graph.connect('Bus Stop', 'Qariat Zaman', 23)
    graph.connect('Bus Stop', 'The Groves', 12) 
    graph.connect('Tuwaiq Palace','Via Riyadh', 5)
    graph.connect('Tuwaiq Palace','The Groves', 8)
    graph.connect('Via Riyadh', 'The Groves', 3)
    graph.connect('Via Riyadh', 'Al Salam Tree',18)
    graph.connect('Al Murabba','Via Riyadh', 14)
    graph.connect('Al Murabba','Al Salam Tree', 6)
    graph.connect('Al Murabba','Qariat Zaman', 29)
    graph.connect('Al Murabba', 'khulawha', 36)
    graph.connect('Qariat Zaman', 'Riyadh Front', 17)
    graph.connect('Qariat Zaman', 'khulawha', 9)
    graph.connect('Qariat Zaman', 'Winter Wonderland', 15)
    graph.connect('Riyadh Boulevard','Winter Wonderland', 7)
    graph.connect('Riyadh Boulevard', 'Riyadh Front', 24)


    # Create heuristics (straight-line distance in KM) for Destination Bus Stop
    SLheuristics = {}
    SLheuristics['Riyadh Front'] = 22
    SLheuristics['Qariat Zaman'] = 20
    SLheuristics['khulawha'] = 27
    SLheuristics['Winter Wonderland'] = 9
    SLheuristics['Riyadh Boulevard'] = 6
    SLheuristics['Via Riyadh'] = 8
    SLheuristics['Al Murabba'] = 17
    SLheuristics['The Groves'] = 6
    SLheuristics['Tuwaiq Palace'] = 5
    SLheuristics['Al Salam Tree'] = 17
    SLheuristics['Bus Stop'] = 0
    

    # Create heuristics (time based in min) for Destination Bus Stop
    Theuristics = {}
    Theuristics['Riyadh Front'] = 36 
    Theuristics['Qariat Zaman'] = 28
    Theuristics['khulawha'] = 44
    Theuristics['Winter Wonderland'] = 23
    Theuristics['Riyadh Boulevard'] = 12
    Theuristics['Via Riyadh'] = 24
    Theuristics['Al Murabba'] = 33
    Theuristics['The Groves'] = 15
    Theuristics['Tuwaiq Palace'] = 17
    Theuristics['Al Salam Tree'] = 41
    Theuristics['Bus Stop'] = 0
    

    # Create heuristics (minimum Stops) for Destination Bus Stop
    MinSheuristics = {}
    MinSheuristics['Riyadh Front'] = 20 
    MinSheuristics['Qariat Zaman'] = 10
    MinSheuristics['khulawha'] = 20
    MinSheuristics['Winter Wonderland'] = 20
    MinSheuristics['Riyadh Boulevard'] = 10
    MinSheuristics['Via Riyadh'] = 20
    MinSheuristics['Al Murabba'] = 20
    MinSheuristics['The Groves'] = 10
    MinSheuristics['Tuwaiq Palace'] = 20
    MinSheuristics['Al Salam Tree'] = 30
    MinSheuristics['Bus Stop'] = 0
    
        
    # Print Graph Nodes
    #graph.printgraph()
    #print("--------------------------------\n\n")
    
    #Create a Sorce Node 
    SorceNode = "The Groves"
    
    # Run search algorithm for each heuristic
    print("Using stright-line heuristic")   
    SLpath,h= A_Star(graph, SLheuristics, SorceNode, 'Bus Stop')     
    print("Path: " ,end = " ")
    print(SLpath)

    print("\nUsing least Time heuristic") 
    Tpath,time = A_Star(graph, Theuristics, SorceNode, 'Bus Stop')       
    print("Least time: "+str(time)+" Km/m")
    print("Path: " ,end = " ")
    print(Tpath)

    print("\nUsing minimum Stops heuristic")         
    Minpath,h= A_Star(graph, MinSheuristics, SorceNode, 'Bus Stop') 
    print("Number of stops: "+str(len(Minpath)))
    print("Path: " ,end = " ")
    print(Minpath)
    

# Tell python to run main method
if __name__ == "__main__": 
    main()
