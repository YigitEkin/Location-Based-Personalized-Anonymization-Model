from collections import defaultdict

def hash_function(id):
    string = ''
    if id :
        while id > 0:
            i = id % 10
            string += str(i * 475)
            id = id // 10
        return string
    else:
        return 0

class Message:
    def __init__(self, x, y, msg, id, k):
        self.x = x
        self.y = y
        self.L = (x, y)
        self.msg = msg
        self.id = id
        self.k = k

    def printData(self, B):
        print("ID: ", self.id, "hashed ID:", hash_function(self.id) ,"B: ", B, " k: ", self.k, "content:", self.msg,)
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getL(self):
        return self.L
    def getMsg(self):
        return self.msg
    def getId(self):
        return self.id
    def getK(self):
        return self.k
    def setX(self, x):
        self.x = x
    def setY(self, y):
        self.y = y
    def setL(self, L):
        self.L = L
    def setMsg(self, msg):
        self.msg = msg

class Queue:
    def __init__(self):
        self.items = []
    def isEmpty(self):
        return self.items == []
    def enqueue(self, item):
        self.items.insert(0,item)
    def dequeue(self):
        return self.items.pop()
    def size(self):
        return len(self.items)
    def printQueue(self):
        print(self.items)
    def peek(self):
        return self.items[-1]
    def clear(self):
        self.items = []

class multiDimIndex:
    def __init__(self):
        self.array = []
        self.length = 0
    def add(self, msg, L):
        self.array.append((msg, L))
        self.length += 1
    def get(self, index):
        return self.array[index]
    def getLength(self):
        return self.length
        # (x,y), (x-dx, x+dx) (y-dy, y+dy)
    def checkInRange(tuple, interval):
        return tuple[0] >= interval[0][0] and tuple[0] <= interval[0][1] and tuple[1] >= interval[1][0] and tuple[1] <= interval[1][1] 
    def remove(self, msg):
        for i in range(self.length):
            if self.array[i][0].id == msg.id:
                self.array.pop(i)
                self.length -= 1
    def rangeSearch(self, intervals):
        tmp = []
        x_interval = intervals[0]
        y_interval = intervals[1]
        for i in range(self.length):
            if multiDimIndex.checkInRange(self.array[i][1], (x_interval, y_interval)):
                tmp.append(self.array[i])
        return tmp

#write a directed non-weighted graph class
class Graph:
    def __init__(self):
        self.graph = defaultdict(list)
    def add_edge(self, u, v):
        self.graph[u].append(v)
    def getEdges(self, u):
        return self.graph[u]
    def printGraph(self):
        for i in self.graph:
            #print all elements in the list self.graph
            print(i, ":", self.graph[i])
    def add_node(self, node):
        self.graph[node] = []
    #get the subgraph of the graph such that the nodes are in the messages
    def remove_node(self, node):
        self.graph.pop(node)
    def getSubgraph(self, messages):
        subgraph = Graph()
        for i in messages:
            for j in self.getEdges(i[0]):
                subgraph.add_edge(i[0], j)
                #print("add edge", i[0], j)
        return subgraph
    def getNeighbors(self, node):
        return self.graph[node]

