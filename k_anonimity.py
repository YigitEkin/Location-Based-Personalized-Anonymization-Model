import argparse
import sys

import pandas as pd

import helpers as helpers


def get_min_BB(M):
    if(len(M) > 0):
        min_x = M[0].x
        min_y = M[0].y
        max_x = M[0].x
        max_y = M[0].y
        for i in range(len(M)):
            if M[i].x < min_x:
                min_x = M[i].x
            if M[i].y < min_y:
                min_y = M[i].y
            if M[i].x > max_x:
                max_x = M[i].x
            if M[i].y > max_y:
                max_y = M[i].y
        return ((min_x, max_x), (min_y, max_y))
    return ((0,0),(0,0))

def check_is_in_range(msg, B):
    return msg.x >= B[0][0] and msg.x <= B[0][1] and msg.y >= B[1][0] and msg.y <= B[1][1]

def msgPertEngine(queue, dx, dy):
    cnt = 0
    Im = helpers.multiDimIndex()
    graph  = helpers.Graph()
    bounding_boxes = []
    k_anonimity_neighborhoods = []
    index = 0
    while True:
        if not queue.isEmpty():
            msg = queue.dequeue() #msg obj is returned
            B = ((msg.x - dx,msg.x + dx), (msg.y - dy, msg.y + dy))
            Im.add(msg, msg.L)
            graph.add_node(msg)
            N = Im.rangeSearch(B) #(msg, L) tuples are returned
            if len(N) < msg.k:
                cnt += 1
            for i in range(len(N)):
                B_n = ((N[i][0].x - dx,N[i][0].x + dx), (N[i][0].y - dy, N[i][0].y + dy))
                if N[i][0].id != msg.id and check_is_in_range(msg, B_n):
                    graph.add_edge(msg, N[i][0])
            subgraph = graph.getSubgraph(N)
            M = local_k_search(msg.k, msg, subgraph)
            B_tmp = get_min_BB(M)
            if len(M) > 0:
                bounding_boxes.append(B_tmp)
                if len(M) < msg.k:
                    print(f"K Anonimity is not satisfied for value {msg.k} for the following messages:")
                    cnt += 1
                for i in range(len(M)):
                    M[i].printData(B_tmp)
                    if msg in graph.graph:
                        graph.remove_node(msg)
                    Im.remove(msg)
            print("---------------------------------------------------------------------------------------")
        else:
            return cnt


def local_k_search(k, msg, subgraph):
    neighbors = subgraph.getNeighbors(msg)
    U = []
    for neighbor in neighbors:
        if neighbor.k >= k:
            U.append(neighbor)
    if len(U) < k - 1:
        return []
    l = 0
    while l != len(U):
        l = len(U)
        tmp = []
        for i in range(len(U)):
            neighbors = subgraph.getNeighbors(U[i])
            intersection = []
            for neighbor in neighbors:
                if neighbor in U:
                    intersection.append(neighbor)
            for neighbor in intersection:
                if len(intersection) < k - 2:
                    ind = U.index(neighbor)
                    tmp.append(ind)
        #decrementing for loop for removing elements from list
        for i in range(len(tmp)-1, -1, -1):
            U.pop(tmp[i])
    M = []
    for i in range(len(U)):
        M.append(U[i])

    return_val = M
    return_val.append(msg)

    return return_val

#write a argument parser with argparse make each argument required
def parse_args():
    parser = argparse.ArgumentParser(description='K anonimity perturbation engine')
    parser.add_argument('-csv_file', type=str, required=True, help='csv file to read')
    parser.add_argument('-k_anonimity_treshold', type=int, required=True, help='k anonimity treshold')
    parser.add_argument('-dx', type=float, required=True, help='dx value')
    parser.add_argument('-dy', type=float, required=True, help='dy value')
    args = parser.parse_args()
    return args

def main():
    #read the csv files relative path from the command line arguments
    args = parse_args()
    filename = args.csv_file
    k_anonimity_treshold = args.k_anonimity_treshold
    dx = args.dx
    dy = args.dy

    #read the csv file
    df = pd.read_csv(filename)
    messages = []

    if k_anonimity_treshold < 2:
        print("K anonimity treshold must be greater than 2")
        return

    print("WELCOME TO THE K ANONIMITY PERTURBATION ENGINE")
    print("THE ALGORITHM WILL PERTURB THE MESSAGES IN THE DATASET TO SATISFY THE K ANONIMITY TRESHOLD FOR EACH MESSAGE")
    print(f"THE K ANONIMITY TRESHOLD IS SET TO {k_anonimity_treshold}")
    print("---------------------------------------------------------------------------------------")

    queue = helpers.Queue()
    #iterate through the dataframe and create a message object for each row
    for i in range(len(df)):
        messages.append(helpers.Message(df['Latitude'][i], df['Longitude'][i], df['Name'][i], df['OBJECTID'][i], k_anonimity_treshold))
    for msg in messages:
        queue.enqueue(msg)
    cnt = msgPertEngine(queue, dx, dy)
    print (len(df))
    print( f"Out of {len(df)} messages, {cnt} did not satisfy k-anonimity for k value {k_anonimity_treshold}")

main()


