
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
        
    def __init__(self, name, parent, g, h, f):                                      # Initializing the class
        self.name = name
        self.parent = parent                                                        # node's parent
        self.g = g                                                                  # Distance to start node
        self.h = h                                                                  # Distance to goal node
        self.f = f                                                                  # Total cost
            
    def __eq__(self, other):                                                        # Comparing two nodes
        return self.name == other.name
    
    def __lt__(self, other):                                                        # Sorting nodes
        return self.f < other.f
    
    def __repr__(self):                                                             # Printing nodes
        return ('({0},{1})'.format(self.name, self.f))
    
   

###########################################################################################################################

###################################################### Graph Class ########################################################

class Graph:
    
    def __init__(self, graph_dict=None):                                           # Initialize the class
        self.graph_dict = graph_dict or {}
                    
    def connect(self, A, B, distance=1):                                           # Add a link from A and B of given distance
        self.graph_dict.setdefault(A, {})[B] = distance
        self.graph_dict.setdefault(B, {})[A] = distance
               
    def get(self, a, b=None):                                                      # Get neighbors or a neighbor
        links = self.graph_dict.setdefault(a, {})
        if b is None:
            return links
        else:
            return links.get(b)
            
    def nodes(self):                                                              # Return a list of nodes in the graph
        s1 = set([k for k in self.graph_dict.keys()])
        s2 = set([k2 for v in self.graph_dict.values() for k2, v2 in v.items()])
        nodes = s1.union(s2)
        return list(nodes)

    def getNode(self, city, heuristics, end):                                     # Get a specific neighbour which has minimum cost
        nodes = list()
        min = 9999
        #b= neighbour,dist= cost between them 
        for (b,dist) in self.graph_dict[city].items():
            if(b == end):
                return Node(city, b, dist, heuristics[b], dist+heuristics[b] )
            nodes.append(Node(city, b, dist, heuristics[b], dist+heuristics[b] ))
            if (dist+heuristics[b]) <= min:
                min = dist+heuristics[b]
                minnode = Node(city, b, dist, heuristics[b], dist+heuristics[b] )
        return minnode
        
    def printgraph(self):                                                         # Function to print each edge in the entire graph
         for a in list(self.graph_dict.keys()):
            for (b, dist) in self.graph_dict[a].items():
                print (self.graph_dict.setdefault(a,{})[b], end = " : ")
                print(a, end = " - ")
                print(b)


###########################################################################################################################

################################################## A* Implementation ######################################################
        

def A_Star(graph, heuristics, start, end):
    open_list = list()                                                              # candidate nodes
    closed_list = list()                                                            # visited nodes
    path = list()                                                                   # Will store the path we are taking
    curr_node = graph.getNode(start,heuristics, end)                                # Starting node
    open_list.append(curr_node)
    totalcost = 0

    if(end not in graph.graph_dict):                                                # Incase the goal state does not exist
        print("\n\n---------------------------\nGOAL STATE DOES NOT EXIST\n---------------------------\n\n")
        return  None

    while(curr_node.name != end):                                                   # Runs Until we cannot find the goal state
        totalcost += curr_node.g
        path.append(curr_node.name)
        curr_node = open_list.pop()
        closed_list.append(curr_node)
        curr_node = graph.getNode(curr_node.parent,heuristics, end)
        open_list.append(curr_node)
        if(curr_node.name == end):
            path.append(curr_node.name)
            break
    return path,totalcost
  
###########################################################################################################################

########################################################## Main ###########################################################


# The main entry point for this module
def main():
    # Create a graph
    graph = Graph()
        
    # Create graph connections (Actual distance in KM)
    graph.connect('Bus stop', 'Riyadh boulevard', 10)
    graph.connect('Bus stop', 'Qariat zaman', 23)
    graph.connect('Bus stop', 'The groves', 12) 
    graph.connect('Tuwaiq palace','Via riyadh', 10)
    graph.connect('Tuwaiq palace','The groves', 8)
    graph.connect('Via riyadh', 'The groves', 12)
    graph.connect('Via riyadh', 'al salam tree',15)
    graph.connect('Al murabba','Via riyadh', 12)
    graph.connect('Al murabba','al salam tree', 6)
    graph.connect('Al murabba','Qariat zaman', 27)
    graph.connect('Al murabba', 'Khulawha', 33)
    graph.connect('Qariat zaman', 'Riyadh front', 13)
    graph.connect('Qariat zaman', 'Khulawha', 15)
    graph.connect('Qariat zaman', 'Winter wonderland', 15)
    graph.connect('Riyadh boulevard','Winter wonderland', 10)
    graph.connect('Riyadh boulevard', 'Riyadh front', 21)


    # Create heuristics (straight-line distance in KM) for Destination Bus Stop
    SLheuristics = {}
    SLheuristics['Riyadh front'] = 22
    SLheuristics['Qariat zaman'] = 21
    SLheuristics['Khulawha'] = 27
    SLheuristics['Winter wonderland'] = 9
    SLheuristics['Riyadh boulevard'] = 6
    SLheuristics['Via riyadh'] = 8
    SLheuristics['Al murabba'] = 16
    SLheuristics['The groves'] = 6
    SLheuristics['Tuwaiq palace'] = 6
    SLheuristics['al salam tree'] = 18
    SLheuristics['Bus stop'] = 0
    

    # Create heuristics (time based in min) for Destination Bus Stop
    Theuristics = {}
    Theuristics['Riyadh front'] = 36 
    Theuristics['Qariat zaman'] = 31
    Theuristics['Khulawha'] = 40
    Theuristics['Winter wonderland'] = 17
    Theuristics['Riyadh boulevard'] = 17
    Theuristics['Via riyadh'] = 20
    Theuristics['Al murabba'] = 30
    Theuristics['The groves'] = 19
    Theuristics['Tuwaiq palace'] = 22
    Theuristics['al salam tree'] = 35
    Theuristics['Bus stop'] = 0
    

    # Create heuristics (minimum Stops) for Destination Bus Stop
    MinSheuristics = {}
    MinSheuristics['Riyadh front'] = 20 
    MinSheuristics['Qariat zaman'] = 10
    MinSheuristics['Khulawha'] = 20
    MinSheuristics['Winter wonderland'] = 20
    MinSheuristics['Riyadh boulevard'] = 10
    MinSheuristics['Via riyadh'] = 20
    MinSheuristics['Al murabba'] = 20
    MinSheuristics['The groves'] = 10
    MinSheuristics['Tuwaiq palace'] = 20
    MinSheuristics['al salam tree'] = 30
    MinSheuristics['Bus stop'] = 0
    
        
    # Print Graph Nodes
    #graph.printgraph()
    #print("--------------------------------\n\n")
    
    #Create a Source Node 
    print("How would you like to choose a path \n1-shortest distance \n2-least time \n3-minimum stop ")
    option=input()

    try:
        print("Please enter the start node")
        SourceNode =input().capitalize()

        if(option=="1"):
        # Run search algorithm for each heuristic
            print("\nUsing stright-line heuristic\n")   
            path,cost= A_Star(graph, SLheuristics, SourceNode, 'Bus stop')  
        elif(option=="2"):
            print("\nUsing least Time heuristic\n") 
            path,cost= A_Star(graph, Theuristics, SourceNode, 'Bus stop') 
            time=round((cost/50)*60)
            print("Time in minutes: "+str(time))
        elif(option=="3"):
            print("\nUsing minimum Stops heuristic\n")         
            path,cost= A_Star(graph, MinSheuristics, SourceNode, 'Bus stop')

        print("Final cost: " + str(cost) + " KM")
        print("Path:" ,end = " ")
        print(path) 

    except KeyError:
        print("The node is not found please choose one of these nodes")
        for s in MinSheuristics:
            if (s=="Bus stop"):
                break
            print(s)
    

# Tell python to run main method
if __name__ == "__main__": 
    main()
