import networkx as nx
import json 
import pickle 

def rt_ids(tweets_fn, graph_fn, outfolder='data'):
    edges = set()
    with open(tweets_fn) as file:
        for line in file:
            tweet = json.loads(line)
            try:
                if 'referenced_tweets' in tweet.keys():
                    edges.add((tweet['id'], tweet['referenced_tweets'][0]['id']))
            except KeyError:
                pass
    with open(graph_fn, 'wb') as graph_edges:
        pickle.dump(edges, graph_edges)
    return 

def create_kcore(graph_fn, cores, outfolder='data'):
    with open(graph_fn, 'rb') as file:
        edges = pickle.load(file)

    graph = nx.DiGraph()
    graph.add_edges_from(edges)
    graph.remove_edges_from(nx.selfloop_edges(graph))
    num_edges = len(nx.k_core(graph, k=int(cores)).edges())
    
    with open(outfolder + "/outputs.txt", "a") as text_file:
        text_file.write(f'The number of edges with {cores} cores was {num_edges}.\n')
    return 
    
